from . import internal


def canonical_formula(
    formula: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    """Canonicalizes a chemical (sum) formula.

    The given sum formula may contain bracketed elements, e.g. ``CH3(CH2)4CH3``.

    Parameters
    ----------
    formula : str
        Any chemical sum formula. May contain repeated elements in parentheses.
    version : str, optional
        A specific API version in case you want to enforce backwards compatibility.
    urgent : bool, optional
        Enable to call with priority, might not allow parallel execution.
    progress : bool, optional
        Enable to show interactive progress bar for this blocking call.

    Returns
    -------
    str
        Canonical sum formula in Hill notation.
    """
    payload = {"formula": formula}
    return internal._base_call("canonical-formula", payload, version, urgent, progress)


def canonical_graph(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return internal._base_call("canonical-graph", payload, version, urgent, progress)


def name_to_graph(
    name: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"name": name}
    return internal._base_call("name-to-graph", payload, version, urgent, progress)


def formula_to_graphs(
    formula: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"formula": formula}
    return internal._base_call("formula-to-graphs", payload, version, urgent, progress)


def formula_to_cost(
    formula: str,
    basisset: str,
    version: str = "latest",
    urgent: bool = False,
    progress: bool = False,
):
    payload = {"formula": formula, "basisset": basisset}
    return internal._base_call("formula-to-cost", payload, version, urgent, progress)
