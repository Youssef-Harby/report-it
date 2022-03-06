from tabnanny import check
from flask import request
from numpy import integer
from reportit import Base, engine,session
from sqlalchemy import Column, Integer, String, Float, Date
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2 import Geometry
from shapely.geometry import Point
from datetime import date, datetime

##USER TABLE##
class user_info (Base):
    __tablename__='user_info'
    id = Column('id', Integer,primary_key= True )
    f_Name= Column('First_Name', String)
    l_Name= Column('Last_Name', String)
    email=Column('E-mail', String)
    National_ID= Column('National_ID',String )
    phone_num=Column('Phone_Number', String)

    ## initializing
    def __ini__(self,id,f_Name,l_Name,email,National_ID,phone_num):
        self.id= id
        self.f_Name= f_Name
        self.l_Name= l_Name
        self.email= email
        self.National_ID= National_ID
        self.phone_num=phone_num

##Categories ID##
class categories (Base):
    __tablename__= 'categories'

    cat_name= Column('Category_Name', String, primary_key= True)
    cat_id = Column('Category_id', Integer)

    def __ini__(self, cat_name,cat_id):
        self.cat_name= cat_name
        self.cat_id= cat_id

## Reported problems Tables##
class Utility_table(Base):
    __tablename__='Utility_table'

    prop_id= Column('id', Integer, primary_key= True)
    type= Column('type',Integer)
    lat= Column('lat', Float)
    long= Column('long', Float)
    timeStamp= Column('Time_stamp', Date)
    Geometry= Column((Geometry("POINT", srid=4326, spatial_index=True)))
    effect= Column('Effect', Integer)
    description= Column('Description', String)
    img=Column('img', type_=String )
    user_id= Column('user_id', Integer)

    def __init__(self, prop_id, type, lat, long, timeStamp, Geometry, effect, description, img, user_id):
        self.prop_id=prop_id
        self.type= type
        self.lat= lat
        self.long= long
        self.timeStamp=timeStamp
        self.Geometry= Geometry
        self.effect= effect
        self.description= description
        self.img = img
        self.user_id=user_id



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