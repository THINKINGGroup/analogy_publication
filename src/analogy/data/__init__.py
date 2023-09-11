from typing import List, Optional

from importlib import resources

import numpy as np
import pandas as pd


def _load_dataset(filename: str, columns: Optional[List] = None) -> pd.DataFrame:
    """
    Load a dataset from analogy.data

    Args:
    ----
      filename (string): name of the file to load, for example sample.csv
      columns (list): list of column names to use.

    Returns:
    -------
      Dataframe
    """
    with resources.path("analogy.data", filename) as df:
        return pd.read_csv(df, usecols=columns)


def load_sample_data(columns: Optional[List] = None) -> pd.DataFrame:
    """
    Load data that is part of the analogy package. This data set comes from simulated data from
    Neil Cockburn. This data is used for examples on analogy.readthedocs

    Args:
    ----
      columns (list): list of column names to use.

    Notes:
    -----
    The generated dataset consist of following variables:
      * ID - participant unique ID
      * INDEX_DATE: Date on which the patient follow-up starts.
      * START_DATE: This is the start date for patient follow-up. It is defined as the latest of the following:
                    1. Vision or Computerization date.
                    2. Acceptable Mortality Reporting(AMR) date.
                    3. Patient registration date.
                    4. Study start date.
                    5. Date on which patient becomes eligible for the study based on age restrictions(if any).
      * END_DATE: This is the end date for patient follow-up. It is defined as the earliest of the following:
                    1. Practice collection date.
                    2. Patient transfer date.
                    3. Patient death date.
                    4. Study end date.
                    5. Maximum age(115 years by default) until which patient is eligible to participate in the study.
      * Condition: the baseline condition diagnosis date for which incidence and prevelance is to be calculated.
      * SEX: demographic variable for patient sex [1 (Male), 2 (Female)].
      * ETHNICITY: demographic variable for patient ethnicity [White, Black, Asian, Mixed, Other, Unknown].

    Returns:
    -------
    DataFrame
        Returns a pandas DataFrame.

    Examples:
    --------
    """
    return _load_dataset("sample.csv", columns=columns)
