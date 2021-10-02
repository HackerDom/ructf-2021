#!/usr/bin/env python3
import functools
import re
import sys

import requests
import traceback

from gornilo import CheckRequest, Verdict, Checker, PutRequest, GetRequest

from generators import gen_string, gen_employee, gen_user_agent
from request_pb2 import UserPair, StringList

checker = Checker()


PORT = 9000


REGISTER_URL = "http://{hostname}:{port}/register"
LOGIN_URL = "http://{hostname}:{port}/login"
NEW_EMPLOYEE_URL = "http://{hostname}:{port}/add_employee"
SEARCH_EMPLOYEES_URL = "http://{hostname}:{port}/search_employees?q={query}"
OWNER_VIEW_URL = "http://{hostname}:{port}/owner_view?employee_id={employee_id}"


def get_creds(url_template, hostname, username, password):
    session = requests.Session()
    url = url_template.format(hostname=hostname, port=PORT)
    user = UserPair(username=username, password=password)
    r = session.post(url, headers={'User-Agent': gen_user_agent(), 'Content-Type': 'application/protobuf'}, data=user.SerializeToString())
    r.raise_for_status()
    return session


login = functools.partial(get_creds, LOGIN_URL)
register = functools.partial(get_creds, REGISTER_URL)


def add_new_employee(session, hostname, new_employee):
    url = NEW_EMPLOYEE_URL.format(hostname=hostname, port=PORT)
    r = session.post(url, headers={'User-Agent': gen_user_agent(), 'Content-Type': 'application/protobuf'}, data=new_employee.SerializeToString())
    r.raise_for_status()
    return r.content.decode()


def list_employee(session, hostname):
    url = SEARCH_EMPLOYEES_URL.format(hostname=hostname, port=PORT, query='new_employee')
    r = session.get(url, headers={'User-Agent': gen_user_agent()})
    r.raise_for_status()
    employee_ids = StringList()
    employee_ids.ParseFromString(r.content)
    return employee_ids.strings


flag_pattern = re.compile('<label><b>Bank card number:</b>(.+)</label>')


def get_flag_from_full_info(content):
    res = flag_pattern.findall(content)
    return res[0].strip() if res[0] else None


def get_flag_from_employee_id_as_owner(session, hostname, employee_id):
    url = OWNER_VIEW_URL.format(hostname=hostname, port=PORT, employee_id=employee_id)
    r = session.get(url, headers={'User-Agent': gen_user_agent()})
    r.raise_for_status()
    return get_flag_from_full_info(r.content.decode())


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
            traceback.print_tb(exc_traceback, file=sys.stdout)
        return True


@checker.define_check
def check_service(request: CheckRequest) -> Verdict:
    return Verdict.OK()


@checker.define_put(vuln_num=1, vuln_rate=1)
def put_flag(request: PutRequest) -> Verdict:
    with NetworkChecker() as nc:
        username, password = gen_string(), gen_string()
        session = register(request.hostname, username, password)
        new_employee_id = add_new_employee(session, request.hostname, gen_employee(request.flag))
        flag_id = f"{username}:{password}:{new_employee_id}"

        nc.verdict = Verdict.OK(flag_id)
    return nc.verdict


@checker.define_get(vuln_num=1)
def get_flag(request: GetRequest) -> Verdict:
    with NetworkChecker() as nc:
        username, password, new_employee_id = request.flag_id.strip().split(":")
        session = login(request.hostname, username, password)
        employee_ids = set(list_employee(session, request.hostname))

        if new_employee_id not in employee_ids:
            return Verdict.MUMBLE("Can not search employee")

        real_flag = get_flag_from_employee_id_as_owner(session, request.hostname, new_employee_id)
        if request.flag != real_flag:
            print(f"Different flags, expected: {request.flag}, real: {real_flag}")
            return Verdict.CORRUPT("Corrupt flag")
        nc.verdict = Verdict.OK()
    return nc.verdict


if __name__ == '__main__':
    checker.run()
