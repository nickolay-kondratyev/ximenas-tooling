from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class SourceTable:
    """The extracted tab of one input file. Column labels are the original header values."""

    file_name: str
    frame: pd.DataFrame
