from sqlalchemy import Column, Integer, String, Date

from models.base import BaseModel


class Comment(BaseModel):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    track = Column(String)
    description = Column(String)
    likes_amount = Column(Integer)
    author_nickname = Column(String)
    post_id = Column(Integer)
    publishing_date = Column(Date)

    def __repr__(self):
        return "<Comment(id='{}', track='{}', description='{}', likes_amount='{}', author_nickname='{}', post_id='{}', publishing_date='{}'>" \
            .format(self.id,
                    self.track,
                    self.description,
                    self.likes_amount,
                    self.author_nickname,
                    self.post_id,
                    self.publishing_date)
