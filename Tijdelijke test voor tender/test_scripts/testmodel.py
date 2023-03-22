import pandas as pd
import numpy as np

schadelijst = pd.read_excel('Schadelijst.xlsx')
schadelijst.columns = schadelijst.columns.str.lower()
maatregellijst = pd.read_excel('Maatregellijst.xlsx')
maatregellijst.columns = maatregellijst.columns.str.lower()
schadekans = pd.read_excel('Schadekans.xlsx')
schadekans.columns = schadekans.columns.str.lower()

costs_of_hole_in_road = 2000

chance_curve = np.linspace(0,1,14).tolist()

print(chance_curve)

scenarios = []

def generate_scenarios(current_scenario, remaining_safety_year, current_cost, years_to_GO_moment, max_solutions):
    if remaining_safety_year <= 0:
        scenarios.append(current_scenario)
        return
    
    for solution in maatregel_indexen:
            for year in range(1, years_to_GO_moment+1):
                if year in max_solutions and max_solutions[year] == 0:
                    continue
                new_safety_year = solution["reset"]
                new_cost = current_cost - solution["cost"]
                new_scenario = current_scenario + [(solution["name"], solution["cost"], year)]
                new_max_solutions = max_solutions.copy()
                if year in new_max_solutions:
                    new_max_solutions[year] -= 1
                generate_scenarios(new_scenario, new_safety_year, new_cost, years_to_GO_moment, new_max_solutions)



for index, iets in schadelijst.iterrows():
    length = schadelijst.loc[index, 'lengte']
    damage_descrition = schadelijst.loc[index, 'schadebeeld'].lower()
    damage_class = schadelijst.loc[index, 'schade classificatie'].lower()
    maintenance_year = schadelijst.loc[index, 'go-jaar']
    road_type = schadelijst.loc[index, 'deklaagtype'].lower()
    jaren_tot_go = maintenance_year - 2023
    
    #get index of rows where road type equals the maatregellijst
    maatregel_indexen = maatregellijst.index[maatregellijst['randvoorwaarde uitvoering'] == road_type].tolist()
    #get index of the corresponding damage class
    damage_class_index = schadekans.index[schadekans['meest maatgevende schade klasse'].str.lower().str.contains(damage_class.lower())].tolist()
    current_safety_year = (schadekans.loc[damage_class_index, 'jaar'].values)[0]
    
    chance_list = []
    print(current_safety_year)
    for num in range(jaren_tot_go):
        print('Jaar: ' + str(num))
        chance_list.append(chance_curve[current_safety_year])
        if num == 9:
            #doe maatregel
            current_safety_year + 8
        if num == 4:
            for item in maatregel_indexen:
                    cost_of_solution = maatregellijst.loc[item, 'vaste kosten per nacht'] + length * maatregellijst.loc[item, 'raming per 1000m rijstrook']
                    new_safety_year = maatregellijst.loc[item, 'theoretische levensduur type deklaag']
                    new_safety_costs = schadekans.loc[item, 'veiligheidkosten per jaar']
        if num == 6:
            for item in maatregel_indexen:
                    cost_of_solution = maatregellijst.loc[item, 'vaste kosten per nacht'] + length * maatregellijst.loc[item, 'raming per 1000m rijstrook']
                    new_safety_year = maatregellijst.loc[item, 'theoretische levensduur type deklaag']
                    new_safety_costs = schadekans.loc[item, 'veiligheidkosten per jaar']
        
    print(chance_list)
            
