from flask import request

from models.user import User
from models.sessions import make_session

AUTH_HEADER = 'XTBAuth'
CONTENT_TYPE_FROM_URL = 'application/x-www-form-urlencoded'
CONTENT_TYPE_JSON = 'application/json'


def get_authenticated_user():
    with make_session() as session:
        return get_authenticated_user_in_session(session)


def get_authenticated_user_in_session(session):
    auth_header = request.headers.get(AUTH_HEADER, default=None)

    if auth_header is None:
        return None

    return session.query(User).filter(User.auth_token == auth_header).first()
