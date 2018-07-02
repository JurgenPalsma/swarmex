from optimizer import AOptimizer
from particle import Particle
from fitness import AFitnessFunction, Fitness

class PSO(AOptimizer):

    def __init__(self,
                swarm_size: int = 10,
                v_max: float = 1,
                w_inertia: float = 1,
                w_memory: float = 1,
                w_neigh: float = 1,
                k: int = 5,
                vel_conv_threshold: float = 0.01):
        """ Init params """
        self.swarm_size = swarm_size
        self.v_max = v_max
        self.w_inertia = w_inertia
        self.w_memory = w_memory
        self.w_neigh = w_neigh
        self.k = k
        self.vel_conv_threshold = vel_conv_threshold

        """" Populate the swarm """
        self.__populate()


    def optimize(self, ff: AFitnessFunction):
        """
        Takes a AFitnessFunction abstract fitness function ff and finds a correct optimum
        """
        print("Optimizing")
        print("Calling fitness function with sample individual")
        individual = [134.0, 0.3434593504962303, 0.8807313175318929, 0.0, 0.9790021314573502, 0.296501, 0.398711, 0.639533, 0.833413, 0.700392]
        fitval = ff.fitness(individual)
        print("Returned MDD : %f" % (fitval))
        pass

    def __populate(self):
        self.swarm = [Particle() for _ in range(self.swarm_size)]
        pass

    def __converge(self):
        pass
