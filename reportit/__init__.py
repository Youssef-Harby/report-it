from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine("postgresql://postgres:postgres@localhost:5432/GIS")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from reportit import routes