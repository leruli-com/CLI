from typing import Dict
import urllib
import requests as rq
import time
import os
import tqdm

__all__ = "quickgeometry canonicalizechemicalformula canonicalizesmiles smiles2chemicalformula".split()

BASEURL = os.getenv("LERULI_BASEURL", "https://api.leruli.com")


def _base_call(
    endpoint: str,
    payload: Dict,
    version: str,
    urgent: bool,
    progress: bool,
    files: Dict = {},
):
    # entry = time.time()
    res = rq.post(
        f"{BASEURL}/{version}/{endpoint}?urgent={urgent}", json=payload, files=files
    )
    print(res.content)

    # wait for delayed responses
    if res.status_code == 202:
        res = res.json()
        remainder = res["time_to_result"]
        # now = time.time()
        time.sleep(remainder)
        # pbar = tqdm.tqdm(
        #     total=remainder + (now - entry),
        #     desc="Waiting",
        #     bar_format="{desc}: |{bar}| [{elapsed}<{remaining}]",
        # )
        # pbar.update(now - entry)
        # while remainder > 0:
        #     tosleep = min(remainder, 1)
        #     time.sleep(tosleep)
        #     remainder -= 1
        #     pbar.update(tosleep)
        # pbar.close()

        token = res["token"]
        while True:
            res = rq.post(
                f"{BASEURL}/{version}/get-results",
                json={"tokens": [{"token": token}]},
            )
            if res.status_code != 202:
                break
            time.sleep(res.json()[0]["time_to_result"])
        res = res.json()[0]
    else:
        res = res.json()

    return res


def canonical_formula(
    formula: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"formula": formula}
    return _base_call("canonical-formula", payload, version, urgent, progress)


def canonical_graph(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return _base_call("canonical-graph", payload, version, urgent, progress)


def graph_to_boiling_point(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return _base_call("graph-to-boiling-point", payload, version, urgent, progress)


def graph_to_melting_point(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return _base_call("graph-to-melting-point", payload, version, urgent, progress)


def graph_to_logP(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return _base_call("graph-to-logP", payload, version, urgent, progress)


def graph_to_logD(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return _base_call("graph-to-logD", payload, version, urgent, progress)


def graph_to_pKa(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return _base_call("graph-to-pKa", payload, version, urgent, progress)


def graph_to_formula(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return _base_call("graph-to-formula", payload, version, urgent, progress)


def graph_to_geometry(
    graph: str,
    format: str,
    version: str = "latest",
    urgent: bool = False,
    progress: bool = False,
):
    payload = {"graph": graph, "format": format}
    return _base_call("graph-to-geometry", payload, version, urgent, progress)


def formula_to_graphs(
    formula: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"formula": formula}
    return _base_call("formula-to-graphs", payload, version, urgent, progress)


def graph_to_name(
    graph: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"graph": graph}
    return _base_call("graph-to-name", payload, version, urgent, progress)


def name_to_graph(
    name: str, version: str = "latest", urgent: bool = False, progress: bool = False
):
    payload = {"name": name}
    return _base_call("name-to-graph", payload, version, urgent, progress)


def formula_to_cost(
    formula: str,
    basisset: str,
    version: str = "latest",
    urgent: bool = False,
    progress: bool = False,
):
    payload = {"formula": formula, "basisset": basisset}
    return _base_call("formula-to-cost", payload, version, urgent, progress)


def graph_to_image(
    graph: str,
    format: str,
    angle: int,
    version: str = "latest",
    urgent: bool = False,
    progress: bool = False,
):
    payload = {"graph": graph, "format": format, "angle": angle}
    return _base_call("graph-to-image", payload, version, urgent, progress)


def image_to_graph(
    image: bytes, version: str = "latest", urgent: bool = False, progress: bool = False
):
    return _base_call(
        "image-to-graph",
        {},
        version,
        urgent,
        progress,
        {"file": ("image", image, "image/png")},
    )


# image_to_graph


def _extract_error_message(res):
    try:
        msg = res.json()["detail"]
        return msg
    except:
        pass
    try:
        msg = res.json()["detail"][0]
        param = msg["loc"][-1]
        msg = f"Parameter {param}: {msg['msg']}"
        return msg
    except:
        pass
    raise NotImplementedError()
