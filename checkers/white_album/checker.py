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
        meta = {"author": utils.get_author_name(), "description": utils.get_description()}

        album = {
            "id": {"id": str(uuid.uuid4())},
            "name": utils.get_album_name(),
            "meta": meta,
        }

        single_first = {
            "id": {"id": str(uuid.uuid4())},
            "name": utils.single_name(),
            "meta": meta,
            # "owner": {"id": user_id},
            "track": {"tokens": [utils.get_track(), utils.get_track()]}
        }

        single_second = {
            "id": {"id": str(uuid.uuid4())},
            "name": utils.single_name(),
            "meta": meta,
            # "owner": {"id": user_id},
            "track": {"tokens": [utils.get_track(), utils.get_track()]}
        }

        single_response = client.CreateSingle(single_first).Get()
        single_response.pop('signature')
        single_response.pop('owner')
        Check(single_response, single_first, "single")

        single_response2 = client.CreateSingle(single_second).Get()
        single_response2.pop('signature')
        single_response2.pop('owner')

        now = datetime.utcnow()
        single_by_date = client.GetSinglesByDate(now)
        Check(sorted([s["id"]["id"] for s in single_by_date]), sorted([single_first["id"]["id"], single_second["id"]["id"]]), "singles by date")
        Check(sorted([s["name"] for s in single_by_date]), sorted([single_first["name"], single_second["name"]]), "singles by date")

        Check(single_response2, single_second, "single")

        album_client = client.CreateAlbum(album)
        album_response = album_client.Get()
        album_client.AttachSingle(single_response["id"])
        album_client.AttachSingle(single_response2["id"])

        now = datetime.utcnow()
        album_by_date = client.GetAlbumByDate(now)
        Check(sorted([s["id"]["id"] for s in album_by_date]), [album["id"]["id"]], "albums by date")
        Check(sorted([s["name"] for s in album_by_date]), [album["name"]], "albums by date")

        album_response.pop("owner")
        album_response.pop("singles")  # TODO: check

        Check(album_response, album, "album")

        all_singles = album_client.GetAllSingles()

        for single in all_singles:
            single.pop("signature")
            single.pop("owner")

        Check(all_singles, [single_first, single_second], "singles")

        return Verdict.OK()
    except DataException as e:
        print(e)
        return e.verdict
    except HTTPException as e:
        print(e)
        return e.verdict
    except Exception as e:
        print(e)


def Check(actual, target, subject):
    if not compare(actual, target):
        raise DataException(
            Verdict.MUMBLE(f"Recived incorrect {subject} {actual}, expected {target}"))


@checker.define_put(vuln_num=1, vuln_rate=1)
def put_flag_into_the_service(request: PutRequest) -> Verdict:
    try:
        user_id = str(uuid.uuid4())

        client = WBClient(None, request.hostname, 1234)
        client.CreateUser(utils.get_author_name(), user_id)
        meta = {"author": utils.get_author_name(), "description": utils.get_description()}

        album = {
            "id": {"id": str(uuid.uuid4())},
            "name": utils.get_album_name(),
            "meta": meta,
        }

        single_meta = {"author": utils.get_author_name(), "description": request.flag}
        single = {
            "id": {"id": str(uuid.uuid4())},
            "name": utils.single_name(),
            "meta": single_meta,
            "track": {"tokens": [utils.get_track(), utils.get_track()]}
        }

        single_response = client.CreateSingle(single).Get()
        single_response.pop('signature')
        single_response.pop('owner')
        Check(single_response, single, "single")

        album_client = client.CreateAlbum(album)
        album_response = album_client.Get()
        album_client.AttachSingle(single_response["id"])

        album_response.pop("owner")
        album_response.pop("singles")
        Check(album_response, album, "album")

        return Verdict.OK(f"{client.apikey}||{json.dumps(album['id'])}||{json.dumps(single['id'])}")

    except HTTPException as e:
        return e.verdict


@checker.define_get(vuln_num=1)
def get_flag_from_the_service(request: GetRequest) -> Verdict:
    try:
        data = request.flag_id.replace("\n", "").split("||")

        user_id = data[0]
        album_id = json.loads(data[1])
        single_id = json.loads(data[2])

        client = WBClient(user_id, request.hostname, 1234)
        album = client.Album(album_id).Get()

        Check(album["singles"][0]["id"], single_id["id"], "single id")

        single = client.Single(single_id).Get()

        if single["meta"]["description"] != request.flag:
            return Verdict.CORRUPT("Can't reach flag")

        return Verdict.OK()
    except HTTPException as e:
        return e.verdict
    except Exception as e:
        print(f"bad access {e}")
        return Verdict.CORRUPT("can't reach flag")

# @checker.define_put(vuln_num=2, vuln_rate=1)
# def put_flag_into_the_service2(request: PutRequest) -> Verdict:
#     try:
#
#         return Verdict.OK()
#     except HTTPException as e:
#         return e.verdict
#
#
# @checker.define_get(vuln_num=2)
# def get_flag_from_the_service2(request: GetRequest) -> Verdict:
#     try:
#
#         return Verdict.OK()
#     except HTTPException as e:
#         return e.verdict
#     except Exception as e:
#         print(f"bad access {e}")
#         return Verdict.CORRUPT("can't reach flag")


checker.run()
