from uuid import uuid4

from flask import Blueprint, request, jsonify
from sqlalchemy import desc

from models.post import Post
from routes.common import get_entity_not_found_response, find_entity_by_id_in_session, get_invalid_request_response
from tools.routes.functools import need_authentication, expected_json_arguments, expected_uri_arguments

posts_blueprint = Blueprint('posts', __name__)


@posts_blueprint.route("/api/posts", methods=['POST'])
@need_authentication(keep_user_arg='user', keep_session_arg='session')
@expected_json_arguments('track', 'title', 'description')
def create_post(track=None, title=None, description=None, user=None, session=None):
    with session:
        new_post = Post(
            id=str(uuid4()),
            author_nickname=user.nickname,
            track=track,
            title=title,
            description=description,
            likes_amount=0,
            comment_ids=[]
        )

        user.posts.append(new_post.id)

        session.add(new_post)

        session.commit()

        return jsonify(post_id=new_post.id)


@posts_blueprint.route("/api/posts/<post_id>", methods=['GET', 'PUT'])
@need_authentication(keep_session_arg='session')
def get_or_update_post(post_id, session=None):
    post = find_entity_by_id_in_session(session, Post, post_id)

    if post is None:
        return get_entity_not_found_response(Post, post_id)

    if request.method == 'GET':
        return get_post(session, post)

    return update_post(session, post)


def get_post(session=None, post=None):
    with session:
        return jsonify(
            status="success",
            title=post.title,
            description=post.description,
            author=post.author_nickname,
            likes_amount=post.likes_amount,
            track=post.track,
            comments=post.comment_ids,
            publishing_date=post.publishing_date
        )


def update_post(session=None, post=None):
    with session:
        post.likes_amount = post.likes_amount + 1

        if post.likes_amount > 100500:
            return jsonify(status='success')

        session.commit()

        return jsonify(status='success')


@posts_blueprint.route("/api/posts/latest", methods=['GET'])
@need_authentication(keep_session_arg='session')
@expected_uri_arguments('limit')
def latest(limit=None, session=None):
    with session:
        limit = int(limit)

        if limit < 0:
            return get_invalid_request_response('expected valid amount of latest posts')

        latest_posts = session.query(Post).order_by(desc(Post.publishing_date)).limit(limit).all()

        return jsonify(
            status='success',
            posts=list(map(lambda x: x.id, latest_posts))
        )


@posts_blueprint.route("/api/posts/my", methods=['GET'])
@need_authentication(keep_user_arg='user')
def my(user=None):
    return jsonify(status='success', post_ids=user.posts)
