from optimizer import AOptimizer
from particle import Particle
from fitness import AFitnessFunction, Fitness
from individual import Individual
from enum import Enum, unique

@unique
class Neighbourhood(Enum):
    GLOBAL = 0
    RING = 1

class PSO(AOptimizer):
    """
    PSO algorithm encapsulation. 
    TODO: 
            - define arguments, make better default params
            - neighbourhood
    """
    def __init__(self,
                swarm_size: int = 10,
                v_max: float = 1,
                w_inertia: float = 1,
                w_memory: float = 1,
                w_neigh: float = 1,
                k: int = 5,
                vel_conv_threshold: float = 0.01,
                neighbourhood: int = Neighbourhood.GLOBAL):
        self.swarm_size = swarm_size
        self.v_max = v_max
        self.w_inertia = w_inertia
        self.w_memory = w_memory
        self.w_neigh = w_neigh
        self.k = k
        self.vel_conv_threshold = vel_conv_threshold,
        self.neighbourhood = neighbourhood

        self.__populate()


    def optimize(self, ff: AFitnessFunction) -> Fitness:
        """
        Takes an AFitnessFunction abstract fitness function ff and returns an optimum
        individual = Individual(quantity = 134.0,
                                b_start = 0.3434593504962303, 
                                b_end = 0.8807313175318929, 
                                q_short =  0.0, 
                                b_price = 0.9790021314573502,
                                threshold_number = 5, 
                                threshold_weights = [0.296501, 0.398711, 0.639533, 0.833413, 0.700392])

        fitval = ff.fitness(individual)
        print("Returned fitness: ", fitval)
        """
        
        pass

    def __populate(self):
        """
        TODO
        """
        pass

    def __converge(self):
        """
        TODO
        """
        pass

    def __find_neighbours(self):
        """
        TODO
        """
        pass
