from flask import render_template, request, url_for
from reportit import app, session
import folium
from folium import plugins
import geopandas
import leafmap.kepler as leafmap
from reportit.form import *

myReports = [
    {
        'author': 'Youssef Harby',
        'problem': 'Pipeline Break',
        'description': 'Description Test 1',
        'date_reported': '11-03-2022',
        'status': True

    },
    {
        'author': 'Khalid',
        'problem': 'Noise Pollution',
        'description': 'Description Test 2',
        'date_reported': '10-03-2022',
        'status': False

    }
]


@app.route('/')
def index():
    return render_template('index.html', projectName='Report-it')


@app.route('/form')
def formPage():
    return render_template('form.html')


@app.route('/folium')
def maptest():
    from reportit.postgis import df_utility
    # print(df.info())
    geometry = geopandas.points_from_xy(df_utility.lon, df_utility.lat)
    geo_df = geopandas.GeoDataFrame(
        df_utility[['id', 'description', 'lat', 'lon', 'timestamp']], geometry=geometry)
    print(geo_df.head())
    # Create a geometry list from the GeoDataFrame
    geo_df_list = [[point.xy[1][0], point.xy[0][0]]
                   for point in geo_df.geometry]
    # print(geo_df_list)

    start_coords = (30.0444, 31.2357)
    folium_map = folium.Map(location=start_coords, zoom_start=6)
    plugins.HeatMap(geo_df_list).add_to(folium_map)
    # return df.keys()
    return folium_map._repr_html_()


@app.route('/leafmap')
def leafmapTest():
    from reportit.postgis import df_utility
    m = leafmap.Map(center=[30.0444, 31.2357], zoom=6,
                    height=600, widescreen=False)
    geometry = geopandas.points_from_xy(df_utility.lon, df_utility.lat)
    geo_df = geopandas.GeoDataFrame(
        df_utility[['id', 'description', 'lat', 'lon']], geometry=geometry)
    print(geo_df.head())
    m.add_gdf(geo_df, layer_name="Points",
              fill_colors=["red", "green", "blue"])
    # m.to_html(outfile='./reportit/templates/leafmap.html')
    return m._repr_html_()


@app.route('/submission')
def submission():
    return render_template('submission.html')


@app.route('/jsontest', methods=['POST'])
def jsontestpost():
    data = request.get_json()
    # print(data)
    session.add(User(data["First Name"], data["Last Name"], data["Email"], data["National Id"], data["phone"]))
    session.commit()
    session.add(Utility(1, float(data['lat']), float(data['lng']), int(data["Intensity Range"]), data['Description'],True,3))
    session.commit()
    return url_for('submission')


@app.route('/map')
def maptesto():
    return render_template('map.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/myreports')
def myreports():
    return render_template('myreports.html', reports=myReports)

@app.route('/about')
def about():
    return render_template('about.html', reports=myReports)