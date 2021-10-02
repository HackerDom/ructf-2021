import uuid
from sys import stderr
import requests
import utils
import json

from gornilo import Verdict


def close(code, public="", private=""):
    if public:
        print(public)
    if private:
        print(private, file=stderr)
    print('Exit with code %d' % code, file=stderr)
    exit(code)


def ensure_success(request):
    try:
        r = request()
    except Exception as e:
        print(e)
        raise HTTPException(Verdict.DOWN("HTTP error"))
    if r.status_code != 200:
        print(r)
        raise HTTPException(Verdict.MUMBLE("Invalid status code: %s %s" % (r.url, r.status_code)))
    return r


class HTTPException(Exception):
    def __init__(self, verdict=None):
        self.verdict = verdict  # you could add more args

    def __str__(self):
        return str(self.verdict)


class Client:
    def __init__(self, apikey, address, port):
        self.port = port
        self.user_id = str(uuid.uuid4())
        self.address = address
        self.apikey = apikey

    def __api_call__(self, function, path):
        url = f'http://{self.address}:{self.port}/{path}'
        headers = {'User-Agent': utils.get_user_agent(), "Content-Type": "application/json"}
        cookies = dict({'Api-Token': self.apikey})
        return function(url, headers, cookies)

    def post(self, path, payload):
        def call(url, headers, cookies):
            response = ensure_success(
                lambda: requests.post(url, headers=headers, data=json.dumps(payload), cookies=cookies, verify=False))
            return response

        r = self.__api_call__(call, path)
        if r.content is None or len(r.content) == 0:
            return None

        return json.loads(r.content.decode("UTF-8"))


class Meta:

    def __init__(self, author, description):
        self.description = description
        self.author = author

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=2)



class AlbumClient(Client):

    def __init__(self, apikey, address, port, album_id):
        super().__init__(apikey, address, port)
        self.album_id = album_id

    def AttachSingle(self, single_id):
        payload = {
            "Single": {
                "Id": single_id["id"]
            },
            "AlbumId": {
                "Id": self.album_id["id"]
            }
        }

        self.post("album/attach", payload)

    def Get(self):
        payload = {
            "Id": self.album_id
        }
        return self.post("album/get", payload)

    def GetAllSingles(self):
        payload = {
            "Id": self.album_id
        }
        return self.post("album/get_all_singles", payload)


class SingleClient(Client):

    def __init__(self, apikey, address, port, single_id):
        super().__init__(apikey, address, port)
        self.single_id = single_id

    def Get(self):
        payload = {
            "Id": self.single_id
        }
        return self.post("single/get", payload)

    def RenderSingle(self):
        payload = {
            "Id": self.single_id
        }

        return self.post("single/render", payload)


class WBClient(Client):

    def __init__(self, apikey, address, port):
        super().__init__(apikey, address, port)
        self.user_id = str(uuid.uuid4())

    def CreateUser(self, name, user_id):
        payload = {
            "Id": {
                "Id": f"{user_id}"
            },
            "Name": name
        }

        self.apikey = self.post("user/create", payload)["id"]

    def CreateAlbum(self, album) -> AlbumClient:
        payload = {
            "Id": album["id"],
            "Meta": album["meta"],
            "Name": album["name"]
        }

        self.post("album/create", payload)

        return AlbumClient(self.apikey, self.address, self.port, album["id"])

    def CreateSingle(self, single) -> SingleClient:
        payload = {
            "Id": single["id"],
            "Meta": single["meta"],
            "Track": single["track"],
            "Name": single["name"]
        }

        self.post("single/create", payload)

        return SingleClient(self.apikey, self.address, self.port, single["id"])

    def Album(self, album_id) -> AlbumClient:
        return AlbumClient(self.apikey, self.address, self.port, album_id)

    def Single(self, single_id) -> SingleClient:
        return SingleClient(self.apikey, self.address, self.port, single_id)

    def ensure_success(self, request):
        try:
            r = request()
        except Exception as e:
            raise HTTPException(Verdict.DOWN("HTTP error"))
        if r.status_code != 200:
            raise HTTPException(Verdict.MUMBLE("Invalid status code: %s %s" % (r.url, r.status_code)))
        return r