import geopandas
from reportit.postgis import postGIS_GDF,saveToGPKGforme
import concurrent.futures

def countPinPoly(sqlQ):
    #1 Import Data
    # Import GeoDataFrame from PostGIS
    Problem_gdf = postGIS_GDF(sqlQ)
    Problem_gdf['timestamp'] = Problem_gdf['timestamp'].astype(str)
    Problem_gdf = Problem_gdf.to_crs("EPSG:3857")

    #Service Area Polygon
    admin_poly = geopandas.read_file("Data/Facilities/Admin3Poly.gpkg", layer='All-Admin-Area-Egypt').to_crs("EPSG:3857") #Polygon
    admin_poly["idforcount"] = admin_poly.index + 1

    Problem_And_Admin = geopandas.sjoin(Problem_gdf,admin_poly, how='inner',op='intersects',)

    com_dist_count_problem_locs = Problem_And_Admin.groupby(
    ['idforcount'],
    as_index=False,
    )['id'].count()
    # groupby to count the wifi locations in each community district
    # arbitrarily count the rows for doitt_id
    com_dist_count_problem_locs.columns = ['idforcount', 'count']
    # rename the column

    com_dists_problem_counts = admin_poly.merge(
    com_dist_count_problem_locs,
    on='idforcount',
    how='left',
    )

    com_dists_problem_counts.isnull().sum()

    

    com_dists_problem_counts['count'].fillna(
        0, 
        inplace=True,
    )

    with concurrent.futures.ThreadPoolExecutor() as executor:
            f1 = executor.submit(saveToGPKGforme, com_dists_problem_counts,'count1')
    return com_dists_problem_counts