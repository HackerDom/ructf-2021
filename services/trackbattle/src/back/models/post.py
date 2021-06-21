from sqlalchemy import Column, Integer, String, Date, ARRAY

from models.base import BaseModel


class Post(BaseModel):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    author_nickname = Column(String)
    publishing_date = Column(Date)
    track = Column(String)
    title = Column(String)
    description = Column(String)
    likes_amount = Column(Integer)
    comment_ids = Column(ARRAY(Integer))

    def __repr__(self):
        return "<Post(id='{}', author_nickname='{}', publishing_date='{}', track='{}', title='{}', description='{}', likes_amount='{}', comment_ids='{}')>" \
            .format(self.id,
                    self.author_nickname,
                    self.publishing_date,
                    self.track,
                    self.title,
                    self.description,
                    self.likes_amount,
                    self.comment_ids)
