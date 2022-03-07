import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# app.config['SECRET_KEY'] = (os.environ.get('SECRET_KEY'))
engine = create_engine(os.environ.get('DATABASE_URL'))
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from reportit import routes