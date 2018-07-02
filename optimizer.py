from abc import ABCMeta, abstractmethod
from fitness import AFitnessFunction, Fitness

class AOptimizer:
    """ 
    Encapsulate an optimization algorithm
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def optimize(self, function: AFitnessFunction) -> Fitness:
        pass