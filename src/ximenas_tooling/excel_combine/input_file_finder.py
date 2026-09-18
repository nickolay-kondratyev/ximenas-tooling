from pathlib import Path

from ximenas_tooling.excel_combine.combine_validation_error import CombineValidationError

XLSX_SUFFIX = ".xlsx"
# Excel creates "~$<name>.xlsx" lock files next to workbooks that are open.
EXCEL_LOCK_FILE_PREFIX = "~$"


class InputFileFinder:
    """Finds the .xlsx files directly inside a folder (no subfolders), sorted by name for deterministic output."""

    def __init__(self, output_file_name: str):
        # Skipped so a rerun does not ingest the previous run's output.
        self._output_file_name = output_file_name

    def find(self, folder: Path) -> list[Path]:
        if not folder.is_dir():
            raise CombineValidationError([f"Folder not found: [{folder}]. Check the input_folder value."])
        files = sorted(
            (path for path in folder.iterdir() if self._is_input(path)),
            key=lambda path: path.name,
        )
        if not files:
            raise CombineValidationError(
                [f"No {XLSX_SUFFIX} files found directly in folder [{folder}] (other than [{self._output_file_name}])."]
            )
        return files

    def _is_input(self, path: Path) -> bool:
        return (
            path.is_file()
            and path.suffix.lower() == XLSX_SUFFIX
            and not path.name.startswith(EXCEL_LOCK_FILE_PREFIX)
            and path.name != self._output_file_name
        )
