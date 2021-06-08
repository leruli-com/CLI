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
@click.option("--version", default="latest", help="Request specific API version.")
@click.argument("sumformula")
def canonicalizechemicalformula(
    sumformula: str,
    version: str,
):
    """Canonicalize a sum formula."""
    print(leruli.canonicalizechemicalformula(sumformula, version))


@click.group()
def cli3():
    pass


@cli3.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.argument("smiles")
def canonicalizesmiles(
    smiles: str,
    version: str,
):
    """Canonicalize a SMILES string."""
    print(leruli.canonicalizesmiles(smiles, version))


@click.group()
def cli4():
    pass


@cli4.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.argument("smiles")
def smiles2chemicalformula(
    smiles: str,
    version: str,
):
    """Get the sum formula from SMILES."""
    print(leruli.smiles2chemicalformula(smiles, version))


# @cli2.command()
# @click.option("--charge", type=int, default=0, help="Net charge of the molecule.")
# @click.option(
#     "--multiplicity", type=int, default=1, help="Multiplicity of the molecule."
# )
# @click.option("--version", default="latest", help="Request specific API version.")
# @click.argument("filename", type=click.Path(exists=True))
# @click.argument("level")
# @click.argument("basisset")
# def singlepoint(
#     filename: str,
#     level: str,
#     basisset: str,
#     charge: int,
#     multiplicity: int,
#     version: str,
# ):
#     """Evaluate a geometry with QM methods."""
#     with open(filename) as fh:
#         content = fh.read()
#     leruli.singlepoint_submit(content, level, basisset, charge, multiplicity, version)


cli = click.CommandCollection(sources=[cli1, cli2, cli3, cli4])


def main():
    sys.exit(cli())


if __name__ == "__main__":
    main()
