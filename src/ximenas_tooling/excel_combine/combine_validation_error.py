from ximenas_tooling.excel_combine.column_mismatch import ColumnMismatchReport

ALLOW_COLUMN_MISMATCH_HINT = (
    "To combine anyway (missing values left blank), "
    "set allow_column_mismatch = True in the notebook form and run again."
)


class CombineValidationError(Exception):
    """Every problem found across all input files, reported at once so the user can fix them in one pass."""

    def __init__(self, problems: list[str], column_mismatch: ColumnMismatchReport | None = None):
        self.problems = problems
        self.column_mismatch = column_mismatch
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        banner = (
            "COLUMN MISMATCH — nothing was written."
            if self.column_mismatch
            else "PROBLEMS FOUND — nothing was written."
        )
        lines = [banner]
        if self.problems:
            lines += ["", "Problems:"] + [f"  - {problem}" for problem in self.problems]
        if self.column_mismatch:
            lines += [""] + self.column_mismatch.describe_lines()
            lines += ["", ALLOW_COLUMN_MISMATCH_HINT]
        return "\n".join(lines)
