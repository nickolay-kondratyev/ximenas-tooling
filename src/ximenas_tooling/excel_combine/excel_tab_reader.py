from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
from openpyxl.utils import get_column_letter

from ximenas_tooling.excel_combine.column_name_normalizer import ColumnNameNormalizer
from ximenas_tooling.excel_combine.source_table import SourceTable


@dataclass(frozen=True)
class TabReadResult:
    """Either the extracted table, or the problems that prevented reading it."""

    table: SourceTable | None = None
    problems: list[str] = field(default_factory=list)


class ExcelTabReader:
    """Reads the one tab whose name matches `tab_name` (case/spacing-insensitive) from an .xlsx file.

    Other tabs are never parsed: only the extracted tab matters to the combine.
    """

    def __init__(self, tab_name: str):
        self._tab_name = tab_name
        self._normalized_tab_name = ColumnNameNormalizer.normalize(tab_name)

    def read(self, path: Path) -> TabReadResult:
        with pd.ExcelFile(path, engine="openpyxl") as workbook:
            matching = [
                name
                for name in workbook.sheet_names
                if ColumnNameNormalizer.normalize(name) == self._normalized_tab_name
            ]
            if not matching:
                return TabReadResult(
                    problems=[
                        f"{path.name}: tab [{self._tab_name}] not found. "
                        f"Tabs in this file: {workbook.sheet_names}"
                    ]
                )
            if len(matching) > 1:
                return TabReadResult(
                    problems=[
                        f"{path.name}: several tabs match [{self._tab_name}]: {matching}. "
                        "Rename all but one."
                    ]
                )
            # WHY-NOT header=0: pandas would silently rename duplicate headers ("Clicks", "Clicks.1"),
            # hiding duplicates we must report. So row 1 is taken as the header by hand.
            raw = workbook.parse(matching[0], header=None)
        return self._to_table(path.name, raw)

    def _to_table(self, file_name: str, raw: pd.DataFrame) -> TabReadResult:
        # Excel often keeps formatted-but-empty rows/columns around the real data.
        raw = raw.dropna(how="all").dropna(axis="columns", how="all")
        if raw.empty:
            return TabReadResult(problems=[f"{file_name}: tab [{self._tab_name}] is empty (no header row)."])

        header = raw.iloc[0]
        # With header=None the column labels are 0-based sheet positions, so they map to Excel letters.
        blank_header_letters = [get_column_letter(position + 1) for position, value in header.items() if pd.isna(value)]
        if blank_header_letters:
            return TabReadResult(
                problems=[
                    f"{file_name}: tab [{self._tab_name}] has data under an empty header "
                    f"in column(s) {blank_header_letters}. Add a header in row 1."
                ]
            )

        # infer_objects: the header row forced object dtype; restore numeric/date dtypes of the data.
        frame = raw.iloc[1:].infer_objects().reset_index(drop=True)
        frame.columns = list(header)
        return TabReadResult(table=SourceTable(file_name=file_name, frame=frame))
