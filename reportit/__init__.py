import os
import bcrypt
from dotenv import load_dotenv,find_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
load_dotenv(find_dotenv())
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
engine = create_engine(os.getenv('DB_URL'))
bcrypt = Bcrypt(app)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from reportit import routes