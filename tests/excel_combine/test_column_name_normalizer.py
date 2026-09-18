from ximenas_tooling.excel_combine.column_name_normalizer import ColumnNameNormalizer


class TestColumnNameNormalizer:
    def test_GIVEN_surrounding_spaces_WHEN_normalize_THEN_trimmed(self):
        assert ColumnNameNormalizer.normalize("  clicks  ") == "clicks"

    def test_GIVEN_inner_whitespace_runs_WHEN_normalize_THEN_collapsed_to_single_space(self):
        assert ColumnNameNormalizer.normalize("campaign \t  name") == "campaign name"

    def test_GIVEN_mixed_case_WHEN_normalize_THEN_lowercased(self):
        assert ColumnNameNormalizer.normalize("Campaign NAME") == "campaign name"

    def test_GIVEN_ticket_example_WHEN_normalize_THEN_campaign_name(self):
        assert ColumnNameNormalizer.normalize("  Campaign   Name ") == "campaign name"

    def test_GIVEN_non_string_WHEN_normalize_THEN_uses_its_text(self):
        assert ColumnNameNormalizer.normalize(2024) == "2024"
