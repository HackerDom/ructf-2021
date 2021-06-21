import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import Mutable


def _get_env(name):
    value = os.getenv(name, None)

    if value is None:
        raise ValueError(f'please provide {name} as environment variable')

    return value


def _build_db_uri_from_env():
    user = _get_env('POSTGRES_USER')
    password = _get_env('POSTGRES_PASSWORD')
    host = _get_env('POSTGRES_HOST')
    db = _get_env('POSTGRES_DB_NAME')

    return f'postgresql+psycopg2://{user}:{password}@{host}:5432/{db}'


engine = create_engine(_build_db_uri_from_env())

BaseModel = declarative_base()


class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value
