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

bool_alle_schade_aansluitend = True

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
schade_dataset_copy = schade_dataset.copy()

#idee: stukjes weg opdelen per wegnummer om filter sneller te maken, heb je alleen de overgangen niet
#idee: overgangen kun je checken door verbindingswegen te filteren 
#idee: kan ook op links/rechts gefilterd worden
#idee: of filteren op basis van locatie binnen 200m van center punt 100m deel




valid_of_niet = schade_dataset.geometry.is_valid
valid_of_niet = valid_of_niet[valid_of_niet == False]

for index in valid_of_niet.index:
     make_valid(schade_dataset.loc[index, 'geometry'])
     print("done")

valid_of_niet = schade_dataset.geometry.is_valid
valid_of_niet = valid_of_niet[valid_of_niet == False]
print(valid_of_niet)

schade_dataset["neighbour_damage_uuids"] = " "


#start progress bar
length_dataset = len(schade_dataset)
save_every_x_iterations = length_dataset/100
pbar = tqdm(desc= 'Data clean', total = length_dataset )
n=0

for index, item in schade_dataset.iterrows():
     pbar.update(1)
     n += 1
     uuid_touch_list = []


     for index_copy, item in schade_dataset_copy.iterrows():
          if(schade_dataset.loc[index, 'geometry'].touches(schade_dataset_copy.loc[index_copy, 'geometry'])):
               if(schade_dataset.loc[index, 'uuid'] != schade_dataset.loc[index_copy, 'uuid'] ):
                    schade_dataset.loc[index, 'neighbour_damage_uuids'] = schade_dataset.loc[index_copy, 'neighbour_damage_uuids'] + " " + schade_dataset_copy.loc[index_copy, 'uuid']

     if n >= save_every_x_iterations:
          n = 0
          schade_dataset.to_file("meting_met_uuids_buurschade.geojson", driver='GeoJSON')
          print("\n Saved!")
pbar.close()
