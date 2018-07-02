class Fitness:

    ''' Default fitness constructor '''
    def __init__(
                self,
                value: float = 0, 
                u_sell: int = 0, 
                u_buy: int = 0, 
                noop: int = 0,
                realised_profit: float = 0,
                mdd: float = 0,
                ret: float = 0,
                wealth: float = 0,
                no_of_transactions: int = 0,
                no_of_short_selling_transactions: int = 0
                ):
        self.value = value
        self.u_sell = u_sell
        self.u_buy = u_buy
        self.noop = noop
        self.realised_profit = realised_profit
        self.mdd = mdd
        self.ret = ret
        self.wealth = wealth
        self.no_of_transactions = no_of_transactions
        self.no_of_short_selling_transactions = no_of_short_selling_transactions


from abc import ABCMeta, abstractmethod

class AFitnessFunction:
    __metaclass__ = ABCMeta

    @abstractmethod
    def fitness(self, individual):
        pass