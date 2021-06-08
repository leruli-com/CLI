import urllib
import requests as rq
import os

BASEURL = os.getenv("LERULI_BASEURL", "https://api.leruli.com")


def quickgeometry(smiles: str, format: str = "XYZ", version: str = None) -> str:
    """Returns an approximate 3D geometry from a given SMILES. Supported formats: SDF, PDB and XYZ. Works on molecules up to 60 heavy atoms."""
    if version is None:
        version = "latest"
    smiles = urllib.parse.quote(smiles)
    res = rq.get(f"{BASEURL}/{version}/quickgeometry/{format}/{smiles}")
    if res.status_code == 200:
        return res.content.decode("ascii")
    if res.status_code == 204:
        raise NotImplementedError("Unable to obtain geometry.")
    if res.status_code == 413:
        msg = res.json()["detail"]
        raise ValueError(f"{msg}")
    if res.status_code == 422:
        msg = res.json()["detail"][0]
        param = msg["loc"][-1]
        detail = msg["msg"]
        raise ValueError(f"{param}: {detail}")
    raise NotImplementedError("Unknown status code. Please update the python package.")


def singlepoint_submit(
    filecontents: str,
    level: str,
    basisset: str,
    charge: int = 0,
    multiplicity: int = 1,
    version: str = None,
):
    """Runs a single point calculation on a fixed geometry, specified as file.
    Returns a token and an estimate in seconds how long this probably will take. The result can be obtained from singlepoint_retrieve() using the token."""
    level = urllib.parse.quote(level)
    basisset = urllib.parse.quote(basisset)
    res = rq.post(
        f"{BASEURL}/{version}/singlepoint/{level}/{basisset}/{charge}/{multiplicity}",
        files={"file": filecontents},
    )
    print(res.content)


def canonicalizechemicalformula(sumformula: str, version: str = None) -> str:
    if version is None:
        version = "latest"
    res = rq.get(f"{BASEURL}/{version}/canonicalizechemicalformula/{sumformula}")
    if res.status_code == 200:
        return res.json()["chemicalformula"]
    if res.status_code == 422:
        msg = res.json()["detail"]
        raise ValueError(msg)
    raise NotImplementedError("Unknown status code. Please update the python package.")


def canonicalizesmiles(smiles: str, version: str = None) -> str:
    if version is None:
        version = "latest"
    smiles = urllib.parse.quote(smiles)
    res = rq.get(f"{BASEURL}/{version}/canonicalizesmiles/{smiles}")
    if res.status_code == 200:
        return res.json()["smiles"]
    if res.status_code == 422:
        msg = res.json()["detail"]
        raise ValueError(msg)
    raise NotImplementedError("Unknown status code. Please update the python package.")


def smiles2chemicalformula(smiles: str, version: str = None) -> str:
    if version is None:
        version = "latest"
    smiles = urllib.parse.quote(smiles)
    res = rq.get(f"{BASEURL}/{version}/smiles2chemicalformula/{smiles}")
    if res.status_code == 200:
        return res.json()["chemicalformula"]
    if res.status_code == 422:
        msg = res.json()["detail"]
        raise ValueError(msg)
    raise NotImplementedError("Unknown status code. Please update the python package.")
