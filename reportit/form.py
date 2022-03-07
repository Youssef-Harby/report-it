from reportit import Base, engine, session
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, LargeBinary
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2 import Geometry
from shapely.geometry import Point
from datetime import datetime
from sqlalchemy.orm import backref, relationship,declarative_mixin,declared_attr

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

@declarative_mixin
class MyMixin:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __mapper_args__= {'always_refresh': True}

    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    geometry = Column((Geometry("POINT", srid=4326, spatial_index=True)))
    effect = Column(Integer)
    description = Column(String)
    img = Column(LargeBinary)


    def get_point(self):
        return to_shape(self.geometry)

    
    def __repr__(self):
        return f"Report('{self.type}', '{self.lat}'), '{self.lon}'), '{self.effect}'), '{self.description}')"


class Utility(MyMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    pass


class Pollution(MyMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    pass

class Road(MyMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    pass

class Disaster(MyMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    pass

class Fire(MyMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    pass

#Dropping All Tables
Base.metadata.drop_all(engine, checkfirst=True)

#Creating All Tables
Base.metadata.create_all(engine, checkfirst=True)



print(session.query(User).all())

# This is a query that is looking for the user with the national id of 12345678901111.
# userr = session.query(User).filter_by(national_id='12345678901111').first()

# Getting the user with the id of 3.
# userByGet = session.query(User).get(3)
# print(userByGet)

# print(userr.id)

# print(userByGet.reports)

