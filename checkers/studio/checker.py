#!/usr/bin/env python3
import sys
import requests
import time

from traceback import print_exc, print_tb
from user_agent_randomizer import get as get_user_agent
from payload_generator import get as get_payload
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from gornilo import \
    GetRequest, \
    CheckRequest, \
    PutRequest, \
    Checker, \
    Verdict


def requests_with_retry(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(400, 404, 500, 502),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    return session


checker = Checker()

TCP_PORT = 8000
GET_RETRIES_COUNT = 15
GET_RETRY_DELAY = 2


class NetworkChecker:
    def __init__(self):
        self.verdict = Verdict.OK()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type in {requests.exceptions.ConnectionError, ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError}:
            self.verdict = Verdict.DOWN("Service is down")
        if exc_type in {requests.exceptions.HTTPError}:
            self.verdict = Verdict.MUMBLE(f"Incorrect http code")

        if exc_type:
            print(exc_type)
            print(exc_value.__dict__)
            print_tb(exc_traceback, file=sys.stdout)
        return True


@checker.define_check
def check(check_request: CheckRequest) -> Verdict:
    return Verdict.OK()


@checker.define_put(vuln_num=1, vuln_rate=1)
def put(put_request: PutRequest) -> Verdict:
    request_data = get_payload(put_request.flag)
    with NetworkChecker() as nc:
        resp = requests_with_retry().put(
            f"http://{put_request.hostname}:{TCP_PORT}/api/v1/jobs",
            headers={"User-Agent": get_user_agent()},
            data=request_data
        )
        if resp is None:
            return Verdict.CORRUPT("corrupt response")

        resp_json = resp.json()
        if "data" not in resp_json or "id" not in resp_json["data"]:
            nc.verdict = Verdict.CORRUPT("corrupt response")
        else:
            nc.verdict = Verdict.OK(resp_json["data"]["id"])

    return nc.verdict


@checker.define_get(vuln_num=1)
def get(get_request: GetRequest) -> Verdict:
    try:
        retry_count = 0
        while retry_count <= GET_RETRIES_COUNT:
            # result is not immediate, wait a little bit
            time.sleep(GET_RETRY_DELAY)

            resp = requests_with_retry().get(
                f"http://{get_request.hostname}:{TCP_PORT}/api/v1/jobs/{get_request.flag_id.strip()}",
                headers={"User-Agent": get_user_agent()},
                timeout=3
            )

            if resp is None:
                return Verdict.CORRUPT("corrupt response")

            resp_json = resp.json()
            if "data" not in resp_json or "status" not in resp_json["data"]:
                return Verdict.CORRUPT("corrupt response")

            if resp_json["data"]["status"] == "created":
                retry_count += 1
                continue

            if resp_json["data"]["status"] != "success":
                return Verdict.CORRUPT("u re sending corrupt data")

            if resp_json["data"]["result"] == get_request.flag:
                return Verdict.OK()

            return Verdict.CORRUPT("flag mismatch")

    except Timeout as e:
        print(e, print_exc())
        return Verdict.DOWN("service seems not responding")
    except Exception as e:
        print(e, print_exc())
        return Verdict.CORRUPT("service can't give a flag")


if __name__ == "__main__":
    checker.run()
