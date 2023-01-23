
#Module na module 1 om werkpakketten te maken


import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm import tqdm
import os

df_met_buurschade = pd.read_json('json_buurschade.json')
df_met_buurschade['middenvoor_buur'] = None
df_met_buurschade['middenachter_buur'] = None

for index, row in df_met_buurschade.iterrows():
    
    hm_van_list = []
    hm_tot_list = []
    for item in row['extra_info']:
        #item indexes:
        #0 is wegnummer
        #1 is strooksoort
        #2 is strooknummer
        #3 is hm van
        #4 is hm tot)
        #5 is schade
        #6 is uuid
        #als de hm tot match met de hm_van van het huidige (middelste) vakje ligt het wegdeel erachter
        if row['hm_van'] == item[4]:
            #strooksoort gelijk en strook volg gelijk is midden voor 
            if row['strookvolg'] == item [2]:    
                if row['strooksoor'] == item[1]:
                    row['middenachter_buur'] = [item[5], item[6]]

        #als de hm van match met de hm_tot van het huidige (middelste) vakje ligt het wegdeel ervoor
        if row['hm_tot'] == item[3]:
            #strooksoort gelijk en strook volg gelijk is midden voor 
            if row['strooksoor'] == item[1]:
                if row['strookvolg'] == item [2]:
                    row['middenvoor_buur'] = [item[5], item[6]]
        
    if not row['middenvoor_buur'] and row['middenachter_buur']:
        row['middenvoor_buur'] = ['schade', 'uuid']        

df_met_buurschade.to_excel('buurschade  tussen.xlsx')

#while loop om werkpakketten te maken door alleen vooruit of achteruit te kijken en iedere keer de nieuwe uuid invullen om vervolgens de voor buur uuid weer terug in te vullen
            



