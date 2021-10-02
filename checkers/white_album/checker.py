#!/usr/bin/env python3.7

from client import *

from gornilo import CheckRequest, Verdict, Checker, PutRequest, GetRequest

checker = Checker()

class DataException(Exception):
    def __init__(self, verdict=None):
        self.verdict = verdict  # you could add more args

    def __str__(self):
        return str(self.verdict)



def compare(first, second):
    first_dump = json.dumps(first, sort_keys=True, indent=2)
    second_dump = json.dumps(second, sort_keys=True, indent=2)
    return first_dump == second_dump


@checker.define_check
async def check_service(request: CheckRequest) -> Verdict:
    try:
        user_id = str(uuid.uuid4())

        client = WBClient(None, request.hostname, 1234)
        client.CreateUser(utils.get_author_name(), user_id)
        meta = {"author":utils.get_author_name(), "description": utils.get_description()}

        album = {
            "id": {"id": str(uuid.uuid4())},
            "name": utils.get_album_name(),
            "meta": meta,
        }

        single_first = {
            "id": {"id": str(uuid.uuid4())},
            "name": utils.single_name(),
            "meta": meta,
            "owner": {"id": user_id},
            "track": {"tokens": [utils.get_track(), utils.get_track()]}
        }

        single_second= {
            "id": {"id": str(uuid.uuid4())},
            "name": utils.single_name(),
            "meta": meta,
            "owner": {"id": user_id},
            "track": {"tokens": [utils.get_track(), utils.get_track()]}
        }
        single_response = client.CreateSingle(single_first).Get()
        single_response.pop('signature')
        if not compare(single_response, single_first):
            return Verdict.MUMBLE(f"Get incorrect single {json.dumps(single_response)}, expected {single_first}")

        single_response2 = client.CreateSingle(single_second).Get()
        single_response2.pop('signature')
        if not compare(single_response2, single_second):
            return Verdict.MUMBLE(f"Get incorrect single {json.dumps(single_response2)}, expected {single_first}")

        album_client = client.CreateAlbum(album)
        album_response = album_client.Get()
        album_client.AttachSingle(single_response["id"])
        album_client.AttachSingle(single_response2["id"])

        album_response.pop("owner")
        album_response.pop("signature")
        album_response.pop("singles") #TODO: check

        if not compare(album_response, album):
            return Verdict.MUMBLE(f"Get incorrect album {json.dumps(album_response)}, expected {album}")

        all_singles = album_client.GetAllSingles()

        for single in all_singles:
            single.pop("signature")

        if not compare(album_response, album):
            return Verdict.MUMBLE(f"Incorrect singles {json.dumps([single_first, single_second])}, expected {all_singles}")

        return Verdict.OK()
    except DataException as e:
        print(e)
        return e.verdict
    except HTTPException as e:
        print(e)
        return e.verdict
    except Exception as e:
        print(e)


@checker.define_put(vuln_num=1, vuln_rate=1)
def put_flag_into_the_service(request: PutRequest) -> Verdict:
    try:

        return Verdict.OK()

    except HTTPException as e:
        return e.verdict


@checker.define_put(vuln_num=2, vuln_rate=1)
def put_flag_into_the_service2(request: PutRequest) -> Verdict:
    try:

        return Verdict.OK()
    except HTTPException as e:
        return e.verdict


@checker.define_get(vuln_num=1)
def get_flag_from_the_service(request: GetRequest) -> Verdict:
    try:

        return Verdict.OK()
    except HTTPException as e:
        return e.verdict
    except Exception as e:
        print(f"bad access {e}")
        return Verdict.CORRUPT("can't reach flag")


@checker.define_get(vuln_num=2)
def get_flag_from_the_service2(request: GetRequest) -> Verdict:
    try:

        return Verdict.OK()
    except HTTPException as e:
        return e.verdict
    except Exception as e:
        print(f"bad access {e}")
        return Verdict.CORRUPT("can't reach flag")


checker.run()
