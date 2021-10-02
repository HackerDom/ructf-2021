import datetime

from sqlalchemy import Column, Integer, String, DateTime

from models.base import BaseModel


class Comment(BaseModel):
    __tablename__ = 'comments'
    id = Column(String, primary_key=True)
    track = Column(String)
    description = Column(String)
    likes_amount = Column(Integer)
    author_nickname = Column(String)
    post_id = Column(String)
    publishing_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Comment(id='{}', track='{}', description='{}', likes_amount='{}', author_nickname='{}', post_id='{}', publishing_date='{}'>" \
            .format(self.id,
                    self.track,
                    self.description,
                    self.likes_amount,
                    self.author_nickname,
                    self.post_id,
                    self.publishing_date)
