import os
import geopandas
import leafmap
from dotenv import load_dotenv,find_dotenv
from reportit import engine

load_dotenv(find_dotenv())
sql_utility = 'SELECT * FROM public.utility'
df_utility = geopandas.read_postgis(sql_utility, engine, geom_col='geometry')
con = leafmap.connect_postgis(database=os.getenv('DATABASE'), host=os.getenv('DBHOST'), user=os.getenv('DBUSER'), password=os.getenv('DBPASSWORD'))

# sql_user = 'SELECT * FROM public."user"'
# df_user = geopandas.read_postgis(sql_utility, engine, geom_col='geometry')
def postGIS_GDF():
    sql_water = 'SELECT * FROM public.utility'
    gdf = leafmap.read_postgis(sql_water, con, geom_col='geometry')
    return gdf