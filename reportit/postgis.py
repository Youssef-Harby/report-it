import geopandas
from reportit import engine

sql = 'SELECT * FROM public."Utility_table"'
df = geopandas.read_postgis(sql, engine, geom_col='geometry')