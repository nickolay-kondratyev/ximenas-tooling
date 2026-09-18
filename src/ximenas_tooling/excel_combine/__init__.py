"""Combine one named tab from many Excel files into one file, adding a `Source File` column."""

from ximenas_tooling.excel_combine.combine_validation_error import CombineValidationError
from ximenas_tooling.excel_combine.excel_combine_job import ExcelCombineJob

run = ExcelCombineJob.run

__all__ = ["run", "CombineValidationError", "ExcelCombineJob"]
