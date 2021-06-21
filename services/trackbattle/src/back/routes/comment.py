from flask import Blueprint

comments_blueprint = Blueprint('comments', __name__)


@comments_blueprint.route("/api/comments", methods=['POST'])
def create():
    return "<p>Hello, World!</p>"


@comments_blueprint.route("/api/comments/<comment_id>", methods=['GET', 'PUT'])
def access(comment_id):
    return "<p>Hello, World!</p>"
