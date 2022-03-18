"""Console script for leruli."""
import sys
import click
import leruli
import tabulate
import base64
from typing import List

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


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
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("graph")
def graph_to_geometry(graph: str, format: str, reference: str, version: str = None):
    """Molecular geometry from a graph."""
    try:
        result = leruli.graph_to_geometry(graph, format, version)
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)
    if result is None:
        print("Could not find a geometry.")
    else:
        print(result["geometry"])


@click.group()
def cli2():
    pass


@cli2.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("formula")
def canonical_formula(
    formula: str,
    reference: bool,
    version: str,
):
    """Canonicalize a sum formula."""
    result = leruli.canonical_formula(formula, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    print(result["formula"])


@click.group()
def cli5():
    pass


@cli5.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("graph")
def graph_to_formula(
    graph: str,
    reference: bool,
    version: str,
):
    """Obtain a formula from a graph."""
    result = leruli.graph_to_formula(graph, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    print(result["formula"])


@click.group()
def cli20():
    pass


@cli20.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("graph")
def graph_to_boiling_point(
    graph: str,
    reference: bool,
    version: str,
):
    """Estimate a boiling point in deg C."""
    result = leruli.graph_to_boiling_point(graph, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    print(result["bp"])


@click.group()
def cli21():
    pass


@cli21.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("graph")
def graph_to_melting_point(
    graph: str,
    reference: bool,
    version: str,
):
    """Estimate a melting point in deg C."""
    result = leruli.graph_to_melting_point(graph, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    print(result["mp"])


@click.group()
def cli22():
    pass


@cli22.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("graph")
def graph_to_logP(
    graph: str,
    reference: bool,
    version: str,
):
    """Estimate a logP."""
    result = leruli.graph_to_logP(graph, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    print(result["logp"])


@click.group()
def cli23():
    pass


@cli23.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("graph")
def graph_to_logD(
    graph: str,
    reference: bool,
    version: str,
):
    """Estimate a logD."""
    result = leruli.graph_to_logD(graph, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    print(result["logp"])


@click.group()
def cli24():
    pass


@cli24.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("graph")
def graph_to_pKa(
    graph: str,
    reference: bool,
    version: str,
):
    """Estimate a pKa."""
    result = leruli.graph_to_pKa(graph, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    print(result)


@click.group()
def cli3():
    pass


@cli3.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("graph")
def canonical_graph(
    graph: str,
    reference: bool,
    version: str,
):
    """Canonicalize a graph."""
    result = leruli.canonical_graph(graph, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    print(result["graph"])


@click.group()
def cli6():
    pass


@cli6.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("formula")
def formula_to_graphs(
    formula: str,
    reference: bool,
    version: str,
):
    """Find molecular graphs of a given sum formula."""
    result = leruli.formula_to_graphs(formula, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    for molecule in result["molecules"]:
        print(f"{molecule['name']}: {molecule['smiles']}")


@click.group()
def cli7():
    pass


@cli7.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("graph")
def graph_to_name(
    graph: str,
    reference: bool,
    version: str,
):
    """Obtain a name from a graph."""
    result = leruli.graph_to_name(graph, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    print(result["name"])


@click.group()
def cli8():
    pass


@cli8.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("name")
def name_to_graph(
    name: str,
    reference: bool,
    version: str,
):
    """Obtain a graph from a name."""
    result = leruli.name_to_graph(name, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    print(result["graph"])


@click.group()
def cli9():
    pass


@cli9.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("formula")
@click.argument("basisset")
def formula_to_cost(
    formula: str,
    basisset: str,
    reference: bool,
    version: str,
):
    """Obtain a cost estimate for a molecule."""
    result = leruli.formula_to_cost(formula, basisset, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    print(tabulate.tabulate(result["data"], headers="keys"))


@click.group()
def cli10():
    pass


@cli10.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option("--angle", default=0, help="Rotation angle.")
@click.option(
    "--format",
    type=click.Choice("SVG PNG PDF".split(), case_sensitive=False),
    default="SVG",
    help="File format for output, defaults to SVG.",
)
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.argument("graph")
@click.argument("filename")
def graph_to_image(
    filename: str,
    graph: str,
    format: str,
    angle: int,
    reference: bool,
    version: str,
):
    """Structure formula as image file."""
    result = leruli.graph_to_image(graph, format, angle, version)
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )
    with open(filename, "wb") as fh:
        fh.write(base64.b64decode(result["image"]))


@click.group()
def cli11():
    pass


@cli11.command()
@click.option("--version", default="latest", help="Request specific API version.")
@click.option(
    "--reference", is_flag=True, default=False, help="Print references for the result."
)
@click.option("--quiet", is_flag=True, default=False, help="Hide progress bar.")
@click.argument("graph")
@click.argument("solvent")
@click.argument("temperatures")
def graph_to_solvation_energy(
    graph: str,
    solvent: str,
    temperatures: str,
    reference: bool,
    version: str,
    quiet: bool,
):
    """Estimate the free energy of solvation."""
    temperatures = [float(_) for _ in temperatures.split(",")]
    result = leruli.graph_to_solvation_energy(
        graph, solvent, temperatures, version, progress=not quiet
    )
    if reference:
        print(
            f"# Reference as BibTeX: https://api.leruli.com/{version}/references/{result['reference']}/bibtex"
        )

    if "detail" in result:
        print(f"ERROR: {result['detail']['ERROR']}")
    else:
        printable = [
            {"Temperature [K]": k, "Energy of solvation [kcal/mol]": v}
            for k, v in result["solvation_energies"].items()
        ]
        print(tabulate.tabulate(printable, headers="keys"))


@click.group()
def group_task_submit():
    pass


@group_task_submit.command()
@click.option("--memory", default=4000, help="Memory limit in MB.")
@click.option("--time", default=60 * 24, help="Time limit in minutes.")
@click.option("--cores", default=1, help="Number of cores to allocate.")
@click.argument("code")
@click.argument("version")
@click.argument("command", nargs=-1, required=True)
def task_submit(
    memory: int, time: int, cores: int, code: str, version: str, command: str
):
    """Submit a job to the Leruli queue. This is a paid feature requiring an API secret, which can be obtained from info@leruli.com."""

    try:
        jobid = leruli.task_submit(
            ".", code, version, command, cores, memory, time * 60
        )
    except ValueError as e:
        print(f"Not submitted: {str(e)}")
        sys.exit(1)
    if jobid is not None:
        print(jobid)
    else:
        sys.exit(1)


@click.group()
def group_task_status():
    pass


@group_task_status.command()
@click.argument("jobid", required=False)
def task_status(jobid: str):
    """Get the status of a job in the queue."""
    if jobid is None:
        with open("leruli.job") as fh:
            jobid = fh.read().strip()
    status = leruli.task_status(jobid)
    if status is None:
        sys.exit(1)
    if status["reason"] is None:
        print(status["status"])
    else:
        print(status["status"] + ": " + status["reason"])


@click.group()
def group_task_get():
    pass


@group_task_get.command()
@click.argument("bucket", required=False)
def task_get(bucket: str):
    """Get the status of a job in the queue."""
    if bucket is None:
        with open("leruli.bucket") as fh:
            bucket = fh.read().strip()
    leruli.task_get(".", bucket)


@click.group()
def group_task_cancel():
    pass


@group_task_cancel.command()
@click.argument("jobid", required=False)
def task_cancel(jobid: str):
    """Cancels a job in the queue."""
    if jobid is None:
        with open("leruli.job") as fh:
            jobid = fh.read().strip()
    status = leruli.task_cancel(jobid)
    print(status)


@click.group()
def group_task_prune():
    pass


@group_task_prune.command()
@click.argument("bucket", required=False)
def task_prune(bucket: str):
    """Deletes the input/output files of a bucket."""
    if bucket is None:
        with open("leruli.bucket") as fh:
            bucket = fh.read().strip()
    try:
        leruli.task_prune(bucket)
    except:
        print("Pruning failed. Bucket already pruned or wrong S3 credentials.")
        sys.exit(1)


@click.group()
def group_task_publish_code():
    pass


@group_task_publish_code.command()
@click.argument("code")
@click.argument("version")
def task_publish_code(code: str, version: str):
    """Uploads a local docker image to the queue."""
    leruli.task_publish_code()


cli = click.CommandCollection(
    sources=[
        cli1,
        cli2,
        cli3,
        cli20,
        cli21,
        cli22,
        cli23,
        cli24,
        cli5,
        cli6,
        cli7,
        cli8,
        cli9,
        cli10,
        cli11,
        group_task_submit,
        group_task_status,
        # group_task_cancel,
        group_task_publish_code,
        group_task_prune,
        group_task_get,
    ],
    context_settings=CONTEXT_SETTINGS,
)


def main():
    sys.exit(cli())


if __name__ == "__main__":
    main()
