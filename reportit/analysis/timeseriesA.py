import geopandas
import pandas as pd
from datetime import datetime
import numpy as np
from reportit.postgis import postGIS_GDF
import folium
from folium.plugins import TimeSliderChoropleth

def timeSeriesA(sqlQ):
    #1 Import Data
    # Import GeoDataFrame from PostGIS
    # Problem_gdf = postGIS_GDF(sqlQ)
    # Problem_gdf['timestamp'] = Problem_gdf['timestamp'].astype(str)
    # Problem_gdf = Problem_gdf.to_crs("EPSG:3857")
    Problem_gdf = geopandas.read_file("Data/Facilities/DemoCairoResults.gpkg", layer='Result5').to_crs("EPSG:3857") #Polygon
    # Problem_gdf['adm3_ar'] = Problem_gdf['adm3_ar']
    #Service Area Polygon
    # admin_poly = geopandas.read_file("Data/Facilities/NewCairoPoly.gpkg", layer='NewCairoPoly').to_crs("EPSG:3857") #Polygon
    admin_poly = geopandas.read_file("Data/Facilities/Admin3Poly.gpkg", layer='All-Admin-Area-Egypt').to_crs("EPSG:3857") #Polygon
    # convert datetime to date
    Problem_gdf['timestamp'] = pd.to_datetime(Problem_gdf['timestamp'],format='%Y.%m.%d')
    Problem_gdf['timestamp'] = pd.to_datetime(Problem_gdf['timestamp']).dt.date
    # Make dict to carry admin area name and index id
    cc = admin_poly.copy()
    inv_map = cc['adm3_ar'].to_dict()
    id_dict = {str(v): str(k) for k,v in inv_map.items()}

    
    Problem_gdf['Admin_id'] = Problem_gdf['adm3_ar'].map(id_dict)

    listiss = Problem_gdf['timestamp'].tolist()
    counter = 0
    for l in listiss:
        Problem_gdf['timestamp'][counter] = datetime.strptime(str(l),'%Y-%m-%d').timestamp()
        counter += 1
    Problem_gdf['timestamp']=(Problem_gdf['timestamp'].astype(str))
    poll_dict={}
    for i in Problem_gdf['Admin_id'].unique():
        poll_dict[i]={}
        for j in Problem_gdf[Problem_gdf['Admin_id']==i].set_index(['Admin_id']).values:
            poll_dict[i][j[0]]={'color':j[1],'opacity':0.7}

    bins=np.linspace(min(Problem_gdf['effect']),max(Problem_gdf['effect']),5)

    # Coloring Admin with pollution
    Problem_gdf['color']=pd.cut(Problem_gdf['effect'],bins,labels=['#EBA1A8','#DE6F7C','#D13E50','#C50D24'],include_lowest=False)
    # Coloring Admin without pollution
    Problem_gdf['color'].replace(np.nan,'#32CD32',inplace=True)

    Problem_gdf=Problem_gdf[['timestamp','Admin_id','color']]

    

    for date in Problem_gdf['timestamp'].unique():
        diff=set([str(i) for i in range(18)])-set(Problem_gdf[Problem_gdf['timestamp']==date]['Admin_id'])
        for i in diff:
            Problem_gdf=pd.concat([Problem_gdf,pd.DataFrame([[date,'#0073CF',i]],columns=['timestamp','color','Admin_id'])],ignore_index=True)
    Problem_gdf.sort_values('timestamp',inplace=True)

    Problem_gdf['timestamp']=(Problem_gdf['timestamp'].astype(str))
    poll_dict={}
    for i in Problem_gdf['Admin_id'].unique():
        poll_dict[i]={}
        for j in Problem_gdf[Problem_gdf['Admin_id']==i].set_index(['Admin_id']).values:   
            poll_dict[i][j[0]]={'color':j[1],'opacity':0.7}


    

    admin_poly['Admin_id']=admin_poly['adm3_ar'].map(id_dict)
    admin_poly.drop(columns='adm3_ar',inplace=True)
    
    fig6= folium.Figure()
    m6 = folium.Map([30.113651776114697, 31.50192260742187], tiles='cartodbpositron', zoom_start=11)
    fig6.add_child(m6)
    g = TimeSliderChoropleth(
        admin_poly.set_index('Admin_id').to_json(),
        styledict=poll_dict
    ).add_to(m6)
    return m6

