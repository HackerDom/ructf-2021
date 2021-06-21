from sqlalchemy import Column, Integer, String, ARRAY

from models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    auth_token = Column(String, primary_key=True)
    nickname = Column(String)
    password_sha256 = Column(String)
    posts = Column(ARRAY(Integer))

    def __repr__(self):
        return "<User(auth_token='{}', password_sha256='{}', posts={})>" \
            .format(self.auth_token,
                    self.password_sha256,
                    self.posts)
