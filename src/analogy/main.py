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
    startdate: str,
    enddate: str,
    dateformat: str,
    patientstartcol: str,
    patientendcol: str,
    personyears: int,
    increment: int,
) -> None:
    """
    Run the incidence prevalence analysis.
    """
    conditions_text = input("Enter the list of conditions columns to analyse (col1, col2, ...): ")
    demography_text = input(
        "Enter the list of demography columns for subgroup analyse or leave empty if none (col1, col2, ...): "
    )
    do_checks(filepath, result_dest)
    args = format_input(
        startdate=startdate,
        enddate=enddate,
        conditions=conditions_text,
        demography=demography_text,
        dateformat=dateformat,
        patientstartcol=patientstartcol,
        patientendcol=patientendcol,
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
