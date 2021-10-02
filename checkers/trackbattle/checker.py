#!/usr/bin/env python3
import base64

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
SELENIUM_ADDRESS = 'http://5.45.248.209:31337/users'

mumble = Verdict.MUMBLE('wrong server response')


def get_sha256(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


flag_alphabet = string.digits + string.ascii_uppercase


def generate_some_flag():
    # [0-9A-Z]{31}=
    flag = []
    for i in range(31):
        flag.append(random.choice(flag_alphabet))
    flag.append('=')

    return ''.join(flag)


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
                "payment_info": put_request.flag
            },
        )

        log.debug(f'response: \ncode: {response.status_code}\nheaders:{response.headers}\ntext:{response.text}')

        if response.status_code != 200:
            log.error(f'unexpected code - {response.status_code}')
            return mumble

        response_json = response.json()
        auth_token = response_json['auth_token']
        log.debug(f'user created with auth_token {response.json()}')

        if response.headers[TB_AUTH_HEADER] != auth_token:
            return mumble

        log.debug(f'sending ({auth_token} {put_request.hostname}) into selenium..')
        response = get_session_with_retry().post(
            SELENIUM_ADDRESS, json={
                'auth_token': auth_token,
                'host': put_request.hostname
            }
        )
        log.debug(response.text)

        if response.status_code != 200:
            log.error(f'!!!! status code is not 200!!!!')

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

        if response.json()['payment_info'] == get_request.flag:
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
    try:
        nickname = 'user-' + str(uuid.uuid4())
        password = str(uuid.uuid4())
        password_sha256 = get_sha256(password)
        flag = generate_some_flag()
        user_agent = get_random_user_agent()

        log.info(f">>>>> {nickname} with password {password} and flag {flag}")

        session = get_session_with_retry()

        auth_token, verdict = check_creation(check_request, flag, nickname, password_sha256, session, user_agent)
        if verdict is not None:
            return verdict

        verdict = check_get_user(auth_token, check_request, session, user_agent, flag, nickname)
        if verdict is not None:
            return verdict

        verdict = check_auth(check_request, nickname, password_sha256, session, user_agent, auth_token)
        if verdict is not None:
            return verdict

        latest_posts_ids, verdict = check_latest(check_request, session, user_agent, auth_token)
        if verdict is not None:
            return verdict

        verdict = check_likes_on_posts(check_request, session, user_agent, auth_token, latest_posts_ids)
        if verdict is not None:
            return verdict

        post_id, verdict = check_make_some_post(check_request, session, user_agent, auth_token)
        if verdict is not None:
            return verdict

        log.info(f"<<<<< {nickname}")

        return Verdict.OK()
    except Timeout as e:
        log.error(f'{e}, {print_exc()}')
        return Verdict.DOWN("service not responding")
    except Exception as e:
        log.error(f'{e}, {print_exc()}')
        return Verdict.CORRUPT("service can't give a flag")


def check_make_some_post(check_request, session, user_agent, auth_token):
    track = json.dumps({
        'notes': ''.join(
            [random.choice(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]) for _ in range(20)]),
        'waveform': random.choice(["sine", "square", "sawtooth", "triangle"])
    })
    track = base64.b64encode(track.encode('utf-8')).decode('utf-8')
    title = ''.join([random.choice(string.ascii_letters) for _ in range(15)])
    description = ''.join([random.choice(string.ascii_letters) for _ in range(15)])
    r = session.post(
        f'http://{check_request.hostname}:{TB_API_PORT}/api/posts',
        cookies={
            TB_AUTH_HEADER: auth_token
        },
        headers={'User-Agent': user_agent},
        json={
            'track': track,
            'title': title,
            'description': description
        }
    )
    log.info(r.text)

    if r.status_code != 200:
        return None, mumble

    post_id = r.json().get('post_id')

    r = session.get(
        f'http://{check_request.hostname}:{TB_API_PORT}/api/posts/{post_id}',
        headers={'User-Agent': user_agent, TB_AUTH_HEADER: auth_token}
    )
    log.info(r.text)

    if r.status_code != 200 or r.json().get('track') != track or r.json().get('title') != title or r.json().get(
            'description') != description:
        return None, mumble

    return post_id, None


