
#Module na module 1 om werkpakketten te maken


import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm import tqdm
import os

df_met_buurschade = pd.read_json('json_buurschade.json')
df_met_buurschade['middenvoor_buur'] = None
df_met_buurschade['middenachter_buur'] = None
df_met_buurschade['links_buur'] = None
df_met_buurschade['rechts_buur'] = None

for index, row in df_met_buurschade.iterrows():
    
    for item in row['extra_info']:
        #item indexes:
        #0 is wegnummer
        #1 is strooksoort
        #2 is strooknummer
        #3 is hm van
        #4 is hm tot
        #5 is uuid
        #als de hm tot match met de hm_van van het huidige (middelste) vakje ligt het wegdeel erachter
        #       
        if row['hm_from'] == item[4]:  
            df_met_buurschade.at[index, 'middenachter_buur'] = [item[5]]

        #als de hm van match met de hm_tot van het huidige (middelste) vakje ligt het wegdeel ervoor
        elif row['hm_to'] == item[3]:
            df_met_buurschade.at[index, 'middenvoor_buur'] = [item[5]]

        #links rechts bepalen
        elif row['lane'] > item[2] and row['lane_type_letter'] == item[1]:
            df_met_buurschade.at[index, 'links_buur'] = [item[5]]
        #links rechts bepalen
        elif row['lane'] < item[2] and row['lane_type_letter'] == item[1]:
            df_met_buurschade.at[index, 'rechts_buur'] = [item[5]]
        elif row['rechts_buur'] == None:
            df_met_buurschade.at[index, 'rechts_buur'] = [item[5]]
        elif row['links_buur'] == None:
            df_met_buurschade.at[index, 'links_buur'] = [item[5]]
                      
cols = ['middenachter_buur', 'middenvoor_buur', 'rechts_buur', 'links_buur']
df_met_buurschade['aantal buren ingevuld'] = df_met_buurschade[cols].count(axis=1)
df_met_buurschade['aantal buren gematcht'] = df_met_buurschade['extra_info'].apply(lambda x: len(x))

df_met_buurschade.to_excel('buurschade  tussen.xlsx')

#while loop om werkpakketten te maken door alleen vooruit of achteruit te kijken en iedere keer de nieuwe uuid invullen om vervolgens de voor buur uuid weer terug in te vullen
            



