from atexit import register
from reportit import Base, engine, session, login_manager
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, LargeBinary
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2 import Geometry
from shapely.geometry import Point
from datetime import datetime
from sqlalchemy.orm import backref, relationship,declarative_mixin,declared_attr,has_inherited_table
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

##USER TABLE##

class User(Base,UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    f_Name = Column(String,nullable=False)
    l_Name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    # TODO: make National ID uniqe
    national_id = Column(String,unique=True,nullable=False)
    phone_num = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    register_time = Column(DateTime, default=datetime.utcnow)
    # reports= relationship('Utility', backref='author', lazy=True)

    # initializing
    def __init__(self, f_Name, l_Name, email, national_id, phone_num, password):
        self.f_Name = f_Name
        self.l_Name = l_Name
        self.email = email
        self.national_id = national_id
        self.phone_num = phone_num
        self.password = password

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

    # @declared_attr
    # def userid(cls):
    #     return Column(Integer, ForeignKey('user.id'), nullable=False)

    @declared_attr.cascading
    def id(cls):
        if has_inherited_table(cls):
            return Column(ForeignKey('user.id'), primary_key=True)
        else:
            return Column(Integer, primary_key=True)

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
    solved = Column(Boolean,unique=False,default=False)
    solved_time = Column(DateTime)
    # user_id = Column(Integer, ForeignKey('user.id'), nullable=False)


    def get_point(self):
        return to_shape(self.geometry)

    def __init__(self, type, lat, lon, effect, description,solved,user_id):
        self.type = type
        self.lat = lat
        self.lon = lon
        self.geometry = from_shape(Point(self.lon, self.lat), srid=4326)
        self.effect = effect
        self.description = description
        # self.img = img
        self.solved = solved
        # self.solved_time = solved_time
        self.user_id = user_id

    
    def __repr__(self):
        return f"Report('{self.type}', '{self.lat}'), '{self.lon}'), '{self.effect}'), '{self.description}')"


class Utility(MyMixin, Base):
    pass


class Pollution(MyMixin, Base):
    pass

class Road(MyMixin, Base):
    pass

class Disaster(MyMixin, Base):
    pass

class Fire(MyMixin, Base):
    pass

#Dropping All Tables
# Base.metadata.drop_all(engine, checkfirst=True)

#Creating All Tables
Base.metadata.create_all(engine, checkfirst=True)



# print(session.query(User).all())

# This is a query that is looking for the user with the national id of 12345678901111.
# userr = session.query(User).filter_by(national_id='12345678901111').first()

# Getting the user with the id of 3.
# userByGet = session.query(User).get(3)
# print(userByGet)

# print(userr.id)

# print(userByGet.reports)

