print("F1")
from reportit import *
from reportit import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2 import Geometry
from shapely.geometry import Point
from datetime import datetime

class Form(Base):
    __tablename__ = 'water1'
    
    fid = Column(Integer, primary_key=True)
    Description = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(DateTime)
    geometry = Column((Geometry("POINT", srid=4326, spatial_index=True)))

    def __init__(self, fid, description, lat, lon):
        self.fid = fid
        self.Description = description
        self.lat = lat
        self.lon = lon
        self.timestamp = str(datetime.utcnow())
        self.geometry = from_shape(Point(self.lon, self.lat), srid=4326)

    def get_point(self):
        return to_shape(self.geometry)

Form.__table__.create(engine)