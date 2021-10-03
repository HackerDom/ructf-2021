import datetime
import os
import threading
import time
import multiprocessing as mp
import requests

from random import randint
from filelock import FileLock, Timeout
from flask import Flask, request, make_response, jsonify
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from selenium import webdriver
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database, drop_database

from user_agent_randomizer import get_random_user_agent

app = Flask(__name__)


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


TB_API_PORT = 8080
TB_PORT = 8080
TB_AUTH_HEADER = 'XTBAuth'
SELENIUMS_AMOUNT = 4


def _get_env(name):
    value = os.getenv(name, None)

    if value is None:
        raise ValueError(f'please provide {name} as environment variable')

    return value


def _build_db_uri_from_env():
    user = _get_env('POSTGRES_USER')
    password = _get_env('POSTGRES_PASSWORD')
    host = _get_env('POSTGRES_HOST')
    db = _get_env('POSTGRES_DB_NAME')

    return f'postgresql+psycopg2://{user}:{password}@{host}:5432/{db}'


postgres_engine = create_engine(_build_db_uri_from_env())
BaseModel = declarative_base()


def init_database():
    if database_exists(postgres_engine.url):
        drop_database(postgres_engine.url)

    if not database_exists(postgres_engine.url):
        create_database(postgres_engine.url)

    BaseModel.metadata.create_all(postgres_engine)


@app.before_first_request
def app_init():
    init_database()


class User(BaseModel):
    __tablename__ = 'users'
    auth_token = Column(String, primary_key=True)
    host = Column(String)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<User(auth_token='{}', host={}, create_date={})>" \
            .format(self.auth_token, self.host, self.create_date)

    def is_old(self, now: datetime.datetime):
        return (now - self.create_date).min > 15


def make_session():
    return Session(postgres_engine)


@app.route("/users", methods=['POST'])
def put_user_info():
    if not request.is_json:
        return make_response(
            jsonify(
                message='request must be json'
            ),
            400
        )

    auth_token, host = request.json.get('auth_token'), request.json.get('host')

    if auth_token is None or host is None:
        return make_response(
            jsonify(
                message='request must contains user auth token and host'
            ),
            400
        )

    with make_session() as session:
        existing = find_user_by_token(auth_token, session)
        if existing is not None:
            return make_response(
                jsonify(
                    message='user with that token already exists'
                ),
                409
            )

        user = User(auth_token=auth_token, host=host)

        session.add(user)

        session.commit()

        return make_response(
            jsonify(
                message='user successfully created'
            ),
            201
        )


def find_user_by_token(auth_token, session):
    return session.query(User).filter(User.auth_token == auth_token).first()


def build_host_to_users_map(users):
    host_to_users = {}

    for user in users:
        host = user.host

        if host not in host_to_users:
            host_to_users[host] = list()

        host_to_users[host].append(user)

    return host_to_users


def select_random_selenium():
    selenium_idx = randint(0, SELENIUMS_AMOUNT - 1)

    return f'http://selenium{selenium_idx}:{4440 + selenium_idx}/wd/hub'


def run_execute_play_page(host, user, track):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-xss-auditor")
    driver = None
    try:
        driver = webdriver.Remote(select_random_selenium(), options=options)
        driver.get(f'http://{host}:{TB_PORT}/#/track?{track}')

        driver.add_cookie({
            'name': TB_AUTH_HEADER,
            'value': user.auth_token,
            'path': '/'
        })

        driver.get(f'http://{host}:{TB_PORT}/#/track?{track}')

        driver.find_element_by_xpath("//button[text()='play']").click()

        time.sleep(1)

    finally:
        if driver is not None:
            driver.close()


def get_posts_list(host, user_on_host, user_agent):
    r = get_session_with_retry().get(
        f"http://{host}:{TB_API_PORT}/api/posts/latest?limit=100",
        headers={'User-Agent': user_agent, TB_AUTH_HEADER: user_on_host.auth_token}
    )

    if r.status_code != 200:
        return None

    return r.json().get('posts')


def get_post_content(post, host, user, user_agent):
    response = get_session_with_retry().get(
        f'http://{host}:{TB_API_PORT}/api/posts/{post}',
        headers={'User-Agent': user_agent, TB_AUTH_HEADER: user.auth_token}
    )

    if response.status_code != 200:
        return None, None

    response_json = response.json()

    return response_json.get('track'), response_json.get('comments')


def get_comment_content(comment, host, user, user_agent):
    response = get_session_with_retry().get(
        f'http://{host}:{TB_API_PORT}/api/comments/{comment}',
        headers={'User-Agent': user_agent, TB_AUTH_HEADER: user.auth_token}
    )

    if response.status_code != 200:
        return None

    response_json = response.json()

    return response_json.get('track')


def run_pages_for_user_on_host(user, host, posts, user_agent):
    tasks_args = []

    for post in posts:
        track, comments = get_post_content(post, host, user, user_agent)

        if track is None or comments is None:
            continue

        tasks_args.append((host, user, track))

        for comment in comments:
            comment_track = get_comment_content(comment, host, user, user_agent)

            if comment_track is None:
                continue

            tasks_args.append((host, user, track))

    with mp.Pool() as pool:
        pool.map(run_execute_play_page, tasks_args)


def run_cycle(lock, session):
    try:
        with session:
            users = session.query(User).all()
        host_to_users = build_host_to_users_map(users)
        user_agent = get_random_user_agent()

        for (host, users_on_host) in host_to_users.items():
            try:
                if len(users_on_host) <= 1:
                    continue

                post_list = get_posts_list(host, users_on_host[0], user_agent)

                for user in users_on_host:
                    run_pages_for_user_on_host(user, host, post_list, user_agent)

            except Exception:
                continue

    finally:
        lock.release()


def run_cycle_in_thread(lock, session):
    threading.Thread(target=run_cycle, args=(lock, session)).start()


def run_cycle_with_acquired_lock(lock):
    with make_session() as session:
        run_cycle_in_thread(lock, session)


def try_run():
    lock = FileLock('running.lock')

    try:
        lock.acquire(timeout=1)
        run_cycle_with_acquired_lock(lock)
        return True
    except Timeout:
        return False


@app.route('/run', methods=['POST'])
def run():
    if try_run():
        return make_response(
            jsonify(
                message='tracks playing started'
            ),
            200
        )

    return make_response(
        jsonify(
            message='previous playing not finished yet'
        ),
        409
    )


def remove_old_users():
    while True:
        time.sleep(15 * 60)

        lock = FileLock('running.lock')

        try:
            lock.acquire()

            with make_session() as session:
                users = session.query(User).all()
                now = datetime.datetime.utcnow()

                for old_user in filter(lambda u: u.is_old(now), users):
                    session.delete(old_user)

                session.commit()
        finally:
            lock.release()


def run_playing():
    while True:
        time.sleep(60)

        try_run()


threading.Thread(target=remove_old_users).start()
# threading.Thread(target=run_playing).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=31337, debug=True)
