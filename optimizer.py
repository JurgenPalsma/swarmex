from abc import ABCMeta, abstractmethod
from fitness import AFitnessFunction

class AOptimizer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def optimize(self, function: AFitnessFunction):
        pass