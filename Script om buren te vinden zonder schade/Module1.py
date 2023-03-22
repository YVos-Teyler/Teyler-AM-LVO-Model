# Created on 15/10/2022
# Author: Yoeri Vos
# Function: In deze module wordt op basis van maatgevende schades per 100 meter vakken werkpakket voorstellen gemaakt

import pandas as pd
import geopandas as gpd
from shapely.validation import make_valid, explain_validity
import numpy as np
from tqdm import tqdm
import os

os.chdir("C:/Users/YoeriVosTEYLER/TEYLER consultancy/TEYLER projects - F. Data Solutions/98 Scripts/Teyler-AM-LVO-Model/Script om buren te vinden zonder schade")
filename = "A1_links_all_roads.geojson"
vakken_dataset = gpd.read_file(filename, driver="geojson")

#check if geometry is valid and try to fix it
valid_of_niet = vakken_dataset.geometry.is_valid
valid_of_niet = valid_of_niet[valid_of_niet == False]
print(valid_of_niet)


for index in valid_of_niet.index:
     print(vakken_dataset.loc[index, 'uuid'])
     make_valid(vakken_dataset.loc[index, 'geometry'])

#nog een x checken na de make valid statement om alle niet valid secties te droppen
valid_of_niet = vakken_dataset.geometry.is_valid
valid_of_niet = valid_of_niet[valid_of_niet == False]
index_niet_valid = valid_of_niet.index

vakken_dataset.drop(index_niet_valid, inplace=True)

vakken_dataset["neighbour_damage_uuids"] = " "
vakken_dataset = vakken_dataset.reset_index(drop = True)
vakken_dataset_copy = vakken_dataset.copy()
vakken_dataset_pandas = pd.DataFrame(vakken_dataset, copy=True)
#schade_dataset_pandas["neighbour_damage_uuids"] = [[] for _ in range(len(schade_dataset_pandas))]

#start progress bar
length_dataset = len(vakken_dataset)
save_every_x_iterations = length_dataset/5
pbar = tqdm(desc= 'Data clean', total = length_dataset )
n=0



#make a matches column for the uuids
vakken_dataset_pandas['matches'] = None
vakken_dataset_pandas['extra_info'] = None
#make a list for all the matches with same length as the df
#matches = [[] for _ in range(len(schade_dataset))]
extra_info = [[] for _ in range(len(vakken_dataset))]
matches = [[] for _ in range(len(vakken_dataset))]
for index, item in vakken_dataset.iterrows():
     
     pbar.update(1)
     #update n om iedere x iteraties op te slaan
     n += 1
     n_matches = 0
     geo1 = item['geometry']
     for index_copy, item2 in vakken_dataset_copy.iterrows():
          geo2 = item2['geometry']
          
          #moet niet zichzelf als buur toevoegen
          if(item['uuid'] != item2['uuid'] ):
               try:
                    #als wegvak aan een ander wegvak grenst met schade (inclusief diagonalen)
                    if(geo1.touches(geo2)):
                         intersect_info = geo1.intersection(geo2)
                         if intersect_info.boundary:
                              matches[index].append(item2['uuid'])
                              extra_info[index].append([vakken_dataset_copy.loc[index_copy, 'road_number'],
                                                       vakken_dataset_copy.loc[index_copy,'lane_type_letter'],
                                                       vakken_dataset_copy.loc[index_copy, 'lane'],
                                                       vakken_dataset_copy.loc[index_copy, 'hm_from'],
                                                       vakken_dataset.loc[index_copy, 'hm_to'],
                                                       item2['uuid']])
                              n_matches += 1
                              if n_matches == 4:
                                   print('Matched all 4, breaking the for loop!')
                                   break
               except:
                    print('')
                    print('geometry probably not valid')
                    print('uuid: ' + str(item2['uuid']))

     #sla iedere x iteraties een versie op
     if n >= save_every_x_iterations:
          #zet de lijst van matches in de kolom
          vakken_dataset_pandas['matches'] = matches
          vakken_dataset_pandas['extra_info'] = extra_info
          #schade_dataset['matches'] = matches
          n = 0
          #schade_dataset.to_file("meting_met_uuids_buurschade.geojson", driver='GeoJSON')
          vakken_dataset_pandas.to_excel('excel_buurschade.xlsx')
          vakken_dataset_pandas.to_json('json_buurschade.json', default_handler=str)
          print("\n Saved!")
pbar.close()


