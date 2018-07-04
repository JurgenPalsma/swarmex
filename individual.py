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
