from flask import Blueprint

posts_blueprint = Blueprint('posts', __name__)


@posts_blueprint.route("/api/posts", methods=['POST'])
def create():
    return "<p>Hello, World!</p>"


@posts_blueprint.route("/api/posts/<post_id>", methods=['GET', 'PUT'])
def access(post_id):
    return "<p>Hello, World!</p>"


@posts_blueprint.route("/api/posts/latest", methods=['GET'])
def latest():
    return "<p>Hello, World!</p>"
