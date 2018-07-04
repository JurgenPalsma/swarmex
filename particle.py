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
    Parameters:
            function: the fitness function you want to optimize
            constraints: list min/max values the parameters can take on the search space
    """

    def __init__(self, 
                function,
                constraints: {
                'quantity': {'min': int, 'max': int},
                'b_start': {'min': float, 'max': float},
                'b_end': {'min': float, 'max': float},
                'b_price': {'min': float, 'max': float},
                'threshold_weights': {'min': float, 'max': float},
                'q_short': {'min': int, 'max': int}},
                n_thresholds: int = 5,
                w_inertia: float = 0.333,
                w_memory: float = 0.5,
                w_neigh: float = 0.5,):
        
        # Assign fitness function
        self.ff = function

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

        # Map velocity at a random tiny value
        self.p = pd.DataFrame({ 'Parameter': params,
                                'Coordinate': coords, 
                                'Velocity': np.random.uniform(0.0, 0.001)})
        # Set index to parameters for eazy access
        self.p.set_index('Parameter', inplace=True)

        # Assign fitness
        self.current_fit = self.ff.fitness(Individual(n_thresholds, self.p))
        
        # Up to know you're your historical best
        self.p['HBest'] = self.p['Coordinate']

        # Assign update weights
        self.w_inertia = w_inertia
        self.w_memory = w_memory
        self.w_neigh = w_neigh

        self.n_thresholds = n_thresholds
        self.iteration = 0

    def __generateCoord(self, constraints: {'min': float, 'max': float}):
        return random.uniform(constraints['min'], constraints['max'])

  

    def update_velocity(self, neighbour):
        """
        self.velocity = (w_inertia * v) + (w_mem * (histpos - pos) + (wg * (neihg - pos)))
        self.pos = self.pos + self.vel
        """
        self.p['Neighbour'] = neighbour.p['Coordinate']
        def updatev(row):    
            return (
                    (self.w_inertia * row['Velocity']) +
                    (self.w_memory * (row['HBest'] - row['Coordinate'])) + 
                    (self.w_neigh * (row['Neighbour'] - row['Coordinate'])))

        def move(row):
            return row['Coordinate'] + row['Velocity']
        print(self.p)
        #print(self.p['Velocity'][1])
        #print(self.p['Coordinate'][1])
        self.p['Velocity'] = self.p.apply(updatev, axis=1)
        self.p['Coordinate'] = self.p.apply(move, axis=1)

        # TODO: replace your historical best if you've defeated it

        #self.p['V' + str(self.iteration)] = self.p.apply(updatev, axis=1)
        #self.p['P' + str(self.iteration)] = self.p.apply(updatep, axis=1)
        self.iteration += 1 

    def __clamp(self):
        pass
    
    def __compute_neighbour_fitness(self):
        pass
