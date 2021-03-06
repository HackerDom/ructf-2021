import base64
import datetime
import os
import sys
import threading
import time
import multiprocessing as mp
import requests
import traceback

from random import randint
from selenium.webdriver.support.ui import WebDriverWait
from filelock import FileLock, Timeout
from flask import Flask, request, make_response, jsonify
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from selenium import webdriver
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database, drop_database
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
    if not database_exists(postgres_engine.url):
        create_database(postgres_engine.url)

    BaseModel.metadata.create_all(postgres_engine)


class User(BaseModel):
    __tablename__ = 'users'
    auth_token = Column(String, primary_key=True)
    host = Column(String)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<User(auth_token='{}', host={}, create_date={})>" \
            .format(self.auth_token, self.host, self.create_date)

    def is_old(self, now: datetime.datetime):
        ans = (now - self.create_date) > datetime.timedelta(minutes=15)

        print(f'{self.create_date} and {now}, answer is {ans}')

        return ans


def make_session():
    return Session(postgres_engine)


init_database()


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
    # selenium_idx = randint(0, SELENIUMS_AMOUNT - 1)

    return f'http://selenium:4444/wd/hub'


sem = threading.Semaphore(mp.cpu_count() * 2)


def run_execute_play_page(host, user, track, title, description):
    try:
        sem.acquire()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-xss-auditor")
        driver = None
        try:
            full = []
            if title is not None:
                full.append('title=' + title)
            if description is not None:
                full.append('description=' + description)
            full.append('track=' + track)
            full = '&'.join(full)
            print(f'running for http://{host}:{TB_PORT}/#/track?{full}', file=sys.stderr)
            full = base64.b64encode(full.encode('utf-8')).decode('utf-8')
            driver = webdriver.Remote(select_random_selenium(), options=options)
            driver.get(f'http://{host}:{TB_PORT}/#/track?{full}')

            driver.add_cookie({
                'name': TB_AUTH_HEADER,
                'value': user.auth_token,
                'path': '/'
            })

            driver.get(f'http://{host}:{TB_PORT}/#/track?{full}')

            # wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='play']")))

            driver.find_element_by_xpath("//button[text()='play']").click()
            print(f'running for http://{host}:{TB_PORT}/#/track?{full} completed', file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)
            traceback.print_tb(e, file=sys.stderr)
        finally:
            if driver is not None:
                driver.close()
    finally:
        sem.release()


def get_posts_list(host, user_on_host, user_agent):
    r = get_session_with_retry().get(
        f"http://{host}:{TB_API_PORT}/api/posts/latest?limit=200",
        headers={'User-Agent': user_agent, TB_AUTH_HEADER: user_on_host.auth_token}
    )
    print(r.text, file=sys.stderr)

    if r.status_code != 200:
        return None

    return r.json().get('posts')


def get_post_content(post, host, user, user_agent):
    response = get_session_with_retry().get(
        f'http://{host}:{TB_API_PORT}/api/posts/{post}',
        headers={'User-Agent': user_agent, TB_AUTH_HEADER: user.auth_token}
    )

    if response.status_code != 200:
        return None, None, None, None

    response_json = response.json()

    return response_json.get('track'), response_json.get('title'), response_json.get('description'), response_json.get(
        'comments')


def get_comment_content(comment, host, user, user_agent):
    response = get_session_with_retry().get(
        f'http://{host}:{TB_API_PORT}/api/comments/{comment}',
        headers={'User-Agent': user_agent, TB_AUTH_HEADER: user.auth_token}
    )

    if response.status_code != 200:
        return None, None

    response_json = response.json()

    return response_json.get('track'), response_json.get('description')


def run_pages_for_user_on_host(user, host, posts, user_agent):
    threads = []

    for post in posts:
        track, title, description, comments = get_post_content(post, host, user, user_agent)

        if track is None or comments is None:
            continue

        t = threading.Thread(target=run_execute_play_page, args=(host, user, track, title, description))
        t.start()
        threads.append(t)

        # for comment in comments:
        #     comment_track, description = get_comment_content(comment, host, user, user_agent)
        #
        #     if comment_track is None:
        #         continue
        #
        #     t = threading.Thread(target=run_execute_play_page, args=(host, user, comment_track, title, description))
        #     t.start()
        #     threads.append(t)

    return threads

    # with mp.Pool() as pool:
    #     pool.map(run_execute_play_page, tasks_args)


def run_cycle(lock):
    try:
        with make_session() as session:
            users = session.query(User).all()
        host_to_users = build_host_to_users_map(users)
        user_agent = get_random_user_agent()

        print('started pages execution for:', file=sys.stderr)
        print(host_to_users, file=sys.stderr)

        for (host, users_on_host) in host_to_users.items():
            try:
                if len(users_on_host) < 1:
                    continue

                post_list = get_posts_list(host, users_on_host[0], user_agent)

                if post_list is None:
                    continue

                print(f'posts are: {post_list}', file=sys.stderr)

                threads = []

                for user in users_on_host:
                    for t in run_pages_for_user_on_host(user, host, post_list, user_agent):
                        threads.append(t)

                print(f'joining {len(threads)} threads...', file=sys.stderr)
                for k in threads:
                    try:
                        k.join(3)
                    except Exception as e:
                        print(f'thread joining failed: ', e, file=sys.stderr)
                        traceback.print_tb(e, file=sys.stderr)

            except Exception as e:
                print(e, file=sys.stderr)
                traceback.print_tb(e, file=sys.stderr)

    finally:
        if lock is not None:
            lock.release()


def run_cycle_in_thread(lock):
    run_cycle(lock)
    # threading.Thread(target=run_cycle, args=(lock,)).start()


def run_cycle_with_acquired_lock(lock):
    run_cycle_in_thread(lock)


def try_run():
    # lock = FileLock('running.lock')
    #
    # try:
    #     lock.acquire(timeout=1)
        run_cycle_with_acquired_lock(None)
        return True
    # except Timeout:
    #     return False


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

        clean_old_users()


def clean_old_users():
    try:
        print('waiting 15 minutes to clean up old users', file=sys.stderr)

        with make_session() as session:
            users = session.query(User).all()
            now = datetime.datetime.utcnow()
            old = list(filter(lambda u: u.is_old(now), users))

            print(f'now date is {now}', file=sys.stderr)
            print('users to delete:', file=sys.stderr)
            print(old)

            for old_user in old:
                session.delete(old_user)

            session.commit()
    except Exception as e:
        print('error while cleaning users')
        print(e, file=sys.stderr)


def run_playing():
    while True:
        try_run()


@app.route('/clean', methods=['POST'])
def clean():
    clean_old_users()

    return make_response()


threading.Thread(target=remove_old_users).start()
threading.Thread(target=run_playing).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=31337, debug=True)
