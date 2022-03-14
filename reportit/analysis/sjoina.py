import geopandas
from reportit.postgis import postGIS_GDF

# Spacial Join (Problem Query from DB , Facilities Layer Name/QDB , Service Area Polygon)
def sJoinA():
    #1 Import Data
    # Import GeoDataFrame from PostGIS
    Problem_gdf = postGIS_GDF()
    Problem_gdf['timestamp'] = Problem_gdf['timestamp'].astype(str)
    Problem_gdf = Problem_gdf.to_crs("EPSG:3857")

    #Facilities Layer From GPKG or PostGIS
    facilities = geopandas.read_file("https://raw.githubusercontent.com/Youssef-Harby/report-it/main/Data/Facilities/DemoCairo.gpkg", layer='facilities').to_crs("EPSG:3857") #Point

    #Service Area Polygon
    admin_poly = geopandas.read_file("https://raw.githubusercontent.com/Youssef-Harby/report-it/main/Data/Facilities/DemoCairo.gpkg", layer='NewCairoPolyDemo').to_crs("EPSG:3857") #Polygon

    #Spatial Join (Facilities and Service Area Polygon)
    fac_And_Admin = geopandas.sjoin(facilities,admin_poly[['adm3_ar', 'geometry']], how='left')
    fac_And_Admin.rename_geometry('fac_geo', inplace=True)
    type_name = ['Fire','Health','Road','Utility']
    fac_And_Admin_for_Problem = fac_And_Admin.loc[fac_And_Admin['type']==type_name[0]]

    #Add lat and lon from geometry column
    fac_And_Admin_for_Problem = fac_And_Admin_for_Problem.to_crs("EPSG:4326")
    fac_And_Admin_for_Problem['fac_lat'] = fac_And_Admin_for_Problem['fac_geo'].y
    fac_And_Admin_for_Problem['fac_lon'] = fac_And_Admin_for_Problem['fac_geo'].x

    #
    problem_And_Admin = geopandas.sjoin(Problem_gdf,admin_poly[['adm3_ar', 'geometry']], how='left')

    final_result = problem_And_Admin.merge(fac_And_Admin_for_Problem[['fac_lat','fac_lon','adm3_ar']], on='adm3_ar',how='left').to_crs("EPSG:4326")
    final_result['lat'] = final_result['geometry'].y
    final_result['lon'] = final_result['geometry'].x

    return final_result

