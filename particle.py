from fitness import Fitness
from individual import Individual
import pandas as pd
import numpy as np
import random


def genCoord(constraints: {'min': float, 'max': float}):  
    return random.uniform(constraints['min'], constraints['max'])

class Particle:
    """
    Candidate solution in the swarm
    TODO:    
            - Constructor
            - Update velocity
            - Clamping func
            - Neighbourhood
    """

    def __init__(self, function, constraints: {
        'quantity': {'min': int, 'max': int},
        'b_start': {'min': float, 'max': float},
        'b_end': {'min': float, 'max': float},
        'b_price': {'min': float, 'max': float},
        'threshold_weights': {'min': float, 'max': float},
        'q_short': {'min': int, 'max': int}},
        n_thresholds: int = 5):
        
        self.function = function

        # Map coordinates
        coords = pd.Series([])
        params = pd.Series(['quantity', 'b_start', 'b_end', 'q_short', 'b_price'])

        coords[0] = self.__generateCoord(constraints['quantity'])
        coords[1] = self.__generateCoord(constraints['b_start'])
        coords[2] = self.__generateCoord(constraints['b_end'])
        coords[3] = self.__generateCoord(constraints['q_short'])
        coords[4] = self.__generateCoord(constraints['b_price'])
        for i in range(0, n_thresholds):
            coords[5 + i] =  self.__generateCoord(constraints['threshold_weights'])
            params[5 + i] = "t" + str(i+1)

        self.p = pd.DataFrame({ 'Parameter': params,
                                'Coordinate': coords, 
                                'Velocity': np.random.uniform(0.0, 0.001)})
        # Set index to parameters for eazy access
        self.p.set_index('Parameter', inplace=True)
        print(self.p)

        self.current_fit = self.function.fitness(Individual(n_thresholds, self.p))
 
    def __generateCoord(self, constraints: {'min': float, 'max': float}):
        return random.uniform(constraints['min'], constraints['max'])

  

    def update_velocity(self, neighbours = []):
        pass

    def __clamp(self):
        pass
    
    def __compute_neighbour_fitness(self):
        pass