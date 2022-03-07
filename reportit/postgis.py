import geopandas
from reportit import engine

sql_utility = 'SELECT * FROM public.utility'
df_utility = geopandas.read_postgis(sql_utility, engine, geom_col='geometry')

sql_user = 'SELECT * FROM public."user"'
# df_user = geopandas.read_postgis(sql_utility, engine, geom_col='geometry')