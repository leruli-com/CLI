import urllib
import requests as rq

BASEURL = "https://api.leruli.com"


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
        print(res.json())
        param = msg["loc"][-1]
        detail = msg["msg"]
        raise ValueError(f"{param}: {detail}")
