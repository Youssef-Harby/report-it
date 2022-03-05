import geopandas
from reportit import engine

sql = "SELECT * FROM public.water1"
df = geopandas.read_postgis(sql, engine, geom_col='geometry')