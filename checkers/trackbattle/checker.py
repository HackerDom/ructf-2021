#!/usr/bin/env python3
import requests
import socket
import random
import time
import uuid
import string
import hashlib
import json
from traceback import print_exc
import logging
import contextlib

from http.client import HTTPConnection
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from gornilo import \
    GetRequest, \
    CheckRequest, \
    PutRequest, \
    Checker, \
    Verdict

from user_agent_randomizer import get_random_user_agent

HTTPConnection.debuglevel = 1
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger("requests.packages.urllib3")
log.setLevel(logging.DEBUG)
log.propagate = True

checker = Checker()

TB_API_PORT = 8080
TB_AUTH_HEADER = 'XTBAuth'


def get_sha256(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def get_session_with_retry(
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


@checker.define_put(vuln_num=1, vuln_rate=1)
def put(put_request: PutRequest) -> Verdict:
    try:
        nickname = 'user-' + str(uuid.uuid4())
        password = str(uuid.uuid4())
        password_sha256 = get_sha256(password)

        log.debug(f'creating user {nickname} with password {password} ({password_sha256})')

        response = get_session_with_retry().post(
            f"http://{put_request.hostname}:{TB_API_PORT}/api/users",
            headers={"User-Agent": get_random_user_agent()},
            json={
                "nickname": nickname,
                "password_sha256": password_sha256,
                "flag": put_request.flag
            },
        )

        log.debug(f'response: \ncode: {response.status_code}\nheaders:{response.headers}\ntext:{response.text}')

        if response.status_code != 200:
            log.error(f'unexpected code - {response.status_code}')
            return Verdict.MUMBLE('unexpected http code from service')

        response_json = response.json()
        auth_token = response_json['auth_token']
        log.debug(f'user created with auth_token {response.json()}')

        if response.headers[TB_AUTH_HEADER] != auth_token:
            return Verdict.MUMBLE('wrong headers from server')

        return Verdict.OK(auth_token)
    except Exception as e:
        log.error(f'{e}, {print_exc()}')
        return Verdict.DOWN("can't create user")


@checker.define_get(vuln_num=1)
def get(get_request: GetRequest) -> Verdict:
    try:
        response = get_session_with_retry().get(
            f"http://{get_request.hostname}:{TB_API_PORT}/api/users",
            headers={"User-Agent": get_random_user_agent(), TB_AUTH_HEADER: get_request.flag_id},
            timeout=3
        )

        log.debug(f'response: \ncode: {response.status_code}\nheaders:{response.headers}\ntext:{response.text}')

        if response.json()['flag'] == get_request.flag:
            return Verdict.OK()
        else:
            return Verdict.CORRUPT('wrong flag')
    except Timeout as e:
        log.error(f'{e}, {print_exc()}')
        return Verdict.DOWN("service not responding")
    except Exception as e:
        log.error(f'{e}, {print_exc()}')
        return Verdict.CORRUPT("service can't give a flag")


@checker.define_check
def check(check_request: CheckRequest) -> Verdict:
    return Verdict.OK()


if __name__ == "__main__":
    checker.run()
