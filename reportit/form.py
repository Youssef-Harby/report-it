from flask import request
from reportit import Base, engine,session
from sqlalchemy import Column, Integer, String, Float, DateTime
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2 import Geometry
from shapely.geometry import Point
from datetime import datetime

class FormToDB(Base):
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

    def get_current_weather(self):
        url = f"https://api.weather.gov/points/{self.lat},{self.lon}"
        r = request.get_json(url)
        if not r.ok:
            return None
        # r = request.get(r.json()['properties']['forecast'])
        # return r.json()['properties']['periods'][0] if 'properties' in r.json() else None

# Run once table created
FormToDB.__table__.create(engine, checkfirst=True)

# session.add(FormToDB(3,"Test 4",27.1783, 31.1859))
# session.commit()
