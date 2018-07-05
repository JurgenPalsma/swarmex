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



    def optimize(self, ff: AFitnessFunction) -> Fitness:
        """
        Takes an AFitnessFunction abstract fitness function ff and returns an optimum
        """
        # Initialize swarm
        self.__populate(ff)
        self.ff = ff
        self.conv = 0

        #Loop
        while (not self.__converged()):
            for p in self.swarm:
                p.update_velocity(self.__find_best_neighbour(p))

        i = 0
        bestp = self.swarm[0]
        for p in self.swarm:
           if p.current_fit.value > bestp.current_fit.value:
               bestp = p

        print(bestp.p)
        print(bestp.current_fit)
        
        pass

    def __populate(self, ff: AFitnessFunction):
        print("Initialise swarm with %d particles" % self.swarm_size)
        self.swarm = [  Particle(function=ff, v_max=3,
                        constraints={'quantity': {'min': 0, 'max': 100},
                        'b_start': {'min': 0.0, 'max': 1.0},
                        'b_end': {'min': 0.0, 'max': 1.0},
                        'b_price': {'min': 0.0, 'max': 1.0},
                        'threshold_weights': {'min': 0.0, 'max': 1.0},
                        'q_short': {'min': 0, 'max': 100}},
                        w_inertia=self.w_inertia,
                        w_memory= self.w_memory,
                        w_neigh=self.w_neigh)
                        for i in range(self.swarm_size)]

    def __converged(self):
        """
        TODO
        """
        self.conv += 1
        return self.conv > 10

    def __find_best_neighbour(self, p: Particle):
        """
        For now, just returns global neighbourhood
        TODO 
        """
        bestp = self.swarm[0]
        for p in self.swarm:
            bestf = self.ff.fitness(Individual.factory("Coordinate", bestp.n_thresholds, bestp.p))
            currentf = self.ff.fitness(Individual.factory("Coordinate", p.n_thresholds, p.p))
            if (currentf.value > bestf.value):
                bestp = p
        return bestp
