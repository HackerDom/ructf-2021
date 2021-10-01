from flask import request, make_response, jsonify

from models.user import User
from models.sessions import make_session

AUTH_HEADER = 'XTBAuth'
CONTENT_TYPE_FROM_URL = 'application/x-www-form-urlencoded'
CONTENT_TYPE_JSON = 'application/json'
MAX_TRACK_LENGTH = 124


def get_authenticated_user():
    with make_session() as session:
        return get_authenticated_user_using_session(session)


def get_authenticated_user_using_session(session):
    auth_header = request.headers.get(AUTH_HEADER, default=None)

    if auth_header is None:
        return None

    return session.query(User).filter(User.auth_token == auth_header).first()


def is_authenticated(session):
    return get_authenticated_user_using_session(session) is not None


def get_not_authenticated_response():
    return make_response(
        jsonify(
            status='error',
            message='not authenticated'
        ),
        401
    )


def get_authentication_failed_response():
    return make_response(
        jsonify(
            status='error',
            message='invalid nickname or password'
        ),
        401
    )


def get_expected_json_response():
    return get_invalid_request_response('expected json as body of request')


def get_expected_json_argument_response(arg_name):
    return make_response(
        jsonify(
            status='error',
            message=f'expected json-body argument "{arg_name}" but not found'
        ),
        400
    )


def get_expected_uri_argument_response(arg_name):
    return make_response(
        jsonify(
            status='error',
            message=f'expected url argument "{arg_name}" but not found'
        ),
        400
    )


def invalid_track_length_response():
    return make_response(
        jsonify(
            status='error',
            message=f'invalid track length (max is {MAX_TRACK_LENGTH})'
        ),
        400
    )


def get_success_auth_response(auth_token):
    response = make_response(
        jsonify(
            status='success',
            auth_token=auth_token
        ),
        200
    )
    response.headers[AUTH_HEADER] = auth_token

    return response


def get_success_user_response(user):
    return make_response(
        jsonify(
            nickname=user.nickname,
            posts=user.posts,
            payment_info=user.payment_info
        ),
        200
    )


def get_entity_not_found_response(entity_type, entity_id):
    return make_response(
        jsonify(
            status='error',
            message=f"{entity_type.__name__.lower()} '{entity_id}' not found",
            id=entity_id
        ),
        404
    )


def get_invalid_request_response(message):
    return make_response(
        jsonify(
            status='error',
            message=message),
        400
    )


def find_entity_by_id_in_session(session, entity_type, entity_id):
    return session.query(entity_type).filter(entity_type.id == entity_id).first()
