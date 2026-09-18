import re


class ColumnNameNormalizer:
    """Single source of the name-matching rule, shared by tab names and column names.

    Excel headers typed by hand differ in case and spacing ("Campaign  Name " vs "campaign name");
    they must still be treated as the same name.
    """

    _WHITESPACE_RUN = re.compile(r"\s+")

    @staticmethod
    def normalize(name: object) -> str:
        collapsed = ColumnNameNormalizer._WHITESPACE_RUN.sub(" ", str(name).strip())
        return collapsed.lower()
