import pandas as pd
import pytest

from ximenas_tooling.excel_combine.combine_validation_error import CombineValidationError
from ximenas_tooling.excel_combine.source_table import SourceTable
from ximenas_tooling.excel_combine.tab_combiner import SOURCE_FILE_COLUMN, TabCombiner


def table(file_name: str, data: dict) -> SourceTable:
    return SourceTable(file_name=file_name, frame=pd.DataFrame(data))


class TestTabCombinerGivenMatchingColumnsInDifferentOrderCaseAndSpacing:
    @pytest.fixture
    def result(self):
        tables = [
            table("a.xlsx", {"Campaign Name": ["x", "y"], "Clicks": [1, 2]}),
            table("b.xlsx", {"clicks": [3], "  campaign   NAME ": ["z"]}),
        ]
        return TabCombiner().combine(tables)

    def test_THEN_headers_come_from_first_file_plus_source_file(self, result):
        assert list(result.frame.columns) == ["Campaign Name", "Clicks", SOURCE_FILE_COLUMN]

    def test_THEN_all_rows_are_present_with_values_aligned(self, result):
        assert result.frame["Campaign Name"].tolist() == ["x", "y", "z"]

    def test_THEN_numbers_stay_aligned(self, result):
        assert result.frame["Clicks"].tolist() == [1, 2, 3]

    def test_THEN_source_file_holds_file_name(self, result):
        assert result.frame[SOURCE_FILE_COLUMN].tolist() == ["a.xlsx", "a.xlsx", "b.xlsx"]

    def test_THEN_no_mismatch_is_reported(self, result):
        assert result.tolerated_column_mismatch is None


class TestTabCombinerGivenColumnMismatch:
    @pytest.fixture
    def tables(self):
        return [
            table("a.xlsx", {"Campaign": ["x"], "Clicks": [1]}),
            table("b.xlsx", {"Campaign": ["y"], "Impressions": [10]}),
        ]

    @pytest.fixture
    def error_message(self, tables):
        with pytest.raises(CombineValidationError) as error:
            TabCombiner().combine(tables)
        return str(error.value)

    def test_WHEN_default_THEN_message_starts_with_banner(self, error_message):
        assert error_message.startswith("COLUMN MISMATCH — nothing was written.")

    @pytest.mark.parametrize(
        "expected_text",
        ["allow_column_mismatch", "missing: ['Clicks']", "unexpected: ['Impressions']", "a.xlsx", "b.xlsx"],
    )
    def test_WHEN_default_THEN_message_contains(self, error_message, expected_text):
        assert expected_text in error_message

    def test_WHEN_default_THEN_message_ends_with_override_hint(self, error_message):
        assert error_message.endswith(
            "To combine anyway (missing values left blank), "
            "set allow_column_mismatch = True in the notebook form and run again."
        )

    def test_WHEN_allowed_THEN_columns_are_the_union(self, tables):
        result = TabCombiner(allow_column_mismatch=True).combine(tables)
        assert list(result.frame.columns) == ["Campaign", "Clicks", "Impressions", SOURCE_FILE_COLUMN]

    def test_WHEN_allowed_THEN_missing_cells_are_blank(self, tables):
        result = TabCombiner(allow_column_mismatch=True).combine(tables)
        assert result.frame["Clicks"].isna().tolist() == [False, True]

    def test_WHEN_allowed_THEN_row_count_is_sum_of_files(self, tables):
        result = TabCombiner(allow_column_mismatch=True).combine(tables)
        assert len(result.frame) == 2

    def test_WHEN_allowed_THEN_mismatch_is_reported_for_the_warning(self, tables):
        result = TabCombiner(allow_column_mismatch=True).combine(tables)
        assert result.tolerated_column_mismatch.mismatches[0].file_name == "b.xlsx"


class TestTabCombinerGivenInvalidTables:
    def test_GIVEN_duplicate_normalized_columns_THEN_error_names_the_column(self):
        tables = [table("a.xlsx", {"Clicks": [1], " clicks": [2]})]
        with pytest.raises(CombineValidationError, match=r"a\.xlsx: several columns have the same name.*'clicks'"):
            TabCombiner().combine(tables)

    def test_GIVEN_existing_source_file_column_THEN_error(self):
        tables = [table("a.xlsx", {"Clicks": [1], "source  FILE": ["q"]})]
        with pytest.raises(CombineValidationError, match=r"a\.xlsx: already has a \[Source File\] column"):
            TabCombiner().combine(tables)

    def test_GIVEN_upstream_problem_and_mismatch_THEN_both_are_in_one_error(self):
        tables = [table("a.xlsx", {"A": [1]}), table("b.xlsx", {"B": [1]})]
        with pytest.raises(CombineValidationError) as error:
            TabCombiner().combine(tables, upstream_problems=["c.xlsx: tab [Data] not found."])
        assert "c.xlsx: tab [Data] not found." in str(error.value) and "b.xlsx: missing" in str(error.value)

    def test_GIVEN_no_tables_THEN_error(self):
        with pytest.raises(CombineValidationError):
            TabCombiner().combine([])
