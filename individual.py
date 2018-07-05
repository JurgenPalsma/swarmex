import numpy as np 
import pandas as pd 

class Individual:
    """ 
        Candidate solution for the optimization problem.

        TODO: Implement multiple thresholds?
    def __init__(self,
                quantity: int, # quantity for trading
                b_start: float, # start of trading during an OS event
                b_end: float, # end of trading during OS event
                b_price: float, # min accepted price range,
                threshold_number: int, # number of thresholds,
                #thresholds: [float] = [], # threshold values
                threshold_weights: [float], #  weight of each threshold
                q_short: int # short selling quantity
                ):
        self.quantity = quantity
        self.b_start = b_start
        self.b_end = b_end
        self.b_price = b_price
        self.threshold_number = threshold_number
        #self.thresholds = thresholds
        self.threshold_weights = threshold_weights
        self.q_short = q_short
    """

    
    def factory(type, threshold_number, indiv: pd.DataFrame):

        if (type == "Coordinate"):
            return IndividualFromCoord(threshold_number, indiv)

        elif (type == "HBest"):
            return IndividualFromHBest(threshold_number, indiv)
        
        else:
            raise AssertionError("Individual type does not exist: " + type)

    factory = staticmethod(factory)

class IndividualFromCoord(Individual):

    def __init__(self, threshold_number: int, indiv: pd.DataFrame):
        self.quantity = indiv.loc['quantity']['Coordinate']
        self.b_start = indiv.loc['b_start']['Coordinate']
        self.b_end = indiv.loc['b_end']['Coordinate']
        self.b_price = indiv.loc['b_price']['Coordinate']
        self.q_short = indiv.loc['q_short']['Coordinate']
        self.threshold_number = threshold_number
        w = []
        for i in range(0, threshold_number):
            w.append(indiv.loc['t'+str(i + 1)]['Coordinate'])
        self.threshold_weights = w


class IndividualFromHBest(Individual):

    def __init__(self, threshold_number: int, indiv: pd.DataFrame):
        self.quantity = indiv.loc['quantity']['HBest']
        self.b_start = indiv.loc['b_start']['HBest']
        self.b_end = indiv.loc['b_end']['HBest']
        self.b_price = indiv.loc['b_price']['HBest']
        self.q_short = indiv.loc['q_short']['HBest']
        self.threshold_number = threshold_number
        w = []
        for i in range(0, threshold_number):
            w.append(indiv.loc['t'+str(i + 1)]['HBest'])
        self.threshold_weights = w
