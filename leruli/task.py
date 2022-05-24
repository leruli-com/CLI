import aiohttp
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
import tqdm.asyncio
import asyncio
import aiobotocore.session
import multiprocessing as mp
import time


async def _async_object_stage(
    s3_client,
    directory: str,
    code: str,
    version: str,
    command: str,
    cores: int,
    memorymb: int,
    timeseconds: int,
):
    global counter
    global rank

    api_secret = internal.get_api_secret()
    if api_secret is None:
        counter[rank] += 2
        return {"error": "No API token configured", "directory": directory}

    if os.path.exists(f"{directory}/leruli.job"):
        counter[rank] += 2
        return {"error": "Directory already submitted.", "directory": directory}

    # TODO: detect failed S3 interactions
    bucket = str(uuid.uuid4())
    await s3_client.create_bucket(Bucket=bucket)
    counter[rank] += 1

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
    await s3_client.put_object(Bucket=bucket, Key="run.tgz", Body=buffer)

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
        "directory": directory,
    }

    counter[rank] += 1
    return payload


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
    dict[str]
        Keys: directories which could not be submitted, values: reasons for this to happen.
    """

    cases = list(
        zip(directories, codes, versions, commands, cores, memorymb, timeseconds)
    )

    def split(a, n):
        k, m = divmod(len(a), n)
        return (a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))

    # TODO find number of procs
    nprocs = 5
    segments = split(cases, nprocs)

    # assign one id to every worker
    idqueue = mp.Queue()
    [idqueue.put(_) for _ in range(nprocs)]
    progress_counter = mp.Array("i", nprocs, lock=False)

    # Uploading
    with tqdm.tqdm(total=len(cases), desc="Uploading job data") as pbar:
        with mp.Pool(
            nprocs,
            initializer=_task_submit_many_initializer,
            initargs=(idqueue, progress_counter),
        ) as p:
            result = p.map_async(_task_submit_many_toasync, segments)
            while True:
                total = sum([progress_counter[_] for _ in range(nprocs)])
                pbar.n = int(total / 2)
                pbar.refresh()
                try:
                    result.successful()
                except:
                    time.sleep(0.1)
                    continue
                result.wait()
                break

        # prepare for stage 2: submission to bulk API
        failed = {}
        cases = []
        for case in sum(result.get(), []):
            if "error" in case:
                failed[case["directory"]] = case["error"]
            else:
                payload = case.copy()
                del payload["directory"]
                cases.append((payload, case["directory"]))

    results = asyncio.run(_task_submit_many_API_toasync(cases))
    for result in results:
        failed.update(results)
    return failed


async def _task_submit_many_API_toasync(cases):
    # build parallel task list
    async with aiohttp.ClientSession() as session:
        tasks = []
        while len(cases) > 0:
            segment, cases = cases[:50], cases[50:]
            tasks.append(_task_submit_many_API(session, segment))

        # defer for async execution
        result = await tqdm.asyncio.tqdm.gather(*tasks, desc="Submitting job batches")

    return result


def _task_submit_many_toasync(cases):
    return asyncio.run(_task_submit_many_worker(cases))


async def _task_submit_many_API(session, segment):
    failed = {}
    async with session.post(
        f"{internal.BASEURL}/v22_1/bulk/task-submit", json=[_[0] for _ in segment]
    ) as res:
        results = await res.json()
        for case, result in zip(segment, results):
            payload, directory = case

            if result["status"] != 200:
                reason = "Job not accepted"
                if result["status"] == 403:
                    reason = "API key not accepted"
                if result["status"] == 412:
                    reason = "Compute secret not set-up"
                if result["status"] == 422:
                    reason = f"Job not accepted: {str(result)}"
                failed[directory] = reason
                continue

            jobid = result["data"]
            _task_submit_finalize(directory, jobid, payload["bucketid"])
    return failed


async def _task_submit_many_worker(cases):
    session = aiobotocore.session.get_session()
    tasks = []
    async with session.create_client(
        "s3",
        endpoint_url=os.getenv("LERULI_S3_SERVER"),
        aws_secret_access_key=os.getenv("LERULI_S3_SECRET"),
        aws_access_key_id=os.getenv("LERULI_S3_ACCESS"),
    ) as s3_client:
        for args in cases:
            tasks.append(_async_object_stage(s3_client, *args))
        cases = await asyncio.gather(*tasks)

    return cases


def _task_submit_many_initializer(idqueue, progress):
    global rank
    global counter
    rank = idqueue.get()
    counter = progress

    # TODO print missing API key only once, abort immediately


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
        print(f"Failed: {str(e)}")
        return

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
    res = rq.post(f"{internal.BASEURL}/v22_1/task-status", json=payload)
    if res.status_code == 200:
        return res.json()
    if res.status_code == 404:
        raise ValueError("No such job")


def task_get(directory: str, bucket: str):
    """Downloads the input and output files of a Leruli Queue/Cloud task into a directory."""
    s3_client = internal.get_s3_client()
    for obj in s3_client.list_objects(bucket, recursive=True):
        object = obj.object_name
        dirname = os.path.dirname(object)
        if dirname != "":
            os.makedirs(dirname, exist_ok=True)
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
    for chunk in image.save(named=True):
        cache.write(chunk)
    cache.seek(0)
    tgz = gzip.compress(cache.read())
    del cache
    buffer = io.BytesIO(tgz)

    s3_client.put_object(
        f"code-{group}", f"{code}-{version}.tgz", buffer, buffer.getbuffer().nbytes
    )


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
