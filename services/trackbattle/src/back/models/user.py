from sqlalchemy import Column, String, ARRAY

from models.base import BaseModel, MutableList


class User(BaseModel):
    __tablename__ = 'users'
    auth_token = Column(String, primary_key=True)
    nickname = Column(String)
    password_sha256 = Column(String)
    posts = Column(MutableList.as_mutable(ARRAY(String)))
    payment_info = Column(String)

    def __repr__(self):
        return "<User(auth_token='{}', password_sha256='{}', posts={}, payment_info={})>" \
            .format(self.auth_token,
                    self.password_sha256,
                    self.posts,
                    self.payment_info)
