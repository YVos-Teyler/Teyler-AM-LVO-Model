import itertools
import pandas as pd
from itertools import combinations, permutations
import numpy as np
import json
import re
import Classes 

class rijstrook ():
    
    def __init__(self):
        

    def assign_100m_vak(self):

    def calculate_combination_scenarios(self):

    def load_instance_from_json(self, filename):
        with open(filename, 'r') as f:
            instance_dict = json.load(f)
        return _100mvak(**instance_dict)

    def save_data(self):
        filename = str(self.road_number) +' '+ str(self.road_direction) +' '+ str(self.hmp_from) +'.json'
        self.scenario_with_costs.to_json(filename)