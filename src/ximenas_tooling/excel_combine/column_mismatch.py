from dataclasses import dataclass


@dataclass(frozen=True)
class ColumnMismatch:
    """How one file's columns differ from the reference (first) file. Names are original header text."""

    file_name: str
    missing: list[str]
    unexpected: list[str]

    def describe(self) -> str:
        return f"{self.file_name}: missing: {self.missing}, unexpected: {self.unexpected}"


@dataclass(frozen=True)
class ColumnMismatchReport:
    reference_file_name: str
    mismatches: list[ColumnMismatch]

    def describe_lines(self) -> list[str]:
        header = f"Columns compared with the first file [{self.reference_file_name}]:"
        return [header] + [f"  - {mismatch.describe()}" for mismatch in self.mismatches]
