from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from settings import *

host=MYSQL_HOST
db=MYSQL_DBNAME
user=MYSQL_USER
passwd=MYSQL_PASSWD

engine = create_engine("mysql://"+user+":"+passwd+"@"+host+"/"+db+"?charset=utf8")

DBSession = sessionmaker(bind=engine)

Base = declarative_base()

