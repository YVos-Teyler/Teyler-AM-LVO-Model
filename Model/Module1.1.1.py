import geopandas as gpd
import pandas as pd

# df_met_buurschade = pd.read_excel('excel_buurschade - Copy.xlsx')
# df_met_buurschade.columns = df_met_buurschade.columns.str.lower()
# df_met_buurschade['matches'] = df_met_buurschade['matches'].str.replace("'", '').str.replace('[', '').str.replace(']', '')
# df_met_buurschade['matches'] = df_met_buurschade['matches'].str.split(',').apply(lambda x: [uuid for uuid in x])

filename = 'rewound-geojson.json'
geodf = gpd.read_file(filename, driver = 'GeoJSON' )

geodf['neighbour_damage_uuids'] = geodf['neighbour_damage_uuids'].str.replace("'", '', regex=False).str.replace('[', '', regex=False).str.replace(']', '', regex=False).str.replace('  ', '', regex=False)
geodf['neighbour_damage_uuids'] = geodf['neighbour_damage_uuids'].str.split(' ').apply(lambda x: [uuid for uuid in x])

geodf['middenvoor_buur'] = None
geodf['middenachter_buur'] = None
geodf['links_buur'] = None
geodf['rechts_buur'] = None

for index, item in geodf.iterrows():

    geometry1 = item['geometry']
    for uuid in item['neighbour_damage_uuids']:
        for index2, item2 in geodf.iterrows():
            
            #print(item2['uuid'])
            if  uuid == item2['uuid']:
                print('gematchte uuid:' + str(item2['uuid']))
                print(geometry1.touches(item2['geometry']))
                intersect_info = geometry1.intersection(item2['geometry'])
                if intersect_info.boundary:
                    print(intersect_info.boundary)

                
                # boundary = geometry1.intersection(item2['geometry']).boundary
                # # Calculate the length or area of the shared boundary
                # length = boundary.length
                # area = boundary.area
                # print('length: ' + str(length))
                # print('area: ' + str(area))   
                
                
            
    break
            

# # Loop over each row in geodf
# for idx, row in geodf.iterrows():
#     uuid = row['uuid']
#     geom = row['geometry']
    
#     # Find all rows in geodf that have the same UUID and a different index
#     matching_rows = geodf[(geodf['uuid'] == uuid)]
    
#     # Loop over the matching rows and calculate the intersection area
#     for _, match in matching_rows.iterrows():
#         intersection = gpd.overlay(row.to_frame().T, match.to_frame().T, how='intersection')
#         intersection_area = intersection.area[0]
#         print(intersection_area)

#         # # Store the intersection area in the 'intersection_area' column of both rows
#         # geodf.at[idx, 'intersection_area'] += intersection_area
#         # geodf.at[match.name, 'intersection_area'] += intersection_area