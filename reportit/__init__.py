import os
import bcrypt
from dotenv import load_dotenv,find_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
load_dotenv(find_dotenv())
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
engine = create_engine(os.getenv('DB_URL'))
bcrypt = Bcrypt(app)
admin = Admin(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from reportit import routes