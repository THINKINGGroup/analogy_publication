import typer

from analogy import __version__
from analogy.utils.file_utils import do_checks

app = typer.Typer()


@app.command()
def version() -> None:
    """Display the CLI version number."""
    typer.echo(f"Analogy version : {__version__}")


@app.command()
def analyse(filepath: str, result_dest: str) -> None:
    """
    Run the incidence prevalence analysis.
    """
    do_checks(filepath, result_dest)


if __name__ == "__main__":
    app()
