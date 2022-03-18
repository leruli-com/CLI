from . import internal
from typing import List


def graph_to_image(
    graph: str,
    format: str,
    angle: int,
    version: str = "latest",
    urgent: bool = False,
    progress: bool = False,
):
    payload = {"graph": graph, "format": format, "angle": angle}
    return internal._base_call("graph-to-image", payload, version, urgent, progress)


def graph_to_solvation_energy(
    graph: str,
    solventname: str,
    temperatures: List[float],
    version: str = "latest",
    urgent: bool = False,
    progress: bool = False,
):
    payload = {"graph": graph, "solvent": solventname, "temperatures": temperatures}
    return internal._base_call(
        "graph-to-solvation-energy", payload, version, urgent, progress
    )


def graph_to_geometry(
    graph: str,
    format: str,
    version: str = "latest",
    urgent: bool = False,
    progress: bool = False,
):
    """Obtains a 3D geometry for a molecular graph.

    Parameters
    ----------
    graph : str
        SMILES
    format : str
        The requested geometry format: XYZ, SDF, PDB.
    version : str, optional
        Specific version of the API to use, by default "latest"
    urgent : bool, optional
        For interactive use only, by default False
    progress : bool, optional
        Whether to show a progress bar, by default False

    Returns
    -------
    str or None
        String of the file, None if no geometry could be found
    """
    payload = {"graph": graph, "format": format}
    return internal._base_call("graph-to-geometry", payload, version, urgent, progress)


def graph_to_name(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return internal._base_call("graph-to-name", payload, version, urgent, progress)


def graph_to_boiling_point(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return internal._base_call(
        "graph-to-boiling-point", payload, version, urgent, progress
    )


def graph_to_melting_point(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return internal._base_call(
        "graph-to-melting-point", payload, version, urgent, progress
    )


def graph_to_logP(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return internal._base_call("graph-to-logP", payload, version, urgent, progress)


def graph_to_logD(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return internal._base_call("graph-to-logD", payload, version, urgent, progress)


def graph_to_pKa(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return internal._base_call("graph-to-pKa", payload, version, urgent, progress)


def graph_to_formula(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return internal._base_call("graph-to-formula", payload, version, urgent, progress)
