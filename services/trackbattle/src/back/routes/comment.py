from uuid import uuid4

from flask import Blueprint, make_response, request, jsonify

from models.comment import Comment
from models.post import Post
from models.sessions import make_session
from routes.common import get_authenticated_user_using_session, is_authenticated

comments_blueprint = Blueprint('comments', __name__)


@comments_blueprint.route("/api/comments", methods=['POST'])
def create():
    with make_session() as session:
        user = get_authenticated_user_using_session(session)

        if user is None:
            return make_response('not authenticated', 401)

        if not request.is_json:
            return make_response('expected json', 400)

        track = request.json.get('track')
        description = request.json.get('description')
        post_id = request.json.get('post_id')

        if track is None or description is None or post_id is None:
            return make_response('expected track, description and post_id fields', 400)

        post = session.query(Post).filter(Post.id == post_id).first()

        if post is None:
            return make_response(f'post {post_id} not found', 404)

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

        return jsonify(comment_id=new_comment.id)


@comments_blueprint.route("/api/comments/<comment_id>", methods=['GET', 'PUT'])
def comment(comment_id):
    if request.method == 'GET':
        return get_comment(comment_id)

    return update_comment(comment_id)


def get_comment(comment_id):
    with make_session() as session:
        if not is_authenticated(session):
            return make_response('not authenticated', 401)

        existing_comment = session.query(Comment).filter(Comment.id == comment_id).first()

        if existing_comment is None:
            return make_response(f'comment {comment_id} not found', 404)

        return jsonify(
            track=existing_comment.track,
            description=existing_comment.description,
            likes_cmount=existing_comment.likes_amount,
            author_nickname=existing_comment.author_nickname,
            post_id=existing_comment.post_id,
            publishing_date=existing_comment.publishing_date
        )


def update_comment(comment_id):
    with make_session() as session:
        if not is_authenticated(session):
            return make_response('not authenticated', 401)

        existing_comment = session.query(Comment).filter(Comment.id == comment_id).first()

        if existing_comment is None:
            return make_response(f'comment {comment_id} not found', 404)

        if not request.is_json:
            return make_response('expected json', 400)

        new_likes = request.json.get('likes_amount')

        if new_likes is None:
            return make_response()

        new_likes_amount = int(request.json.get('likes_amount'))

        if new_likes_amount < 0 or new_likes_amount > 10 ** 6:
            return make_response('invalid amount of likes', 400)

        existing_comment.likes_amount = new_likes_amount

        session.commit()

        return make_response()
