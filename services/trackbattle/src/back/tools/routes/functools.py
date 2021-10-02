import functools

from flask import request

from models.sessions import make_session
from routes.common import \
    AUTH_HEADER, \
    get_not_authenticated_response, \
    get_authenticated_user_using_session, \
    get_expected_json_response, \
    get_expected_json_argument_response, get_expected_uri_argument_response


def need_authentication(keep_user_arg=None, keep_session_arg=None):
    def real_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            session = make_session()
            user = get_authenticated_user_using_session(session)

            if user is None:
                session.close()

                return get_not_authenticated_response()

            if keep_user_arg is not None:
                kwargs[keep_user_arg] = user

            if keep_session_arg is not None:
                kwargs[keep_session_arg] = session
            else:
                session.close()

            return func(*args, **kwargs)

        return wrapper

    return real_decorator


def expected_json_arguments(*arg_names):
    def real_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return get_expected_json_response()

            for arg_name in arg_names:
                value = request.json.get(arg_name)

                if value is None:
                    return get_expected_json_argument_response(arg_name)

                kwargs[arg_name] = value

            return func(*args, **kwargs)

        return wrapper

    return real_decorator


def expected_uri_arguments(*arg_names):
    def real_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for arg_name in arg_names:
                value = request.args.get(arg_name)

                if value is None:
                    return get_expected_uri_argument_response(arg_name)

                kwargs[arg_name] = value

            return func(*args, **kwargs)

        return wrapper

    return real_decorator
