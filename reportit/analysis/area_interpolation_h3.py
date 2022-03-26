import geopandas
import libpysal
from tobler.util import h3fy
from tobler.area_weighted import area_interpolate

def area_interpolation_h3():
    dc = geopandas.read_file('Data/Facilities/pol1.zip').to_crs("EPSG:3857") #Polygon
    dc_hex_clipped = h3fy(dc, resolution=5, clip=True)
    dc_hex_interpolated = area_interpolate(source_df=dc, target_df=dc_hex_clipped, intensive_variables=['PM2.5'])
    return dc_hex_interpolated
