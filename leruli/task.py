from . import internal
import os
import io
import tarfile
import gzip
import docker
import requests as rq
import uuid
from typing import List, Iterable
import tqdm


def task_submit_many(
    directories: Iterable[str],
    codes: Iterable[str],
    versions: Iterable[str],
    commands: Iterable[str],
    cores: Iterable[int],
    memorymb: Iterable[int],
    timeseconds: Iterable[int],
) -> List[str]:
    """Submits many calculations to Leruli Queue/Cloud at once.

    Parameters
    ----------
    directories : Iterable[str]
        Paths to directories, either absolute or relative.
    codes : Iterable[str]
        Codes to run. Needs to be of same length as `directories`.
    versions : Iterable[str]
        Code versions to use. Needs to be of same length as `directories`.
    commands : Iterable[str]
        Commands to execute. Needs to be of same length as `directories`.
    cores : Iterable[int]
        Cores to use. Needs to be of same length as `directories`.
    memorymb : Iterable[int]
        Memory to use in MB. Needs to be of same length as `directories`.
    timeseconds : Iterable[int]
        Time limit for jobs in seconds. Needs to be of same length as `directories`.

    Returns
    -------
    list[str]
        A list of those directories which could not be submitted, e.g. due to missing permissions.
    """

    def do_cases(cases):
        failed = []
        if len(cases) == 0:
            return failed
        res = rq.post(
            f"{internal.BASEURL}/v22_1/bulk/task-submit", json=[_[0] for _ in cases]
        )
        results = res.json()
        for case, result in zip(cases, results):
            payload, directory = case

            if result["status"] != 200:
                failed.append(directory)
                continue

            jobid = result["data"]
            _task_submit_finalize(directory, jobid, payload["bucketid"])
        return failed

    cases = []
    failed = []
    directories = list(directories)
    for args in tqdm.tqdm(
        zip(directories, codes, versions, commands, cores, memorymb, timeseconds),
        total=len(directories),
    ):
        try:
            payload = _task_submit_payload(*args)
        except ValueError as e:
            failed.append(args[0])
            continue
        directory = args[0]
        cases.append((payload, directory))

        if len(cases) == 50:
            failed += do_cases(cases)
            cases = []

    failed += do_cases(cases)

    return failed


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
    try:
        payload = _task_submit_payload(
            directory, code, version, command, cores, memorymb, timeseconds
        )
    except ValueError as e:
        print (f"Failed: {str(e)}")

    res = rq.post(f"{internal.BASEURL}/v22_1/task-submit", json=payload)
    if res.status_code != 200:
        print("Cannot submit jobs. Please check the input.")
        return
    jobid = res.json()

    _task_submit_finalize(directory, jobid, payload["bucketid"])


def _task_submit_payload(
    directory: str,
    code: str,
    version: str,
    command: str,
    cores: int,
    memorymb: int,
    timeseconds: int,
):
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
        tar.add(directory, arcname=os.path.basename("."))

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
    return payload


def _task_submit_finalize(directory, jobid, bucket):
    # local handle
    with open(f"{directory}/leruli.job", "w") as fh:
        fh.write(f"{jobid}\n")
    with open(f"{directory}/leruli.bucket", "w") as fh:
        fh.write(f"{bucket}\n")
    return jobid


def task_status(jobid: str):
    """Queries the status of a job at Leruli Queue/Cloud."""
    api_secret = internal.get_api_secret()
    if api_secret is None:
        return

    payload = {
        "secret": api_secret,
        "jobid": jobid,
    }
    status = rq.post(f"{internal.BASEURL}/v22_1/task-status", json=payload).json()
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
    if api_secret is None:
        return

    payload = {
        "secret": api_secret,
        "jobid": jobid,
    }
    status = rq.post(f"{internal.BASEURL}/v22_1/task-cancel", json=payload)
    return status.json()


def task_publish_code(code: str, version: str):
    """Uploads a local docker image to use with Leruli Queue/Cloud."""
    api_secret = internal.get_api_secret()
    if api_secret is None:
        return
    s3_client = internal.get_s3_client()
    group = internal.get_group_token()

    client = docker.from_env()
    image = client.images.get(f"{code}:{version}")
    cache = io.BytesIO()
    for chunk in image.save():
        cache.write(chunk)
    cache.seek(0)
    tgz = gzip.compress(cache.read())

    s3_client.fput(f"code-{group}", f"{code}-{version}.tgz", tgz, len(tgz))


def task_list_codes():
    """Lists codes available to your account on Leruli Queue/Cloud.

    Returns
    -------
    list[tuple[str, str]]
        Code name and version tuples.
    """
    api_secret = internal.get_api_secret()
    if api_secret is None:
        return []

    s3_client = internal.get_s3_client()
    group = internal.get_group_token()
    objects = s3_client.list_objects(f"code-{group}")
    codes = []
    for obj in objects:
        filename = obj.object_name
        if not filename.endswith(".tgz"):
            continue
        basename = filename[:-4]
        code, version = basename.rsplit("-", 1)
        codes.append((code, version))
    return codes


def task_prune(bucket: str):
    """Irreversibly deletes the Leruli Queue/Cloud store of input and output files."""
    s3_client = internal.get_s3_client()
    for obj in s3_client.list_objects(bucket, recursive=True):
        s3_client.remove_object(bucket, obj.object_name)
    s3_client.remove_bucket(bucket)
