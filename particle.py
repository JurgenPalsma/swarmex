from fitness import Fitness
from individual import Individual
import pandas as pd
import numpy as np
import random
import logging
import json
import pickle
import time

class Particle:
    """
        Candidate solution in the swarm
        Parameters:
            function: the fitness function you want to optimize
            constraints: list of min & max values the parameters can take on the search space
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
                v_max: float,
                n_thresholds: int = 5,
                w_inertia: float = 0.333,
                w_memory: float = 0.61,
                w_neigh: float = 0.53):
        
        self.ff = function
        self.constraints = constraints
        self.n_thresholds = n_thresholds
        self.v_max = v_max
        self.iteration = 0
        self.w_inertia = w_inertia
        self.w_memory = w_memory
        self.w_neigh = w_neigh
        
        # Map coordinates
        coords = pd.Series([])
        params = pd.Series(['quantity', 'b_start', 'b_end', 'q_short', 'b_price'])
        coords[0] = self.__generateCoord(constraints['quantity'])
        coords[1] = self.__generateCoord(constraints['b_start'])
        coords[2] = self.__generateCoord(constraints['b_end'])
        while (coords[2] <= coords[1]):
            coords[2] = self.__generateCoord(constraints['b_end'])
        coords[3] = self.__generateCoord(constraints['q_short'])
        coords[4] = self.__generateCoord(constraints['b_price'])
        for i in range(0, n_thresholds):
            coords[5 + i] =  self.__generateCoord(constraints['threshold_weights'])
            params[5 + i] = "t" + str(i+1)
            constraints["t" + str(i+1)] = {'min': constraints['threshold_weights']['min'],
                                            'max': constraints['threshold_weights']['max']}

        # Map velocity at a random tiny value
        self.p = pd.DataFrame({ 'Parameter': params,
                                'Coordinate': coords, 
                                'Velocity': self.__generateCoord({'min': 0.00001 , 'max': 0.0001})})
        
        # Set index to parameters for eazy access
        self.p.set_index('Parameter', inplace=True)

        # Assign fitness
        self.current_fit = self.ff.fitness(Individual.factory("Coordinate", n_thresholds, self.p))
        
        # Up to know you're your historical best
        self.p['HBest'] = self.p['Coordinate']

    def __generateCoord(self, constraints: {'min': float, 'max': float}):
        return random.uniform(constraints['min'], constraints['max']) - 0.0000001

    def __reset(self):
        coords = pd.Series([])
        params = pd.Series(['quantity', 'b_start', 'b_end', 'q_short', 'b_price'])

        coords[0] = self.__generateCoord(self.constraints['quantity'])
        coords[1] = self.__generateCoord(self.constraints['b_start'])
        coords[2] = self.__generateCoord(self.constraints['b_end'])
        while (coords[2] <= coords[1]):
            coords[2] = self.__generateCoord(self.constraints['b_end'])
        coords[3] = self.__generateCoord(self.constraints['q_short'])
        coords[4] = self.__generateCoord(self.constraints['b_price'])
        for i in range(0, self.n_thresholds):
            coords[5 + i] =  self.__generateCoord(self.constraints['threshold_weights'])
            params[5 + i] = "t" + str(i+1)

        # Map velocity at a random tiny value
        self.p = pd.DataFrame({ 'Parameter': params,
                                'Coordinate': coords, 
                                'Velocity': np.random.uniform(0.0, 0.001)})
        # Set index to parameters for eazy access
        self.p.set_index('Parameter', inplace=True)

        # Assign fitness
        self.current_fit = self.ff.fitness(Individual.factory("Coordinate", self.n_thresholds, self.p))
        
        # Up to know you're your historical best
        self.p['HBest'] = self.p['Coordinate']

    def update_velocity(self, neighbour):
        """
            Updates the particle's velocity and moves it by one iteration
            self.velocity = (w_inertia * v) + (w_mem * (histpos - pos) + (wg * (neihg - pos)))
            self.pos = self.pos + self.vel
            returns amount of change in velocity
        """
        self.p['Neighbour'] = neighbour.p['Coordinate']
        # Switch to update velocity 
        def updatev(row):
            if ((row['Neighbour'] - row['Coordinate']) == 0):
                ret = (
                    (self.w_inertia * row['Velocity']) +
                    (self.w_memory * (row['HBest'] - row['Coordinate']))
                    + self.__generateCoord({'min': 0.00001 , 'max': 0.0001})) # Add a pinch of randomness to make sure that velocities are different
            elif (row['HBest'] - row['Coordinate']) == 0:
                ret = (
                    (self.w_inertia * row['Velocity']) +
                    (self.w_memory) + 
                    (self.w_neigh * (row['Neighbour'] - row['Coordinate'])))
            elif row['Velocity'] == 0:
                ret = (
                    (self.w_inertia) +
                    (self.w_memory * (row['HBest'] - row['Coordinate'])) + 
                    (self.w_neigh * (row['Neighbour'] - row['Coordinate'])))
            else:
                ret = (
                    (self.w_inertia * row['Velocity']) +
                    (self.w_memory * (row['HBest'] - row['Coordinate'])) + 
                    (self.w_neigh * (row['Neighbour'] - row['Coordinate'])))
            return ret

        def move(row):
            return row['Coordinate'] + row['Velocity']
        
        previous_vel = self.p['Velocity']
        self.p['Velocity'] = self.p.apply(updatev, axis=1)
        self.__clampV()
        self.p['Coordinate'] = self.p.apply(move, axis=1)
        self.__clampPos()

        # Update fitness
        self.current_fit = self.ff.fitness(Individual.factory("Coordinate", self.n_thresholds, self.p))

        # Reset particle while its fitness is not valid
        while (self.current_fit.value == 0):
            self.__reset()

        # Replace your historical best if you've defeated it 
        hfit = self.ff.fitness(Individual.factory("HBest", self.n_thresholds, self.p))
        if ( hfit.value < self.current_fit.value):
            hfit = self.current_fit
            self.p['HBest'] = self.p['Coordinate']
        self.iteration += 1 
        
        diff_in_v = self.p['Velocity'] - previous_vel
        return diff_in_v

    def __clampV(self):
        """
            Clamps the velocity of the particle
        """
        def clamp(row):
            if row.name == "quantity":  
                return row['Velocity']
            if row['Velocity'] > self.v_max:
                return self.v_max
            elif row['Velocity'] < (-self.v_max):
                return -self.v_max
            else:
                return row['Velocity']
        self.p['Velocity'] = self.p.apply(clamp, axis=1)

    def __clampPos(self):
        """
            Clamps the position of the particle if it's out of the constrained search space
        """

        def maxOf(p):
            return self.constraints[p]['max']

        def minOf(p):
            return self.constraints[p]['min']    

        def clampP(row):
            if row['Coordinate'] >= maxOf(row.name):
                return maxOf(row.name) - 0.001
            elif row['Coordinate'] <= minOf(row.name):
                return minOf(row.name) + 0.001
            return row['Coordinate']

        self.p['Coordinate'] = self.p.apply(clampP, axis=1)

    def __repr__(self):
        return ("<Particle: %s>" % self.p.to_string())
        
    def log(self, path, iteration=0):
        if (not self.tf):
            self.tf = self.ff.testFitness(Individual.factory("Coordinate", self.n_thresholds, self.p))
        with open(path + 'testfitness.txt', 'a') as f:
                f.write("%d\t%s" % (iteration, self.tf))
        with open(path + 'trainfitness.txt', 'a') as f:
                f.write("%d\t%s" % (iteration, self.current_fit))
        pickle.dump(self.tf, open(path+"pickles/testfit_run_"+str(iteration)+".pickle", "wb" ))
        pickle.dump(self.current_fit, open(path+"pickles/trainfit_run_"+str(iteration)+".pickle", "wb" ))

    
    def test(self):
        """
            Assign a fitness to the particle's performance on the test data
        """
        self.tf = self.ff.testFitness(Individual.factory("Coordinate", self.n_thresholds, self.p))
