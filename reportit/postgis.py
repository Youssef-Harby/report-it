import os
import geopandas
import leafmap
from dotenv import load_dotenv, find_dotenv
from reportit import engine

from reportit.models import Categories

ACCESS = {
    'guest': 0,
    'user': 1,
    'waterORG': 2,
    'sewageORG': 3,
    'gasORG': 4,
    'electricORG': 5,
    'telecomORG': 6,
    'pollutionORG': 7,
    'roadORG': 8,
    'disasterORG': 9,
    'utilityORG': 10,
    'admin': 666,
}

load_dotenv(find_dotenv())
# sql_utility = 'SELECT u.id, u.sub_type, u.lat, u.lon, u.timestamp, u.geometry, u.effect, u.description, u.solved, u.solved_time FROM public.utility'


def current_qry_url(accessuser_access):
    if accessuser_access == ACCESS['waterORG']:
        sql_Q = "SELECT u.id, c.cat_name, u.sub_type, u.lat, u.lon, u.timestamp, u.geometry, u.effect, u.description, u.solved, u.solved_time FROM public.utility u INNER JOIN public.categories c ON c.id=u.type where c.cat_name='Water'"
        # rel_type = session.query(Categories).filter_by(cat_name="Water").first().type
    if accessuser_access == ACCESS['sewageORG']:
        sql_Q = "SELECT u.id, c.cat_name, u.sub_type, u.lat, u.lon, u.timestamp, u.geometry, u.effect, u.description, u.solved, u.solved_time FROM public.utility u INNER JOIN public.categories c ON c.id=u.type where c.cat_name='Sewage'"
        # rel_type = session.query(Categories).filter_by(cat_name="Sewage").first().type
    if accessuser_access == ACCESS['gasORG']:
        sql_Q = "SELECT u.id, c.cat_name, u.sub_type, u.lat, u.lon, u.timestamp, u.geometry, u.effect, u.description, u.solved, u.solved_time FROM public.utility u INNER JOIN public.categories c ON c.id=u.type where c.cat_name='Gas'"
        # rel_type = session.query(Categories).filter_by(cat_name="Gas").first().type
    if accessuser_access == ACCESS['electricORG']:
        sql_Q = "SELECT u.id, c.cat_name, u.sub_type, u.lat, u.lon, u.timestamp, u.geometry, u.effect, u.description, u.solved, u.solved_time FROM public.utility u INNER JOIN public.categories c ON c.id=u.type where c.cat_name='Electric'"
        # rel_type = session.query(Categories).filter_by(cat_name="Electric").first().type
    if accessuser_access == ACCESS['telecomORG']:
        sql_Q = "SELECT u.id, c.cat_name, u.sub_type, u.lat, u.lon, u.timestamp, u.geometry, u.effect, u.description, u.solved, u.solved_time FROM public.utility u INNER JOIN public.categories c ON c.id=u.type where c.cat_name='Telecom'"
        # rel_type = session.query(Categories).filter_by(cat_name="Telecom").first().type
    if accessuser_access == ACCESS['pollutionORG']:
        sql_Q = "SELECT * FROM public.pollution"
    if accessuser_access == ACCESS['roadORG']:
        sql_Q = "SELECT * FROM public.road"
        # rel_type = session.query(Categories).filter_by(cat_name="Gas").first().type_Road
    if accessuser_access == ACCESS['disasterORG']:
        sql_Q = "SELECT * FROM public.disaster"
        # rel_type = session.query(Categories).filter_by(cat_name="Disasters").first().type_Disaster
    if accessuser_access == ACCESS['utilityORG']:
        sql_Q = "SELECT * FROM public.utility"
        # rel_type = session.query(Categories).filter_by(cat_name="Disasters").first().type_Disaster
    return sql_Q


# sql_user = 'SELECT u.id, u.sub_type, u.lat, u.lon, u.timestamp, u.geometry, u.effect, u.description, u.solved, u.solved_time FROM public."user"'
# df_user = geopandas.read_postgis(sql_utility, engine, geom_col='geometry')
def readpostpandas(sql_Q):
    df_current = geopandas.read_postgis(sql_Q, engine, geom_col='geometry')
    return df_current


con = leafmap.connect_postgis(database=os.getenv('DATABASE'), host=os.getenv(
    'DBHOST'), user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD'))


def postGIS_GDF(sqlQ):
    gdf = leafmap.read_postgis(sqlQ, con, geom_col='geometry')
    return gdf


def saveToGPKGforme(gdf,Result):
    gdf.to_file('Data/Facilities/DemoCairoResults.gpkg', driver='GPKG', layer=Result)