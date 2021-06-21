from uuid import uuid4

from flask import Blueprint, make_response, request, jsonify
from sqlalchemy import desc

from models.sessions import make_session
from models.post import Post
from routes.common import get_authenticated_user_using_session, is_authenticated, get_authenticated_user

posts_blueprint = Blueprint('posts', __name__)


@posts_blueprint.route("/api/posts", methods=['POST'])
def create():
    with make_session() as session:
        user = get_authenticated_user_using_session(session)

        if user is None:
            return make_response('not authenticated', 401)

        if not request.is_json:
            return make_response('expected json in body', 400)

        track = request.json.get('track')
        title = request.json.get('title')
        description = request.json.get('description')

        if track is None or title is None or description is None:
            return make_response('expected track, title and description', 400)

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
def post(post_id):
    if request.method == 'GET':
        return get_post(post_id)

    return update_post(post_id)


def get_post(post_id):
    with make_session() as session:
        if not is_authenticated(session):
            return make_response('not authenticated', 401)

        existing_post = session.query(Post).filter(Post.id == post_id).first()

        if existing_post is None:
            return make_response(f'post {post_id} not found', 404)

        return jsonify(
            title=existing_post.title,
            description=existing_post.description,
            author=existing_post.author_nickname,
            likes_amount=existing_post.likes_amount,
            track=existing_post.track,
            comments=existing_post.comment_ids,
            publishing_date=existing_post.publishing_date
        )


def update_post(post_id):
    with make_session() as session:
        if not is_authenticated(session):
            return make_response('not authenticated', 401)

        existing_post = session.query(Post).filter(Post.id == post_id).first()

        if existing_post is None:
            return make_response(f'post {post_id} not found', 404)

        if not request.is_json:
            return make_response('expected json', 400)

        new_likes = request.json.get('likes_amount')

        if new_likes is None:
            return make_response()

        likes = int(request.json.get('likes_amount'))

        if likes < 0 or likes > 10 ** 6:
            return make_response('invalid amount of likes', 400)

        existing_post.likes_amount = likes

        session.commit()

        return make_response()


@posts_blueprint.route("/api/posts/latest", methods=['GET'])
def latest():
    with make_session() as session:
        if not is_authenticated(session):
            return make_response('not authenticated', 401)

        if not request.is_json:
            return make_response('expected json', 400)

        amount = request.json.get('amount')

        if amount is None or int(amount) < 0:
            return make_response('expected valid amount of latest posts', 400)

        latest_posts = session.query(Post).order_by(desc(Post.publishing_date)).limit(int(amount)).all()

        return jsonify(posts=list(map(lambda x: x.id, latest_posts)))


@posts_blueprint.route("/api/posts/my", methods=['GET'])
def my_posts():
    user = get_authenticated_user()

    if user is None:
        return make_response('not authenticated', 401)

    return jsonify(posts=user.posts)
