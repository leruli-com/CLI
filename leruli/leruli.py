import internal
from graph import *
from task import *


def canonical_formula(
    formula: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
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
