import os

from flask import Flask

from sqlalchemy_utils import database_exists, create_database, drop_database

from models.base import BaseModel, engine
from routes.user import users_blueprint
from routes.post import posts_blueprint
from routes.comment import comments_blueprint

app = Flask(__name__)
app.register_blueprint(users_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(comments_blueprint)
app.debug = False


def should_drop_db():
    return os.getenv('TB_DROP_DB', default=None) is not None


def init_database():
    if should_drop_db() and database_exists(engine.url):
        drop_database(engine.url)

    if not database_exists(engine.url):
        create_database(engine.url)

    BaseModel.metadata.create_all(engine)


@app.before_first_request
def app_init():
    init_database()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=31337, debug=True)
