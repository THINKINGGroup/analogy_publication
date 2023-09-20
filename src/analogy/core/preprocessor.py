from typing import List

from datetime import datetime

import pandas as pd


def format_datatypes(
    data: pd.DataFrame,
    condition_cols: List[str],
    demography_cols: List[str] = None,
    patient_follow_up_cols: List[str] = None,
    date_format: str = "ISO8601",
) -> pd.DataFrame:
    """
    Function that formats dataframe column datatypes.
    Find columns with Date data and assign it datetime type
    Find columns with categorical data and assign it pd.Category

    Args:
        data (DataFrame): study data as pandas dataframe.

    Returns:
        data (DataFrame): study data as pandas dataframe with formatted columns.
    """
    if demography_cols is not None:
        data[demography_cols] = data[demography_cols].astype("category")

    data[patient_follow_up_cols] = data[patient_follow_up_cols].apply(
        pd.to_datetime,
        format=date_format,
    )
    data[condition_cols] = data[condition_cols].apply(
        pd.to_datetime,
        format=date_format,
    )

    return data


def convert_str_to_datetime(date_str: str, format: str = "%Y-%m-%d") -> datetime:
    """
    Function to convert string to datetime with user defined format.

    Args:
        date_str (str): datetime as string.
        format (str): datetime format to parse and convert to datetime. Default: %Y-%m-%d

    Returns:
        datetime object

    Raises:
        StudyAnalysisError: study date not in standard format.
    """
    return datetime.strptime(date_str, format)
