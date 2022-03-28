from typing import Dict
import os
import requests as rq
import tqdm
from minio import Minio
import time

BASEURL = os.getenv("LERULI_BASEURL", "https://api.leruli.com")
SORRY = "ERROR: Accessing API failed. This is our fault, not yours. Please accept our apologies. We have been notified of this error."


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


class LeruliInternalError(Exception):
    pass


def _base_call(
    endpoint: str,
    payload: Dict,
    version: str,
    urgent: bool = False,
    progress: bool = False,
    files: Dict = {},
):
    """Common code to deal with the delayed responses as they can come from the API."""
    try:
        url = f"{BASEURL}/{version}/{endpoint}"
        if urgent is True:
            url = f"{url}?urgent={urgent}"
        res = rq.post(url, json=payload, files=files)

        pbar = None
        # wait for delayed responses
        if res.status_code == 202:
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
            if str(res.status_code).startswith("5"):
                print(SORRY)
                raise LeruliInternalError()
            res = res.json()
        else:
            # Internal error?
            if str(res.status_code).startswith("5"):
                print(SORRY)
                raise LeruliInternalError()

            # No content?
            if res.status_code == 204:
                return None
            res = res.json()
        return res
    except:
        print(SORRY)
        raise LeruliInternalError()


def get_api_secret():
    """Fetches the current API secret from environment variables."""
    if not "LERULI_API_SECRET" in os.environ:
        print(
            "This feature is paid. Please contact info@leruli.com to obtain an API secret."
        )
        return None
    return os.getenv("LERULI_API_SECRET")


def get_group_token():
    """Fetches the current group token."""
    api_secret = get_api_secret()
    if api_secret is None:
        return None

    return _base_call("group-token", payload={"secret": api_secret}, version="latest")


def get_s3_client():
    """Builds a S3 client object from environment variables."""
    if not (
        "LERULI_S3_ACCESS" in os.environ
        and "LERULI_S3_SECRET" in os.environ
        and "LERULI_S3_SERVER" in os.environ
    ):
        print(
            "Please configure the environment variables LERULI_S3_[ACCESS|SECRET|SERVER]."
        )
        return None
    s3_access = os.getenv("LERULI_S3_ACCESS")
    s3_secret = os.getenv("LERULI_S3_SECRET")
    s3_server = os.getenv("LERULI_S3_SERVER")

    s3_client = Minio(
        s3_server.split("/")[-1],
        access_key=s3_access,
        secret_key=s3_secret,
        secure=s3_server.startswith("https"),
    )
    return s3_client
