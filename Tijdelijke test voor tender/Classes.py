import itertools
import pandas as pd
from itertools import combinations, permutations
import numpy as np
import json
import re

class _100mvak ():

    def __init__(self, road_number, road_direction, dvk_letter, hmp_from, hmp_to, age_road, GO_year, asphalt_type, damage_type, damage_class, safety_curve):
        self.initiated = False
        self.road_number = road_number
        self.road_direction = road_direction
        self.dvk_letter = dvk_letter
        self.hmp_from = hmp_from
        self.hmp_to = hmp_to
        self.age_road = age_road
        self.GO_year = GO_year
        self.years_to_GO_year = GO_year - 2023
        self.asphalt_type = asphalt_type
        self.damage_type = damage_type
        self.damage_class = damage_class

        print('Object made!')
        self.calc_road_age_from_dmg()
        self.assign_safety_curve(safety_curve)
        self.get_traffic_intensity()
        self.generate_solutions()
        self.generate_scenarios(min_separation= 3)
        self.calculate_costs()
        self.initiated = True
    
    def calc_road_age_from_dmg(self):
        damage_chance_data = pd.read_excel('Schadekans.xlsx')
        damage_chance_data.columns = damage_chance_data.columns.str.lower()
        damage_class_index = damage_chance_data.index[damage_chance_data['meest maatgevende schade klasse'].str.lower().str.contains(self.damage_class.lower())].tolist()
        self.age_road = (damage_chance_data.loc[damage_class_index, 'jaar'].values)[0]


    def save_instance_to_json(instance, filename):
        with open(filename, 'w') as f:
            json.dump(instance.__dict__, f)

    def get_traffic_intensity(self):
        print('Getting trafic intensity')
        road_number = int(re.findall(r'\d+', self.road_number)[0])
        intensity_data = pd.read_excel('Datasets/Verkeersintensiteit per weg.xlsx')
        try: 
            self.traffic_intensity = intensity_data.at[intensity_data.index[intensity_data['wegnummer'] == str(road_number)][0], 'verkeersintensiteit']
        except:
            self.traffic_intensity = intensity_data.at[0, 'verkeersintensiteit']


    def generate_solutions(self):
        print('Generating solutions!')
        """
        Generate all possible solutions for a this 100m vak

        Parameters:
            self: Reference to the class instance itself

        Returns:
            solution combinations without a return statement
        """
        solution_list = pd.read_excel('Maatregellijst.xlsx')
        solution_list.columns = solution_list.columns.str.lower()
        #get rows where road type equals the maatregellijst
        self.solution_list = solution_list[solution_list['type deklaag'] == self.asphalt_type]
        solution_names = self.solution_list['maatregel djz'] 

        combs = []
        for i in range(1, len(solution_names) + 1):
            for comb in combinations(solution_names, i):
                for perm in permutations(comb):
                    combs.append(perm)
        self.solution_combinations = combs

    def generate_scenarios(self, min_separation=None):
        print('Generating scenarios!')
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
        i = 0
        for solution_combination in self.solution_combinations:
            i+= 1
            print(f'Iteration {i}', end='\r')
            for values in itertools.product(range(0, self.years_to_GO_year), repeat=len(solution_combination)):
                scenario = list(zip(solution_combination, values))
                if min_separation is not None and not all(scenario[i+1][1]-scenario[i][1]>=min_separation for i in range(len(scenario)-1)):
                    continue
                if all(scenario[i][1] < scenario[i+1][1] for i in range(len(scenario)-1)):
                    scenarios.append(scenario)
        self.scenarios = scenarios
    
    def calculate_costs(self):
        print('Calculating costs!')
        n = 0
        scenarios_with_info = pd.DataFrame(columns=['scenario no', 'year', 'road years', 'solution costs', 'safety costs'])
        for solution_combination in self.scenarios:
            road_per_year = [0] * (self.years_to_GO_year)
            solution_per_year = [None] * (self.years_to_GO_year)
            solution_costs_per_year = [None] * (self.years_to_GO_year)
            safety_costs_per_year = [None] * (self.years_to_GO_year)
            lost_hours_costs_per_year = [None] * (self.years_to_GO_year)
            year_list = [None] * (self.years_to_GO_year)
            current_road_year = self.age_road
            n+= 1
            for scenario in solution_combination:
                solution_per_year[(scenario[1])] = scenario[0]
            for year in range(0, len(solution_per_year)):
                current_costs = 0
                lost_hours_costs = 0
                if solution_per_year[year] != None:
                    solution_index = self.solution_list.index[self.solution_list['maatregel djz'] == solution_per_year[year]][0]
                    current_road_year = self.solution_list.at[solution_index, 'theoretische levensduur']
                    current_costs = self.solution_list.at[solution_index, 'totale kosten maatregel per 100 meter']
                    lost_hours_costs = self.traffic_intensity * 2/60 * 70 
                year_list[year] = year
                safety_costs_per_year[year] = int(self.safety_curve.at[int(current_road_year), 'schadekans']*10000)
                lost_hours_costs_per_year[year] = lost_hours_costs
                solution_costs_per_year[year] = current_costs
                road_per_year[year] = current_road_year
                if current_road_year != 0:
                    current_road_year -= 1
            temp_df = pd.DataFrame({'scenario no': n, 'year': [year_list], 'road years': [road_per_year], 'solution costs': [solution_costs_per_year], 'safety costs': [safety_costs_per_year], 'lost hours costs': [lost_hours_costs_per_year]})
            scenarios_with_info = pd.concat( [scenarios_with_info, temp_df], ignore_index=True)
        self.scenario_with_costs = scenarios_with_info

        
    def assign_safety_curve(self, safety_curve):
            safety_curve = safety_curve[::-1]
            index_max = next((i for i, x in safety_curve['schadekans'].items() if x > 0.95), None)
            safety_curve = safety_curve.iloc[:-index_max+1]
            safety_curve = safety_curve[::-1]
            self.safety_curve = safety_curve.reset_index(drop=True)
            if self.initiated:
                print('New safety curve assigned! Calculating new cost!')
                self.calculate_costs()
        
    def save_data(self):
        filename = str(self.road_number) +' '+ str(self.road_direction) +' '+ str(self.hmp_from) +'.json'
        self.scenario_with_costs.to_json(filename)



def load_instance_from_json(filename):
    with open(filename, 'r') as f:
        instance_dict = json.load(f)
    return _100mvak(**instance_dict)
