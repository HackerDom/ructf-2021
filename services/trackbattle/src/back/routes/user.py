from uuid import uuid4

from flask import make_response, Blueprint, jsonify
from sqlalchemy import and_

from models.sessions import make_session
from models.user import User
from routes.common import get_success_auth_response, get_authentication_failed_response
from tools.routes.functools import expected_json_arguments

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route("/api/users", methods=['POST'])
@expected_json_arguments('nickname', 'password_sha256')
def create(nickname=None, password_sha256=None):
    with make_session() as session:
        existing = session.query(User).filter(User.nickname == nickname).first()

        if existing is not None:
            return make_response(
                jsonify(
                    status='error',
                    message=f"username '{nickname}' already exists"
                ),
                409
            )

        auth_token = str(uuid4())
        new_user = User(
            auth_token=auth_token,
            nickname=nickname,
            password_sha256=password_sha256,
            posts=[]
        )

        session.add(new_user)

        session.commit()

        return get_success_auth_response(auth_token)


@users_blueprint.route("/api/users/auth_token", methods=['GET'])
@expected_json_arguments('nickname', 'password_sha256')
def auth(nickname=None, password_sha256=None):
    with make_session() as session:
        user = session.query(User).filter(
            and_(
                User.nickname == nickname,
                User.password_sha256 == password_sha256
            )).first()

        if user is None:
            return get_authentication_failed_response()

        return get_success_auth_response(user.auth_token)
