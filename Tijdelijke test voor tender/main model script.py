import Classes 
import pandas as pd
import numpy as np


schadelijst = pd.read_excel('Schadelijst.xlsx')
schadelijst.columns = schadelijst.columns.str.lower()
schadekans = pd.read_excel('Schadekans.xlsx')
schadekans.columns = schadekans.columns.str.lower()
safety_curve = pd.read_excel('Veiligheid curve.xlsx')
safety_curve.columns = safety_curve.columns.str.lower()

for index, item in schadelijst.iterrows():
    road_number = schadelijst.loc[index, 'rijksweg'].lower()
    hmp_from = schadelijst.loc[index, 'van']
    hmp_to = schadelijst.loc[index, 'tot']
    road_direction = schadelijst.loc[index, 'richting'].lower()
    try:
        dvk_letter = schadelijst.loc[index, 'dvk'].lower()
    except:
        dvk_letter = schadelijst.loc[index, 'dvk']
    damage_type = schadelijst.loc[index, 'schadebeeld'].lower()
    damage_class = schadelijst.loc[index, 'schade classificatie'].lower()
    GO_year = schadelijst.loc[index, 'go jaar']
    asphalt_type = schadelijst.loc[index, 'deklaagtype'].lower()

    object = Classes._100mvak(road_number, road_direction, dvk_letter, hmp_from, hmp_to, 8 ,GO_year, asphalt_type,damage_type, damage_class, safety_curve)
    #object.assign_safety_curve(safety_curve)
    # name = str(road_number + '_' + road_direction +'_'+ hmp_from)
    # globals()[name] = object
    object.save_data()