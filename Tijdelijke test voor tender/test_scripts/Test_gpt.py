import pandas as pd
import geopandas as gpd


jsongeo = gpd.read_file('Datasets/Vakkenbestand WNN.geojson')

result = jsongeo[(jsongeo['road_number'] == "1") & (jsongeo['roadway_direction_letter'] == "L")]

result.to_file('A1_links_all_roads.geojson', driver='GeoJSON')