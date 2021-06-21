from uuid import uuid4

from flask import request, make_response, Blueprint
from sqlalchemy import and_

from models.sessions import make_session
from models.user import User
from routes.common import CONTENT_TYPE_FROM_URL, AUTH_HEADER


def extract_nickname_and_password_hash():
    if request.content_type == CONTENT_TYPE_FROM_URL:
        nickname = request.form.get('username', default=None)
        password_sha256 = request.form.get('password_sha256', default=None)
    elif request.is_json:
        nickname = request.json.get('username')
        password_sha256 = request.json.get('password_sha256')
    else:
        return None, None

    return nickname, password_sha256


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route("/api/users/create", methods=['POST'])
def create():
    nickname, password_sha256 = extract_nickname_and_password_hash()

    if nickname is None or password_sha256 is None:
        return make_response('expected username and password_sha256 for creation new user', 400)

    with make_session() as session:
        existing = session.query(User).filter(User.nickname == nickname).first()

        if existing is not None:
            return make_response(f'username {nickname} already exists', 409)

        auth_token = str(uuid4())
        new_user = User(
            auth_token=auth_token,
            nickname=nickname,
            password_sha256=password_sha256,
            posts=[]
        )

        session.add(new_user)

        session.commit()

    response = make_response('', 200)
    response.headers[AUTH_HEADER] = auth_token

    return response


@users_blueprint.route("/api/users/auth", methods=['GET'])
def auth():
    nickname, password_sha256 = extract_nickname_and_password_hash()

    if nickname is None or password_sha256 is None:
        return make_response('need username and password_sha256 for authentication', 400)

    with make_session() as session:
        user = session.query(User).filter(
            and_(
                User.nickname == nickname,
                User.password_sha256 == password_sha256
            )).first()

        if user is None:
            return make_response('invalid username or password', 401)

        response = make_response('', 200)
        response.headers[AUTH_HEADER] = user.auth_token

        return response

