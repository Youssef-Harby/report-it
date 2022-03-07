from reportit import Base, engine
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime,LargeBinary
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2 import Geometry
from shapely.geometry import Point
from datetime import datetime
from sqlalchemy.orm import backref, relationship

##USER TABLE##


class Users (Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    f_Name = Column(String)
    l_Name = Column(String)
    email = Column(String)
    national_id = Column(Integer)
    phone_num = Column(Integer)

    # initializing
    def __ini__(self, f_Name, l_Name, email, National_ID, phone_num):
        self.f_Name = f_Name
        self.l_Name = l_Name
        self.email = email
        self.National_ID = National_ID
        self.phone_num = phone_num

##Categories ID##


class Categories (Base):
    __tablename__ = 'categories'

    cat_name = Column(String)
    id = Column(Integer, primary_key=True)

    def __ini__(self, cat_name, cat_id):
        self.cat_name = cat_name
        self.id = cat_id

## Reported problems Tables##


class Utility(Base):
    __tablename__ = 'utility'
    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(DateTime)
    geometry = Column((Geometry("POINT", srid=4326, spatial_index=True)))
    effect = Column(Integer)
    description = Column(String)
    img = Column(LargeBinary)
    cat_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship("Categories", backref="categories")


    def __init__(self, type, lat, lon, effect, description):
        self.type = type
        self.lat = lat
        self.lon = lon
        self.timestamp = str(datetime.utcnow())
        self.geometry = from_shape(Point(self.lon, self.lat), srid=4326)
        self.effect = effect
        self.description = description
        # self.img = img
        #self.user_id = user_id

    def get_point(self):
        return to_shape(self.geometry)

##Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine, checkfirst=True)


##

# class FormToDB(Base):
#     __tablename__ = 'water1'

#     fid = Column(Integer, primary_key=True)
#     Description = Column(String)
#     lat = Column(Float)
#     lon = Column(Float)
#     timestamp = Column(Date)
#     geometry = Column((Geometry("POINT", srid=4326, spatial_index=True)))

#     def __init__(self, fid, description, lat, lon):
#         self.fid = fid
#         self.Description = description
#         self.lat = lat
#         self.lon = lon
#         self.timestamp = str(datetime.utcnow())
#         self.geometry = from_shape(Point(self.lon, self.lat), srid=4326)

#     def get_point(self):
#         return to_shape(self.geometry)

#     def get_current_weather(self):
#         url = f"https://api.weather.gov/points/{self.lat},{self.lon}"
#         r = request.get_json(url)
#         if not r.ok:
#             return None
#         # r = request.get(r.json()['properties']['forecast'])
#         # return r.json()['properties']['periods'][0] if 'properties' in r.json() else None


# # Run once table created
# FormToDB.__table__.create(engine,checkfirst=True)

# session.add(FormToDB(1,"Test 4",27.1, 31.1))
# session.commit()
# Print
