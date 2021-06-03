"""Console script for leruli."""
import sys
import click
import leruli


@click.group()
def cli1():
    pass


@cli1.command()
@click.option(
    "--format",
    type=click.Choice("XYZ PDB SDF".split(), case_sensitive=False),
    default="XYZ",
    help="File format for output, defaults to XYZ.",
)
@click.option("--version", default="latest", help="Request specific API version.")
@click.argument("smiles")
def quickgeometry(smiles: str, format: str, version: str = None):
    """Molecular geometry from SMILES."""
    print(leruli.quickgeometry(smiles, format, version))


@click.group()
def cli2():
    pass


@cli2.command()
def smiles2sumformula():
    """Sum formula from SMILES."""


cli = click.CommandCollection(sources=[cli1, cli2])

if __name__ == "__main__":
    sys.exit(cli())
