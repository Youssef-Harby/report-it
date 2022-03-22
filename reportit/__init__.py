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
from flask_mail import Mail


app = Flask(__name__)
load_dotenv(find_dotenv())
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
engine = create_engine(os.getenv('DB_URL'))
bcrypt = Bcrypt(app)
admin = Admin(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']= 587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASS')
mail=Mail(app)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from reportit import routes