from uuid import uuid4

from flask import Blueprint, request, jsonify

from models.comment import Comment
from models.post import Post
from routes.common import find_entity_by_id_in_session, get_entity_not_found_response, get_invalid_request_response
from tools.routes.functools import need_authentication, expected_json_arguments

comments_blueprint = Blueprint('comments', __name__)


@comments_blueprint.route("/api/comments", methods=['POST'])
@need_authentication(keep_user_arg='user', keep_session_arg='session')
@expected_json_arguments('track', 'description', 'post_id')
def create_comment(track=None, description=None, post_id=None, user=None, session=None):
    with session:
        post = find_entity_by_id_in_session(session, Post, post_id)

        if post is None:
            return get_entity_not_found_response(Post, post_id)

        new_comment = Comment(
            id=str(uuid4()),
            track=track,
            description=description,
            likes_amount=0,
            author_nickname=user.nickname,
            post_id=post_id
        )

        post.comment_ids.append(new_comment.id)

        session.add(new_comment)

        session.commit()

        return jsonify(status='success', comment_id=new_comment.id)


@comments_blueprint.route("/api/comments/<comment_id>", methods=['GET', 'PUT'])
@need_authentication(keep_session_arg='session')
def get_or_update_comment(comment_id, session=None):
    comment = find_entity_by_id_in_session(session, Comment, comment_id)

    if comment is None:
        return get_entity_not_found_response(Comment, comment_id)

    if request.method == 'GET':
        return get_comment(session, comment)

    return update_comment(session, comment)


def get_comment(session, comment):
    with session:
        return jsonify(
            status="success",
            track=comment.track,
            description=comment.description,
            likes_cmount=comment.likes_amount,
            author_nickname=comment.author_nickname,
            post_id=comment.post_id,
            publishing_date=comment.publishing_date
        )


@expected_json_arguments('likes_amount')
def update_comment(session, comment, likes_amount=None):
    with session:
        new_likes_amount = int(likes_amount)

        if new_likes_amount < 0 or new_likes_amount > 10 ** 6:
            return get_invalid_request_response('invalid amount of likes')

        comment.likes_amount = new_likes_amount

        session.commit()

        return jsonify(status='success')