def check_auth(check_request, nickname, password_sha256, session, user_agent, auth_token):
    r = session.put(
        f"http://{check_request.hostname}:{TB_API_PORT}/api/users/auth_token",
        headers={"User-Agent": user_agent},
        json={
            "nickname": nickname,
            "password_sha256": password_sha256,
        }
    )
    log.info(r.text)

    if r.status_code != 200 or r.headers.get(TB_AUTH_HEADER) != auth_token or r.json().get('auth_token') != auth_token:
        return mumble

    return None


def check_get_user(auth_token, check_request, session, user_agent, flag, nickname):
    r = session.get(
        f"http://{check_request.hostname}:{TB_API_PORT}/api/users",
        cookies={
            TB_AUTH_HEADER: auth_token
        },
        headers={"User-Agent": user_agent, }
    )
    log.info(r.text)
    j = r.json()

    if r.status_code != 200 or j.get('payment_info') != flag or j.get('nickname') != nickname or j.get('posts') != []:
        return mumble

    return None


def check_creation(check_request, flag, nickname, password_sha256, session, user_agent):
    r = session.post(
        f"http://{check_request.hostname}:{TB_API_PORT}/api/users",
        headers={"User-Agent": user_agent},
        json={
            "nickname": nickname,
            "password_sha256": password_sha256,
            "payment_info": flag
        },
    )
    log.info(r.text)
    auth_token = r.headers.get(TB_AUTH_HEADER)

    if r.status_code != 200 or auth_token is None:
        return None, mumble

    return auth_token, None


def check_latest(check_request, session, user_agent, auth_token):
    r = session.get(
        f"http://{check_request.hostname}:{TB_API_PORT}/api/posts/latest?limit=100",
        cookies={
            TB_AUTH_HEADER: auth_token
        },
        headers={'User-Agent': user_agent}
    )
    log.info(r.text)

    posts = r.json().get('posts')
    if r.status_code != 200 or posts is None or len(posts) > 100:
        return None, mumble

    if len(posts) == 0:
        return [], None

    return [random.choice(posts) for _ in range(5)], None


def check_likes_on_posts(check_request, session, user_agent, auth_token, latest_posts_ids):
    for post in latest_posts_ids:
        r = session.get(
            f"http://{check_request.hostname}:{TB_API_PORT}/api/posts/{post}",
            headers={'User-Agent': user_agent, TB_AUTH_HEADER: auth_token}
        )
        log.info(r.text)

        j = r.json()

        if r.status_code != 200:
            return mumble

        for k in ['author', 'comments', 'description', 'likes_amount', 'publishing_date', 'title', 'track']:
            if j.get(k) is None:
                return mumble

        current_likes = int(j.get('likes_amount'))

        r = session.put(
            f"http://{check_request.hostname}:{TB_API_PORT}/api/posts/{post}",
            cookies={
                TB_AUTH_HEADER: auth_token
            },
            headers={'User-Agent': user_agent}
        )
        log.info(r.text)

        if r.status_code != 200:
            return mumble

        r = session.get(
            f"http://{check_request.hostname}:{TB_API_PORT}/api/posts/{post}",
            headers={'User-Agent': user_agent, TB_AUTH_HEADER: auth_token}
        )
        log.info(r.text)

        j = r.json()

        if r.status_code != 200:
            return mumble

        for k in ['author', 'comments', 'description', 'likes_amount', 'publishing_date', 'title', 'track']:
            if j.get(k) is None:
                return mumble

        new_likes = int(j.get('likes_amount'))

        if new_likes != 100500 and new_likes != current_likes + 1 and new_likes != current_likes + 2 and new_likes != current_likes + 3:
            return mumble

    return None


if __name__ == "__main__":
    checker.run()
