#!/usr/bin/env python3.7

from client import *

from gornilo import CheckRequest, Verdict, Checker, PutRequest, GetRequest

checker = Checker()


@checker.define_check
async def check_service(request: CheckRequest) -> Verdict:
    try:
        client = WBClient(None, request.hostname, 1234)
        client.CreateUser(utils.get_author_name())
        meta = Meta(utils.get_author_name(), utils.get_description())
        album_name = utils.get_album_name()
        album_client = client.CreateAlbum(album_name, meta)
        album_response = album_client.Get()

        single_name = utils.single_name()
        single_client = client.CreateSingle(single_name, utils.get_track(), meta)
        single_response = single_client.Get()

        single_name2 = utils.single_name()
        single_client2 = client.CreateSingle(single_name, utils.get_track(), meta)
        single_response2 = single_client.Get()

        print(single_client.Get())
        print(single_client2.Get())

        album_client.AttachSingle(single_client.single_id)
        album_client.AttachSingle(single_client2.single_id)

        print(album_client.GetAllSingles())
        print(album_client.Get())

        return Verdict.OK()
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
