from sqlalchemy.orm import Session

from models.base import engine


def make_session():
    return Session(engine)
