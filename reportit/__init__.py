from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from form import Form

app = Flask(__name__)

engine = create_engine("postgresql://docker:docker@192.168.1.104:5432/gis")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
