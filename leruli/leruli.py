from typing import Dict, List
import urllib
import requests as rq
import time
import os
import tqdm
import sys

# import tqdm

BASEURL = os.getenv("LERULI_BASEURL", "https://api.leruli.com")
SORRY = "ERROR: Accessing API failed. This is our fault, not yours. Please accept our apologies. We have been notified of this error."


def _base_call(
    endpoint: str,
    payload: Dict,
    version: str,
    urgent: bool,
    progress: bool,
    files: Dict = {},
):
    try:
        res = rq.post(
            f"{BASEURL}/{version}/{endpoint}?urgent={urgent}", json=payload, files=files
        )

        pbar = None
        # wait for delayed responses
        if res.status_code == 202:
            starttime = time.time()
            while True:
                res = res.json()
                token = res["token"]
                remainder = res["time_to_result"]

                if progress:
                    if pbar is None:
                        pbar = tqdm.tqdm(
                            total=remainder,
                            desc="Waiting",
                            bar_format="{desc}: |{bar}| [{elapsed}<{remaining}]",
                        )
                    else:
                        pbar.total = remainder + pbar.n
                        pbar.update(0)

                early = remainder - 3
                while remainder > 0 and remainder > early:
                    tosleep = min(remainder, 1)
                    time.sleep(tosleep)
                    remainder -= 1
                    if progress:
                        pbar.update(tosleep)

                res = rq.get(
                    f"{BASEURL}/{version}/result/{token}",
                )
                if res.status_code != 202:
                    if progress:
                        pbar.total = pbar.n
                        pbar.update(0)
                        pbar.close()
                    break
                # time.sleep(res.json()["time_to_result"])
            if str(res.status_code).startswith("5"):
                print(SORRY)
                sys.exit(1)
            res = res.json()
        else:
            if str(res.status_code).startswith("5"):
                print(SORRY)
                sys.exit(1)
            res = res.json()

        return res
    except:
        raise
        print(SORRY)
        sys.exit(1)


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


def graph_to_solvation_energy(
    graph: str,
    solventname: str,
    temperatures: List[float],
    version: str = "latest",
    urgent: bool = False,
    progress: bool = False,
):
    payload = {"graph": graph, "solvent": solventname, "temperatures": temperatures}
    return _base_call("graph-to-solvation-energy", payload, version, urgent, progress)


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


# def image_to_graph(
#     image: bytes, version: str = "latest", urgent: bool = False, progress: bool = False
# ):
#     return _base_call(
#         "image-to-graph",
#         {},
#         version,
#         urgent,
#         progress,
#         {"file": ("image", image, "image/png")},
#     )


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
