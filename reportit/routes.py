from flask import render_template, request
from reportit import app, df
import folium
from folium import plugins
import geopandas
from reportit.form import *

@app.route('/')
def index():
    return render_template('form.html')

# print(df.info())
geometry = geopandas.points_from_xy(df.lon, df.lat)
geo_df = geopandas.GeoDataFrame(df[['fid','Description', 'lat', 'lon', 'timestamp']], geometry=geometry)
# geo_df.head()
# Create a geometry list from the GeoDataFrame
geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in geo_df.geometry ]
print(geo_df_list)

@app.route('/folium')
def maptest():
    start_coords = (30.0444, 31.2357)
    folium_map = folium.Map(location=start_coords, zoom_start=8)
    plugins.HeatMap(geo_df_list).add_to(folium_map)
    # return df.keys()
    return folium_map._repr_html_()