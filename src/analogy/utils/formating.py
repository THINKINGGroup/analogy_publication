from typing import List, TypedDict

from collections import namedtuple

Arguments = TypedDict(
    "Arguments",
    {
        "study_start_date": str,
        "study_end_date": str,
        "conditions": List[str],
        "demography": List[str],
        "patient_start_col": str,
        "patient_end_col": str,
        "person_years": int,
        "date_format": str,
        "increment_by_months": int,
    },
)


def format_input(
    startdate: str,
    enddate: str,
    conditions: str,
    demography: str,
    dateformat: str,
    patientstartcol: str,
    patientendcol: str,
    personyears: int,
    increment: int,
) -> Arguments:
    """
    Function format user input and store it in a named tuple.

    Args:
      startdate (str):
      enddate (str):
      conditions (str):
      demography (str):
      dateformat (str):
      patientstartcol (str):
      patientendcol (str):
      personyears (int):
      increment (int):

    Returns:
      Arguments (dict)
    """
    Arguments = namedtuple(
        "Arguments",
        [
            "study_start_date",
            "study_end_date",
            "condition_columns",
            "demography_columns",
            "followup_start_col",
            "followup_end_col",
            "personyears",
            "dateformat",
            "increment",
        ],
    )
    condition_list = conditions.replace(" ", "").split(",")

    if not (demography and demography.strip()):
        demography_list = []
    else:
        demography_list = demography.replace(" ", "").split(",")

    return {
        "study_start_date": startdate,
        "study_end_date": enddate,
        "conditions": condition_list,
        "demography": demography_list,
        "patient_start_col": patientstartcol,
        "patient_end_col": patientendcol,
        "person_years": int(personyears),
        "date_format": dateformat,
        "increment_by_months": int(increment),
    }
