import os
import geopandas
from reportit.postgis import postGIS_GDF, saveToGPKGforme
import concurrent.futures
import requests
import json
from dotenv import load_dotenv,find_dotenv

def bestrouteFac(lat=31.36,long=30.07,org='Water'):
    load_dotenv(find_dotenv())
    admin_poly = geopandas.read_file("Data/Facilities/DemoCairo.gpkg", layer='NewCairoPolyDemo').to_crs("EPSG:3857")
    Egy_fac= geopandas.read_file("Data/Facilities/EgyptFacilities.gpkg", layer='facilities').to_crs("EPSG:3857") #Point

    fac_And_Admin = geopandas.sjoin(Egy_fac,admin_poly[['adm3_ar', 'geometry']], how='left')
    fac_And_Admin.rename_geometry('fac_geo', inplace=True)
    fac_And_Admin_for_utility = fac_And_Admin.loc[fac_And_Admin['fclass']=='fire_station']
    toto = fac_And_Admin_for_utility.to_crs("EPSG:4326")
    toto['fac_lat'] = toto['fac_geo'].y
    toto['fac_lon'] = toto['fac_geo'].x
    geometry = geopandas.points_from_xy(toto.fac_lon, toto.fac_lat)

    #facilities list
    geo_df_list = [[point.xy[0][0], point.xy[1][0]] for point in toto.fac_geo]
    lastprob=[float(lat),float(long)]
    print(geo_df_list)
    geo_df_list.insert(0,lastprob)

    z=[]
    for i in range(len(geo_df_list)-1):
        z.append(i+1)

    body = {"locations":geo_df_list,"destinations":[0],"metrics":["distance","duration"],"sources":z,"units":"m"}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': os.getenv('ORS_API_KEY1'),
        'Content-Type': 'application/json; charset=utf-8'
    }
    call = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car', json=body, headers=headers)

    # print(call.status_code, call.reason)
    # print(call.text)
    

    res = json.loads(call.text)
    x=res['durations']
    durationList=[]
    for i in x:
        m=i[0]
        durationList.append(m)
    durationList.sort()
    minDuration=durationList[0]
    print(minDuration)

    index = x.index([minDuration])

    sourceList=res['sources']
    source=sourceList[index]
    closestFac=source['location']

    print(closestFac)

    q=closestFac[1]
    w=closestFac[0]

    r=lastprob[1]
    t=lastprob[0]

    # headers = {
    # 'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    # }
    # call = requests.get('https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf62487ad6039a4daa436d88a8a4ff481a40f9&start={},{}&end={},{}'.format(q,w,r,t), headers=headers)

    call = 'http://www.openstreetmap.org/directions?route={}%2C{}%3B{}%2C{}'.format(q,w,r,t)
    print(call)
    # print(call.status_code, call.reason)
    # print(call.text)


    # with concurrent.futures.ThreadPoolExecutor() as executor:
            # f1 = executor.submit(saveToGPKGforme, fac_And_Admin_for_Problem,'facandadmin')