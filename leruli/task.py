from sys import intern
from . import internal
import os
import io
import tarfile
import gzip
import docker
import requests as rq
import uuid


def task_submit(
    directory: str,
    code: str,
    version: str,
    command: str,
    cores: int = 1,
    memorymb: int = 4000,
    timeseconds: int = 24 * 60 * 60,
):
    """Submits a given directory content as job to Leruli Queue/Cloud."""
    api_secret = internal.get_api_secret()
    if api_secret is None:
        return
    s3_client = internal.get_s3_client()
    if s3_client is None:
        return

    if os.path.exists(f"{directory}/leruli.job"):
        raise ValueError("Directory already submitted.")

    bucket = str(uuid.uuid4())
    s3_client.make_bucket(bucket)

    # in-memory tar file
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        tar.add(".", arcname=os.path.basename("."))

        runscript = io.BytesIO(("#!/bin/bash\n" + " ".join(command)).encode("ascii"))
        tarinfo = tarfile.TarInfo(name="run.sh")
        tarinfo.size = runscript.getbuffer().nbytes
        tar.addfile(tarinfo=tarinfo, fileobj=runscript)
    buffer.seek(0)

    # upload
    s3_client.put_object(bucket, "run.tgz", buffer, buffer.getbuffer().nbytes)

    # submit to API
    codeversion = f"{code}:{version}"
    payload = {
        "secret": api_secret,
        "bucketid": bucket,
        "name": "default",
        "codeversion": codeversion,
        "cores": cores,
        "memorymb": memorymb,
        "timelimit": timeseconds,
    }
    res = rq.post(f"{internal.BASEURL}/v22_1/task-submit", json=payload)
    if res.status_code != 200:
        print("Cannot submit jobs. Please check the input.")
        return
    jobid = res.json()

    # local handle
    with open(f"{directory}/leruli.job", "w") as fh:
        fh.write(f"{jobid}\n")
    with open(f"{directory}/leruli.bucket", "w") as fh:
        fh.write(f"{bucket}\n")
    return jobid


def task_status(jobid: str):
    """Queries the status of a job at Leruli Queue/Cloud."""
    api_secret = internal.get_api_secret()

    payload = {
        "secret": api_secret,
        "jobid": jobid,
    }
    status = rq.post(f"{internal.BASEURL}/v22_1/task-status", json=payload).json()
    if type(status) == list:
        return ": ".join(status.json())
    return status


def task_get(directory: str, bucket: str):
    """Downloads the input and output files of a Leruli Queue/Cloud task into a directory."""
    s3_client = internal.get_s3_client()
    for obj in s3_client.list_objects(bucket):
        object = obj.object_name
        try:
            response = s3_client.get_object(bucket, object)
            content = response.read()
        finally:
            response.close()
            response.release_conn()
        with open(f"{directory}/{object}", "wb") as fh:
            fh.write(content)


def task_cancel(jobid: str):
    """Cancels a task on Leruli Queue/Cloud."""
    api_secret = internal.get_api_secret()
    payload = {
        "secret": api_secret,
        "jobid": jobid,
    }
    status = rq.post(f"{internal.BASEURL}/v22_1/task-cancel", json=payload)
    return status.json()


def task_publish_code(code: str, version: str):
    """Uploads a local docker image to use with Leruli Queue/Cloud."""
    s3_client = internal.get_s3_client()
    api_secret = internal.get_api_secret()

    client = docker.from_env()
    image = client.images.get(f"{code}:{version}")
    cache = io.BytesIO()
    for chunk in image.save():
        cache.write(chunk)
    cache.seek(0)
    tgz = gzip.compress(cache.read())

    s3_client.fput(f"code-{api_secret}", f"{code}-{version}.tgz", tgz, len(tgz))


def task_prune(bucket: str):
    """Irreversibly deletes the Leruli Queue/Cloud store of input and output files."""
    s3_client = internal.get_s3_client()

    for obj in s3_client.list_objects(bucket, recursive=True):
        s3_client.remove_object(bucket, obj.object_name)
    s3_client.remove_bucket(bucket)
