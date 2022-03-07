from reportit import Base, engine, session
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, LargeBinary
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2 import Geometry
from shapely.geometry import Point
from datetime import datetime
from sqlalchemy.orm import backref, relationship

##USER TABLE##


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    f_Name = Column(String)
    l_Name = Column(String)
    email = Column(String)
    # TODO: make National ID uniqe
    national_id = Column(String)
    phone_num = Column(String)
    reports= relationship('Utility', backref='author', lazy=True)

    # initializing
    def __init__(self, f_Name, l_Name, email, national_id, phone_num):
        self.f_Name = f_Name
        self.l_Name = l_Name
        self.email = email
        self.national_id = national_id
        self.phone_num = phone_num

    def __repr__(self):
        return f"User('{self.f_Name}', '{self.l_Name}', '{self.email}'), '{self.national_id}'), '{self.phone_num}')"

##Categories ID##


class Categories (Base):
    __tablename__ = 'categories'

    cat_name = Column(String)
    id = Column(Integer, primary_key=True)

    def __init__(self, cat_name, cat_id):
        self.cat_name = cat_name
        self.id = cat_id

## Reported problems Tables##


class Utility(Base):
    __tablename__ = 'utility'
    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    geometry = Column((Geometry("POINT", srid=4326, spatial_index=True)))
    effect = Column(Integer)
    description = Column(String)
    img = Column(LargeBinary)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # categories = relationship("Categories", backref="categories")


    def __init__(self, type, lat, lon, effect, description,user_id):
        self.type = type
        self.lat = lat
        self.lon = lon
        # self.timestamp = str(datetime.utcnow())
        self.geometry = from_shape(Point(self.lon, self.lat), srid=4326)
        self.effect = effect
        self.description = description
        # self.img = img
        self.user_id = user_id
    
    def __repr__(self):
        return f"Report('{self.type}', '{self.lat}'), '{self.lon}'), '{self.effect}'), '{self.description}')"

    def get_point(self):
        return to_shape(self.geometry)

# Dropping all the tables in the database.
# Base.metadata.drop_all(engine, checkfirst=True)

# Creating all the tables in the database.
Base.metadata.create_all(engine, checkfirst=True)

# print(session.query(User).all())

# This is a query that is looking for the user with the national id of 12345678901111.
# userr = session.query(User).filter_by(national_id='12345678901111').first()

# Getting the user with the id of 3.
# userByGet = session.query(User).get(3)
# print(userByGet)

# print(userr.id)

# print(userByGet.reports)

