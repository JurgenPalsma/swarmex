class Fitness(dict):
    """ 
        Struct which has all fitness value variables that DC java strategy returns.
        TODO: define all params
    """
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

    def __repr__(self):
        return "%10.6f\t%10.6f\t%10.6f\t%10.6f\t%10.6f\t%d\t%d\n" % (self.wealth, self.ret, self.value, self.realised_profit, self.mdd, self.no_of_transactions, self.no_of_short_selling_transactions)

from abc import ABCMeta, abstractmethod
from individual import Individual

class AFitnessFunction:
    """
    Encapsulates a function we want to optimize
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def fitness(self, individual: Individual) -> Fitness:
        """
        Fitness function that returns a Fitness object
        """
        pass
