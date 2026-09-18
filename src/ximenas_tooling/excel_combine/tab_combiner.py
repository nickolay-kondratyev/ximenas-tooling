from collections import Counter
from dataclasses import dataclass
from typing import Sequence

import pandas as pd

from ximenas_tooling.excel_combine.column_mismatch import ColumnMismatch, ColumnMismatchReport
from ximenas_tooling.excel_combine.column_name_normalizer import ColumnNameNormalizer
from ximenas_tooling.excel_combine.combine_validation_error import CombineValidationError
from ximenas_tooling.excel_combine.source_table import SourceTable

SOURCE_FILE_COLUMN = "Source File"


@dataclass(frozen=True)
class CombineResult:
    frame: pd.DataFrame
    # Set only when columns differed and allow_column_mismatch let the combine proceed.
    tolerated_column_mismatch: ColumnMismatchReport | None


class TabCombiner:
    """Stacks the extracted tabs of all files into one table, matching columns by normalized name.

    Pure pandas (no file I/O) so the combine rules are easy to test.
    """

    def __init__(self, allow_column_mismatch: bool = False):
        self._allow_column_mismatch = allow_column_mismatch

    def combine(self, tables: Sequence[SourceTable], upstream_problems: Sequence[str] = ()) -> CombineResult:
        """`upstream_problems`: problems found before combining (e.g. a file lacks the tab).

        They are raised together with this combiner's own findings, so the user sees ALL problems in one error.
        """
        problems = list(upstream_problems) + self._find_table_problems(tables)
        if not tables and not problems:
            problems.append("There are no tables to combine.")
        mismatch_report = self._find_column_mismatches(tables) if tables else None
        blocking_mismatch = mismatch_report if not self._allow_column_mismatch else None
        if problems or blocking_mismatch:
            raise CombineValidationError(problems, blocking_mismatch)

        return CombineResult(frame=self._stack(tables), tolerated_column_mismatch=mismatch_report)

    @staticmethod
    def _find_table_problems(tables: Sequence[SourceTable]) -> list[str]:
        problems = []
        source_file_key = ColumnNameNormalizer.normalize(SOURCE_FILE_COLUMN)
        for table in tables:
            counts = Counter(ColumnNameNormalizer.normalize(column) for column in table.frame.columns)
            duplicates = [name for name, count in counts.items() if count > 1]
            if duplicates:
                problems.append(
                    f"{table.file_name}: several columns have the same name "
                    f"(ignoring case and spacing): {duplicates}. Rename or remove the extras."
                )
            if source_file_key in counts:
                problems.append(
                    f"{table.file_name}: already has a [{SOURCE_FILE_COLUMN}] column, "
                    "which this tool adds itself. Rename or remove it."
                )
        return problems

    @staticmethod
    def _find_column_mismatches(tables: Sequence[SourceTable]) -> ColumnMismatchReport | None:
        reference = tables[0]
        reference_columns = TabCombiner._columns_by_key(reference)
        mismatches = []
        for table in tables[1:]:
            columns = TabCombiner._columns_by_key(table)
            missing = [name for key, name in reference_columns.items() if key not in columns]
            unexpected = [name for key, name in columns.items() if key not in reference_columns]
            if missing or unexpected:
                mismatches.append(ColumnMismatch(table.file_name, missing=missing, unexpected=unexpected))
        if not mismatches:
            return None
        return ColumnMismatchReport(reference_file_name=reference.file_name, mismatches=mismatches)

    @staticmethod
    def _columns_by_key(table: SourceTable) -> dict[str, str]:
        """Normalized name -> original header text, in the table's column order."""
        return {ColumnNameNormalizer.normalize(column): str(column) for column in table.frame.columns}

    @staticmethod
    def _stack(tables: Sequence[SourceTable]) -> pd.DataFrame:
        # Output header = original text from the first file having the column; order = first appearance.
        output_header_by_key: dict[str, str] = {}
        for table in tables:
            for key, name in TabCombiner._columns_by_key(table).items():
                output_header_by_key.setdefault(key, name)

        aligned = []
        for table in tables:
            frame = table.frame.rename(
                columns=lambda column: output_header_by_key[ColumnNameNormalizer.normalize(column)]
            )
            aligned.append(frame.assign(**{SOURCE_FILE_COLUMN: table.file_name}))

        output_columns = list(output_header_by_key.values()) + [SOURCE_FILE_COLUMN]
        # WHY-NOT concat empty frames: pandas warns about their dtype handling; reindex restores their columns anyway.
        non_empty = [frame for frame in aligned if not frame.empty]
        if not non_empty:
            return pd.DataFrame(columns=output_columns)
        return pd.concat(non_empty, ignore_index=True).reindex(columns=output_columns)
