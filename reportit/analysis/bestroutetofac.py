import os
import geopandas
import openrouteservice
from flask_mail import Message
from reportit import mail
from dotenv import load_dotenv,find_dotenv

def send_reset_email(osm_url):
    msg = Message('New Report for You',
                  sender='noreply@mail.georeportit.me',
                  recipients=['org1@mail.georeportit.me'])
    msg.body = f'''To go to the problem, visit the following link:
{osm_url}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def bestrouteFac(lat,long):
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
    # print(geo_df_list)
    geo_df_list.insert(0,lastprob)

    z=[]
    for i in range(len(geo_df_list)-1):
        z.append(i+1)

    from openrouteservice.distance_matrix import distance_matrix
    coords = geo_df_list
    client = openrouteservice.Client(key='5b3ce3597851110001cf624837171f649f514342afd86d5ca248cfd0') # Specify your personal API key
    routes = client.distance_matrix(coords,profile='driving-car',sources=z,destinations=[0],metrics=None,resolve_locations=None,units=None,optimized=None,validate=True,dry_run=None)

    # print(routes)

    res = routes
    x=res['durations']
    durationList=[]
    for i in x:
        m=i[0]
        durationList.append(m)
    durationList.sort()
    minDuration=durationList[0]
    # print(minDuration)

    index = x.index([minDuration])

    sourceList=res['sources']
    source=sourceList[index]
    closestFac=source['location']

    # print(closestFac)

    q=closestFac[1]
    w=closestFac[0]

    r=lastprob[1]
    t=lastprob[0]

    call = 'http://www.openstreetmap.org/directions?route={}%2C{}%3B{}%2C{}'.format(q,w,r,t)
    # print(call)
    send_reset_email(call)
