import pandas as pd
from itertools import combinations, permutations
import itertools
import numpy as np
import matplotlib.pyplot as plt

def generate_scenarios(solutions, GO_year, min_separation=None):
    """
    Generate all possible scenarios for a list of solutions.

    Parameters:
        solutions (list): A list of lists, where each inner list represents a
            solution and the elements in the list represent the letters to be
            assigned values.
        min_separation (int): The minimum separation between consecutive
            values assigned to a solution.

    Returns:
        list: A list of all possible scenarios, where each scenario is a list
        of tuples representing the letter and its assigned value.
    """
    scenarios = []
    for solution_combination in solutions:
        for values in itertools.product(range(0, GO_year), repeat=len(solution_combination)):
            scenario = list(zip(solution_combination, values))
            if min_separation is not None and not all(scenario[i+1][1]-scenario[i][1]>=min_separation for i in range(len(scenario)-1)):
                continue
            if all(scenario[i][1] < scenario[i+1][1] for i in range(len(scenario)-1)):
                scenarios.append(scenario)
    return scenarios


def calculate_costs(scenarios, solutions, safety_curve, GO_year, start_year_road):
    n = 0
    scenarios_with_info = pd.DataFrame(columns=['scenario no', 'year', 'road years', 'solution costs', 'safety costs'])
    for solution_combination in scenarios:
        road_per_year = [0] * (GO_year)
        solution_per_year = [None] * (GO_year)
        solution_costs_per_year = [None] * (GO_year)
        safety_costs_per_year = [None] * (GO_year)
        year_list = [None] * (GO_year)
        current_road_year = start_year_road
        n+= 1
        for scenario in solution_combination:
            solution_per_year[(scenario[1])] = scenario[0]
        for year in range(0, len(solution_per_year)):
            current_costs = 0
            if year != 0:
                current_road_year -= 1
            if solution_per_year[year] != None:
                solution_index = solutions.index[solutions['maatregel djz'] == solution_per_year[year]][0]
                current_road_year = solutions.at[solution_index, 'theoretische levensduur type deklaag']
                current_costs = solutions.at[solution_index, 'vaste kosten per nacht'] + solutions.at[solution_index, 'raming per 1000m rijstrook']
            year_list[year] = year
            safety_costs_per_year[year] = safety_curve[int(current_road_year)]*10000
            solution_costs_per_year[year] = current_costs
            road_per_year[year] = current_road_year
        temp_df = pd.DataFrame({'scenario no': n, 'year': [year_list], 'road years': [road_per_year], 'solution costs': [solution_costs_per_year], 'safety costs': [safety_costs_per_year]})
        scenarios_with_info = pd.concat( [scenarios_with_info, temp_df], ignore_index=True)
    return scenarios_with_info

def list_sum(lst):
    return sum(lst)


schadelijst = pd.read_excel('Schadelijst.xlsx')
schadelijst.columns = schadelijst.columns.str.lower()
maatregellijst = pd.read_excel('Maatregellijst.xlsx')
maatregellijst.columns = maatregellijst.columns.str.lower()
schadekans = pd.read_excel('Schadekans.xlsx')
schadekans.columns = schadekans.columns.str.lower()
current_year = 2023
safety_curve = np.linspace(0,1,20).tolist()
safety_curve = safety_curve[::-1]
print(safety_curve)
for index, item in schadelijst.iterrows():
    length = schadelijst.loc[index, 'lengte']
    damage_descrition = schadelijst.loc[index, 'schadebeeld'].lower()
    damage_class = schadelijst.loc[index, 'schade classificatie'].lower()
    maintenance_year = schadelijst.loc[index, 'go jaar']
    road_type = schadelijst.loc[index, 'deklaagtype'].lower()
    jaren_tot_go = abs(maintenance_year - current_year)
    
    #get rows where road type equals the maatregellijst
    solution_list = maatregellijst[maatregellijst['randvoorwaarde uitvoering'] == road_type]
    solution_names = solution_list['maatregel djz'] 

    combs = []
    for i in range(1, len(solution_names) + 1):
        for comb in combinations(solution_names, i):
            for perm in permutations(comb):
                combs.append(perm)
    #get the corresponding damage class
    damage_class = schadekans[schadekans['meest maatgevende schade klasse'].str.lower().str.contains(damage_class.lower())]
    
    scenarios = generate_scenarios(combs, jaren_tot_go, 3)
    costs = calculate_costs(scenarios, solution_list, safety_curve, jaren_tot_go, 8)
    costs['total costs'] = costs['solution costs'].apply(list_sum) + costs['safety costs'].apply(list_sum)
    top_3 = costs.nsmallest(3,'total costs')
    print(top_3)
    costs.to_json('scenarios.json')
