#!/usr/bin/python3
# Developed by Alexander Bersenev from Hackerdom team, bay@hackerdom.ru

"""Removes a snapshot of vm"""

import sys
import time
import os
import traceback
import re

import do_api
from cloud_common import (log_progress, call_unitl_zero_exit, #get_cloud_ip,
                          SSH_OPTS #, SSH_YA_OPTS
                          )

TEAM = int(sys.argv[1])
NAME = sys.argv[2]
IMAGE_VM_NAME = "team%d" % TEAM

def log_stderr(*params):
    print("Team %d:" % TEAM, *params, file=sys.stderr)


def main():
    if not re.fullmatch(r"[0-9a-zA-Z_]{,64}", NAME):
        print("msg: ERR, name validation error")
        return 1

    SNAPSHOT_NAME = IMAGE_VM_NAME + "-" + NAME

    snapshots = do_api.list_snapshots()

    ids = []

    for snapshot in snapshots:
        if snapshot.get("name", "") != SNAPSHOT_NAME:
            continue

        ids.append(int(snapshot["id"]))

    if not ids:
        print("msg:", "no such snapshot")
        return 1

    if len(ids) > 1:
        print("msg:", "internal error: too much snapshots")
        return 1

    snapshot_id = ids[0]

    result = do_api.delete_snapshot(snapshot_id)

    if not result:
        log_stderr("failed to delete snapshot")
        return 1


    # image_state = open("db/team%d/image_deploy_state" % TEAM).read().strip()

    # if image_state == "NOT_STARTED":
    #     print("msg: ERR, vm is not started")
    #     return 1

    # if image_state == "RUNNING":
    #     cloud_ip = get_cloud_ip(TEAM)
    #     if not cloud_ip:
    #         log_stderr("no cloud ip, exiting")
    #         return 1

    #     cmd = ["sudo", "/cloud/scripts/remove_snapshot.sh", str(TEAM), NAME]
    #     ret = call_unitl_zero_exit(["ssh"] + SSH_YA_OPTS +
    #                                [cloud_ip] + cmd, redirect_out_to_err=False,
    #                                attempts=1)
    #     if not ret:
    #         log_stderr("remove shapshot failed")
    #         return 1
    return 0

if __name__ == "__main__":
    sys.stdout = os.fdopen(1, 'w', 1)
    print("started: %d" % time.time())
    exitcode = 1
    try:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        exitcode = main()
    except:
        traceback.print_exc()
    print("exit_code: %d" % exitcode)
    print("finished: %d" % time.time())
