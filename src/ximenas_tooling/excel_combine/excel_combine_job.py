from pathlib import Path

from ximenas_tooling.excel_combine.column_mismatch import ColumnMismatchReport
from ximenas_tooling.excel_combine.combine_validation_error import CombineValidationError
from ximenas_tooling.excel_combine.excel_tab_reader import ExcelTabReader
from ximenas_tooling.excel_combine.input_file_finder import InputFileFinder
from ximenas_tooling.excel_combine.tab_combiner import TabCombiner

DEFAULT_OUTPUT_FILE_NAME = "combined.xlsx"
EXCEL_SHEET_NAME_MAX_LENGTH = 31


class ExcelCombineJob:
    """Combines one named tab from every .xlsx file in a folder into a single .xlsx file in that folder."""

    @staticmethod
    def run(
        input_folder: str,
        tab_name: str,
        output_file_name: str = DEFAULT_OUTPUT_FILE_NAME,
        allow_column_mismatch: bool = False,
    ) -> Path:
        if not tab_name.strip():
            raise CombineValidationError(["tab_name is empty. Enter the name of the tab to combine."])
        folder = Path(input_folder)
        files = InputFileFinder(output_file_name).find(folder)

        reader = ExcelTabReader(tab_name)
        read_problems = []
        tables = []
        for path in files:
            result = reader.read(path)
            read_problems += result.problems
            if result.table is not None:
                tables.append(result.table)
                print(f"Read rows=[{len(result.table.frame)}] from file=[{path.name}]")

        combined = TabCombiner(allow_column_mismatch).combine(tables, upstream_problems=read_problems)
        if combined.tolerated_column_mismatch:
            ExcelCombineJob._print_mismatch_warning(combined.tolerated_column_mismatch)

        output_path = folder / output_file_name
        combined.frame.to_excel(
            output_path, sheet_name=tab_name[:EXCEL_SHEET_NAME_MAX_LENGTH], index=False, engine="openpyxl"
        )
        print(f"Total rows=[{len(combined.frame)}] from files=[{len(tables)}]")
        print(f"Wrote output=[{output_path}]")
        return output_path

    @staticmethod
    def _print_mismatch_warning(report: ColumnMismatchReport) -> None:
        banner = "!" * 72
        lines = [banner, "WARNING: COLUMN MISMATCH — combining anyway (allow_column_mismatch = True)."]
        lines += ["Cells are left blank where a file lacks a column."]
        lines += report.describe_lines() + [banner]
        print("\n".join(lines))
