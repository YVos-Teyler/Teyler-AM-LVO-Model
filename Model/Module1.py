# Created on 15/10/2022
# Author: Yoeri Vos
# Function: In deze module wordt op basis van maatgevende schades per 100 meter vakken werkpakket voorstellen gemaakt

import pandas as pd
import geopandas as gpd
from shapely.validation import make_valid, explain_validity
import numpy as np
from tqdm import tqdm
import os

os.chdir("C:/Users/YoeriVosTEYLER/TEYLER consultancy/TEYLER projects - F. Data Solutions/98 Scripts/Teyler-AM-LVO-Model")
filename = "20220927 Meting RWS/WNN verhardingsinspectie 2022.geojson"
schade_dataset = gpd.read_file(filename, driver="geojson")


#alle kolommen die niet van toepassing zijn weggooien
#uuid kolom staat er 2 x in
schade_dataset.pop('uuid')
schade_dataset.columns = schade_dataset.columns.str.lower()
schade_dataset.maatgevende_schadeklasse = schade_dataset.maatgevende_schadeklasse.str.lower()
schade_dataset.maatgevende_schadeklasse = schade_dataset.maatgevende_schadeklasse.replace('geen', '0')
schade_dataset.maatgevende_schadeklasse = schade_dataset.maatgevende_schadeklasse.replace('niet onderzocht', '0')
schade_dataset.maatgevende_schadeklasse = schade_dataset.maatgevende_schadeklasse.replace('onbruikbaar', '0')


#deelstreep geen onderhoud aan doen
schade_dataset = schade_dataset.loc[schade_dataset["strooksoor"].str.lower() != "deelstreep"]
schade_dataset = schade_dataset.loc[schade_dataset["maatgevende_schadeklasse"] != "0"]


#idee: stukjes weg opdelen per wegnummer om filter sneller te maken, heb je alleen de overgangen niet
#idee: overgangen kun je checken door verbindingswegen te filteren 
#idee: kan ook op links/rechts gefilterd worden
#idee: of filteren op basis van locatie binnen 200m van center punt 100m deel


#check if geometry is valid and try to fix it
valid_of_niet = schade_dataset.geometry.is_valid
valid_of_niet = valid_of_niet[valid_of_niet == False]
print(valid_of_niet)


for index in valid_of_niet.index:
     print(schade_dataset.loc[index, 'uuid'])
     make_valid(schade_dataset.loc[index, 'geometry'])

#nog een x checken na de make valid statement om alle niet valid secties te droppen
valid_of_niet = schade_dataset.geometry.is_valid
valid_of_niet = valid_of_niet[valid_of_niet == False]
index_niet_valid = valid_of_niet.index

schade_dataset.drop(index_niet_valid, inplace=True)

schade_dataset["neighbour_damage_uuids"] = " "
schade_dataset = schade_dataset.reset_index(drop = True)
schade_dataset_copy = schade_dataset.copy()
schade_dataset_pandas = pd.DataFrame(schade_dataset, copy=True)
#schade_dataset_pandas["neighbour_damage_uuids"] = [[] for _ in range(len(schade_dataset_pandas))]

#start progress bar
length_dataset = len(schade_dataset)
save_every_x_iterations = length_dataset/5
pbar = tqdm(desc= 'Data clean', total = length_dataset )
n=0



#make a matches column for the uuids
schade_dataset_pandas['matches'] = None
schade_dataset_pandas['extra_info'] = None
#make a list for all the matches with same length as the df
#matches = [[] for _ in range(len(schade_dataset))]
extra_info = [[] for _ in range(len(schade_dataset))]

for index, item in schade_dataset.iterrows():
     
     pbar.update(1)
     #update n om iedere x iteraties op te slaan
     n += 1

     for index_copy, item2 in schade_dataset_copy.iterrows():
          

          #als wegvak aan een ander wegvak grenst met schade (inclusief diagonalen)
          if(item['geometry'].touches(item2['geometry'])):
               #moet niet zichzelf als buur toevoegen
               if(item['uuid'] != item2['uuid'] ):
               
                    #matches[index].append(item2['uuid'])
                    extra_info[index].append([schade_dataset_copy.loc[index_copy, 'wegnummer'], schade_dataset_copy.loc[index_copy,'strooksoor'], schade_dataset_copy.loc[index_copy, 'strookvolg'], schade_dataset_copy.loc[index_copy, 'hm_van'], schade_dataset_copy.loc[index_copy, 'hm_tot'],  schade_dataset_copy.loc[index_copy, 'maatgevende_schadeklasse'], item2['uuid']])


     #sla iedere x iteraties een versie op
     if n >= save_every_x_iterations:
          #zet de lijst van matches in de kolom
          #schade_dataset_pandas['matches'] = matches
          schade_dataset_pandas['extra_info'] = extra_info
          #schade_dataset['matches'] = matches
          n = 0
          #schade_dataset.to_file("meting_met_uuids_buurschade.geojson", driver='GeoJSON')
          schade_dataset_pandas.to_excel('excel_buurschade.xlsx')
          schade_dataset_pandas.to_json('json_buurschade.json', default_handler=str)
          print("\n Saved!")
pbar.close()


