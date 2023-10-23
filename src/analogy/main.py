from typing import List

import typer

from analogy import __version__
from analogy.core.analyser import run_incidence, run_prevalence
from analogy.utils.file_utils import do_checks, file_loader
from analogy.utils.formating import format_input

app = typer.Typer()


@app.command()
def version() -> None:
    """Display the CLI version number."""
    typer.echo(f"Analogy version : {__version__}")


@app.command()
def incprev(
    filepath: str,
    result_dest: str,
    studystart: str,
    studyend: str,
    dateformat: str,
    startdatecol: str,
    enddatecol: str,
    personyears: int,
    increment: int,
) -> None:
    """
    Run the incidence prevalence analysis.

    FILEPATH: The location of your csv data file, please provide absolute path.

    RESULT_DEST: The location to save analysis outputs to, please provide absolute path.

    STUDYSTART: The start date of your study, i.e. the first date on which patients can contribute persontime and events. This will define the date to calculate point prevalence on and the beginning of the incidence calculation period.

    STUDYEND: The end date of your study, i.e. the last date on which patients can contribute persontime and events. This will define the end date to calculate the last incidence period, but will not affect point prevalence dates which are defined using STARTDATE and increment.

    DATEFORMAT: Describe the format of data describing dates. Two key variations need to be described; the order of dates and the units displayed. For example, %Y-%m-%d describes the DATEFORMAT as Year-month-day, in that order, with no hour or minute components.

    STARTDATECOL: The date on which an individual patient becomes eligible to take part in the study and contribute patient-time or events, independently from STARTDATE.

    ENDDATECOL: The date on which an individual patient is no longer eligible to take part in the study and contribute patient-time or events.

    PERSONYEARS: The scale to report results in e.g. per 1000 patients, per 100 patients.  Same for both denominators.

    INCREMENT: The number of months between calculations e.g. between each point prevalence calculation, or the length of the period in months for each incidence calculation.
    """
    conditions_text = input("Enter the list of conditions columns to analyse (col1, col2, ...): ")
    demography_text = input(
        "Enter the list of demography columns for subgroup analyse or leave empty if none (col1, col2, ...): "
    )
    do_checks(filepath, result_dest)
    args = format_input(
        startdate=studystart,
        enddate=studyend,
        conditions=conditions_text,
        demography=demography_text,
        dateformat=dateformat,
        patientstartcol=startdatecol,
        patientendcol=enddatecol,
        personyears=personyears,
        increment=increment,
    )

    usecols = (
        [args["patient_start_col"], args["patient_end_col"]]
        + args["conditions"]
        + args["demography"]
    )
    df = file_loader(filepath, usecols)
    run_incidence(df, args, result_dest)
    run_prevalence(df, args, result_dest)


if __name__ == "__main__":
    app()
