class Individual:
    """ 
        Candidate solution for the optimization problem.

        TODO: Implement multiple thresholds?
    """
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