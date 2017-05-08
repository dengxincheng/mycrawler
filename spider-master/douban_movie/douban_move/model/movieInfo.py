#movieInfo.py
from sqlalchemy import Column, String , Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MovieInfo(Base):
    __tablename__ = 'rs_movie'
    rs_movie_id  = Column(String,primary_key=True)
    rs_movie_name = Column(String)
    rs_movie_type = Column(String)
    rs_movie_director = Column(String)
    rs_movie_writer = Column(String)
    rs_movie_stars = Column(String)
    rs_movie_showtime = Column(String)
    rs_movie_length = Column(String)
    rs_movie_img = Column(String)
    rs_movie_country = Column(String)
    rs_movie_language = Column(String)
    rs_movie_updatatime = Column(String)