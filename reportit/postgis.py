import geopandas
from reportit import engine

sql = 'SELECT * FROM public.utility'
df = geopandas.read_postgis(sql, engine, geom_col='geometry')