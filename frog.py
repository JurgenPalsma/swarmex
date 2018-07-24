from fitness import Fitness
from individual import Individual
import pandas as pd
import random
import pickle

class Frog():

    def __init__(self, 
                function,
                constraints: {
                'quantity': {'min': int, 'max': int},
                'b_start': {'min': float, 'max': float},
                'b_end': {'min': float, 'max': float},
                'b_price': {'min': float, 'max': float},
                'threshold_weights': {'min': float, 'max': float},
                'q_short': {'min': int, 'max': int}},
                n_thresholds: int = 5,):

        self.ff = function
        self.constraints = constraints
        self.n_thresholds = n_thresholds

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

        self.p = pd.DataFrame({ 'Parameter': params,
                                'Coordinate': coords})
        
        # Set index to parameters for eazy access
        self.p.set_index('Parameter', inplace=True)

        # Assign fitness
        self.current_fit = self.ff.fitness(Individual.factory("Coordinate", n_thresholds, self.p))

    def __generateCoord(self, constraints: {'min': float, 'max': float}):
        return random.uniform(constraints['min'], constraints['max']) - 0.0000001

    def test(self):
        """
            Assign a fitness to the frog's performance on the test data
        """
        self.tf = self.ff.testFitness(Individual.factory("Coordinate", self.n_thresholds, self.p))
        print("Frog generated fitness: %s " % self.tf)

    def log(self, path, iteration=0):
        if (not self.tf):
            self.tf = self.ff.testFitness(Individual.factory("Coordinate", self.n_thresholds, self.p))
        with open(path + 'testfitness.txt', 'a') as f:
                f.write("%d\t%s" % (iteration, self.tf))
        with open(path + 'trainfitness.txt', 'a') as f:
                f.write("%d\t%s" % (iteration, self.current_fit))
        pickle.dump(self.tf, open(path+"pickles/testfit_run_"+str(iteration)+".pickle", "wb" ))
        pickle.dump(self.current_fit, open(path+"pickles/trainfit_run_"+str(iteration)+".pickle", "wb" ))


    def __repr__(self):
        return self.p.to_string()

    """
    TODO (eventually):
        Make sure operator overloading is safe (eg: same constraints, same number of thresholds)
    """
    def __add__(self, right): 
        left = Frog(function=self.ff, constraints=self.constraints, n_thresholds=self.n_thresholds)
        left.p = self.p + right.p
        return left

    def __sub__(self, right):
        left = Frog(function=self.ff, constraints=self.constraints, n_thresholds=self.n_thresholds)
        left.p = self.p - right.p
        return left