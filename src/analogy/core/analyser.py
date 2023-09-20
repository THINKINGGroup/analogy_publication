from typing import Any, Dict, List

import pandas as pd

from analogy.core.incidence_prevalence import Incidence, Prevalence
from analogy.utils.file_utils import save_dataframe
from analogy.utils.formating import Arguments


def run_incidence(data: pd.DataFrame, args: Arguments, destination_path: str) -> None:
    """ """
    incidence = Incidence(data, **args)
    output = incidence.analyse()
    save_dataframe(output, destination_path, "incidence_analysis.csv")


def run_prevalence(data: pd.DataFrame, args: Arguments, destination_path: str) -> None:
    """ """
    prevalence = Prevalence(data, **args)
    output = prevalence.analyse()
    save_dataframe(output, destination_path, "prevalence_analysis.csv")
