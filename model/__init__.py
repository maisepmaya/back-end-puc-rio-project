from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


from model.base import Base
from model.sheet import Sheet
from model.card import Card

db_path = "database/"

if not os.path.exists(db_path):
   os.makedirs(db_path)

db_url = 'sqlite:///%s/db.sqlite3' % db_path

engine = create_engine(db_url, echo=False, pool_size=20, max_overflow=0)


Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url) 

Base.metadata.create_all(engine)
