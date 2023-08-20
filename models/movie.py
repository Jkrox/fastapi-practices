from config.database import base
from sqlalchemy import Column, Integer, String, Float

# import datetime


class Movie(base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    # director = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    # genre = Column(String)
    overview = Column(String)
    category = Column(String)
    # actors = Column(String)
    # duration = Column(Integer)
    # image_url = Column(String)
    # trailer_url = Column(String)
    # created_at = Column(DateTime, default=datetime.datetime.utcnow)
    # updated_at = Column(DateTime, default=datetime.datetime.utcnow)
