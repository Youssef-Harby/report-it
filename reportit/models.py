from reportit import Base, engine, session, login_manager, admin, ModelView
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, LargeBinary
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2 import Geometry
from shapely.geometry import Point
from datetime import datetime
from sqlalchemy.orm import backref, relationship, declarative_mixin, declared_attr
from flask_login import UserMixin, AnonymousUserMixin, current_user

ACCESS = {
    'guest': 0,
    'user': 1,
    'waterORG': 2,
    'gasORG': 3,
    'utilityORG': 4,
    'admin': 666,
}

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

##USER TABLE##

class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    f_Name = Column(String, nullable=False)
    l_Name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    national_id = Column(String, unique=True, nullable=False)
    phone_num = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    register_time = Column(DateTime, default=datetime.utcnow)
    access = Column(Integer, nullable=False)
    reports= relationship('Utility', backref='reporter', lazy=True)

    # initializing
    def __init__(self, f_Name, l_Name, email, national_id, phone_num, password, access=ACCESS['user']):
        self.f_Name = f_Name
        self.l_Name = l_Name
        self.email = email
        self.national_id = national_id
        self.phone_num = phone_num
        self.password = password
        self.access = access

    def __repr__(self):
        return f"User('{self.f_Name}', '{self.l_Name}', '{self.email}'), '{self.national_id}'), '{self.phone_num}'), '{self.access}'),"

    def is_admin(self):
        return self.access == ACCESS['admin']

    def allowed(self, access_level):
        return self.access == access_level

    

class Controller(ModelView):
    def is_accessible(self):
            return current_user.is_admin()
    def not_auth(self):
        return "Not Admin"

class AnonymousUser(AnonymousUserMixin):
    def allowed(self, access):
            return False

    def is_admin(self):
            return False


login_manager.anonymous_user = AnonymousUser

##Categories ID##

catcat = ['water', 'sewage', 'gas', 'electric', 'telecom', 'utility']


class Categories (Base):
    __tablename__ = 'categories'

    cat_name = Column(String)
    id = Column(Integer, primary_key=True)
    type= relationship('Utility', backref='ptype', lazy=True)

    def __init__(self, cat_name, cat_id):
        self.cat_name = cat_name
        self.id = cat_id

    def __repr__(self):
        return f"Categories('{self.cat_name}', '{self.id}')"

## Reported problems Tables##


@declarative_mixin
class MyMixin:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def userid(cls):
        return Column(Integer, ForeignKey('user.id'), nullable=False)
    
    @declared_attr
    def type(cls):
        return Column(Integer, ForeignKey('categories.id'), nullable=False)

    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer, primary_key=True)
    type = type
    sub_type = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    geometry = Column((Geometry("POINT", srid=4326, spatial_index=True)))
    effect = Column(Integer)
    description = Column(String)
    img = Column(LargeBinary)
    solved = Column(Boolean, unique=False, default=False)
    solved_time = Column(DateTime)

    def get_point(self):
        return to_shape(self.geometry)

    def __init__(self, type, lat, lon, effect, description, solved,cuusid):
        self.type = type
        self.lat = lat
        self.lon = lon
        self.geometry = from_shape(Point(self.lon, self.lat), srid=4326)
        self.effect = effect
        self.description = description
        # self.img = img
        self.solved = solved
        self.userid = cuusid

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

# Dropping All Tables
# Base.metadata.drop_all(engine, checkfirst=True)

admin.add_views(Controller(User,session),Controller(Categories,session),Controller(Utility,session))
# Creating All Tables
Base.metadata.create_all(engine, checkfirst=True)

# session.add(Pollution(1,30.2,31.1,5,'testoo',False,1))
# session.commit()

# print(session.query(User).all())
# user = session.query(User).get(1)
# print(user.reports)


# This is a query that is looking for the user with the national id of 12345678901111.
# userr = session.query(User).filter_by(national_id='12345678901111').first()

# Getting the user with the id of 3.
# userByGet = session.query(User).get(3)
# print(userByGet)

# print(userr.id)

# print(userByGet.reports)
