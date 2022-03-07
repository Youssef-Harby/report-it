from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine("postgresql://postgres:Report-It1324@db.fzhwhfsskyzuhcfjpzcf.supabase.co:5432/postgres")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from reportit import routes