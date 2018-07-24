from optimizer import AOptimizer
from particle import Particle
from fitness import AFitnessFunction, Fitness
from individual import Individual
from enum import Enum, unique
import time
import json
import logging
from tools import setup_logging, calculate_average_fitness
import pickle

@unique
class Neighbourhood(Enum):
    GLOBAL = 0
    RING = 1

class PSO(AOptimizer):
    """
    PSO algorithm encapsulation.
    """
    def __init__(self,
                swarm_size: int = 10,
                v_max: float = 10.0,
                w_inertia: float = 0.55,
                w_memory: float = 0.55,
                w_neigh: float = 0.55,
                k: int = 5,
                vel_conv_threshold: float = 0.001,
                neighbourhood: int = Neighbourhood.GLOBAL,
                max_iter: int = 5):

        logger = logging.getLogger(__name__)
        logger.info("Initialize PSO with swarm_size:%i, v_max:%f, w_inertia:%f, w_memory:%f, w_neigh:%f, k:%i, vel_conv_thresholds:%f, neighbourhood:%s, max_iter:%i" % 
            (swarm_size, v_max, w_inertia, w_memory, w_neigh, k, vel_conv_threshold, neighbourhood.__repr__(), max_iter))
        self.swarm_size = swarm_size
        self.v_max = v_max
        self.w_inertia = w_inertia
        self.w_memory = w_memory
        self.w_neigh = w_neigh
        if k == 0:
            self.k = swarm_size / 4
        else:
            self.k = k
        self.vel_conv_threshold = vel_conv_threshold,
        self.neighbourhood = neighbourhood
        self.converged = False
        self.max_iter = max_iter

    def optimize(self, ff: AFitnessFunction) -> Particle:
        """
        Takes an AFitnessFunction abstract fitness function ff and returns an optimum
        """
        # Initialize swarm
        self.__populate(ff)
        self.ff = ff
        self.iteration = 0

        #Loop
        while (not self.__converged()):
            diff_in_vs = []
            for p in self.swarm:
                # Move the particle and add its difference of velocity to list
                diff_in_vs.append(p.update_velocity(self.__find_best_neighbour(p)))
            
            # Check if we reached minimum velocity change
            ik = 0
            for d in diff_in_vs:
                if (self.__min_vel(d)):
                    ik += 1
                    if (ik >= self.k):
                        self.converged = True
                        break
                    
        self.swarm.sort(key=lambda x: x.current_fit.ret, reverse=True)
        return self.swarm[0]

    def __populate(self, ff: AFitnessFunction):
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
        self.iteration += 1
        if self.iteration > self.max_iter :
            self.converged = True
        return self.converged

    def __min_vel(self, d):
        """
        Returns true if we reach the minimum velocity change in a particle
        We ignore the velocities which tend to not reach minimum change
        """
        d = d.drop('quantity', axis=0)
        d = d.drop('q_short')
        return (abs(d.max()) < self.vel_conv_threshold)

    def __find_best_neighbour(self, p: Particle):
        """
        For now, just returns global neighbourhood
        """
        bestp = self.swarm[0]
        for p in self.swarm:
            bestf = self.ff.fitness(Individual.factory("Coordinate", bestp.n_thresholds, bestp.p))
            while (bestf is None):
                bestf = self.ff.fitness(Individual.factory("Coordinate", bestp.n_thresholds, bestp.p))
                #time.sleep(1)
            currentf = self.ff.fitness(Individual.factory("Coordinate", p.n_thresholds, p.p))

            if (currentf.value > bestf.value):
                bestp = p
        return bestp

def run_pso(fitness_function, 
            results_file_path = "", 
            swarm_size = 40,
            n_max_try_runs=10, 
            v_max: float = 10.0,
            w_inertia: float = 0.55,
            w_memory: float = 0.55,
            w_neigh: float = 0.55,
            k: int = 5,
            vel_conv_threshold: float = 0.001,
            neighbourhood: int = Neighbourhood.GLOBAL,
            max_iter: int = 5):
    # Setup Logging
    setup_logging()
    logger = logging.getLogger(__name__)

    open(results_file_path + 'testfitness.txt', 'w').close()
    open(results_file_path + 'trainfitness.txt', 'w').close()
    with open(results_file_path + 'testfitness.txt', 'a') as f:
        f.write("run\twealth\treturn\tvalue\tprofit\tmdd\ttransactions\tshort transactions\n")
    with open(results_file_path + 'trainfitness.txt', 'a') as f:
        f.write("run\twealth\treturn\tvalue\tprofit\tmdd\ttransactions\tshort transactions\n")
    
    # Set the fitness function
    fitness_function = fitness_function

    # Init variables
    n_runs = 0
    tfitnesses = {}
    particles = {}

    # Main loop
    for i in range(0, n_max_try_runs):

        # Initialize the swarm
        pso = PSO(swarm_size=swarm_size,
                v_max=v_max,
                w_inertia=w_inertia,
                w_memory=w_memory,
                w_neigh=w_neigh,
                k=k,
                vel_conv_threshold=vel_conv_threshold,
                max_iter=max_iter)

        # Optimize with swarm
        particle = pso.optimize(fitness_function)
        
        # Test the particle and add it to list if it's valid
        particle.test()
        if (particle.tf.value < -100) or (particle.tf.mdd == 0):
            logger.info("Run %d: particle not taken into account in average results: fitness is invalid" % i)
        else:
            tfitnesses[i] = particle.tf
            particles[i] = particle
            n_runs += 1

        # Log results
        particle.log(iteration=i, path=results_file_path)
        pickle.dump(particle.p, open(results_file_path+"/pickles/particle_run_"+str(i)+".pickle", "wb" ) )
    calculate_average_fitness(tfitnesses, results_file_path)

import os

def run_pso_from_config(ff, n_runs, config):
    if not os.path.exists(config['results_file_path']):
        os.makedirs(config['results_file_path'])
    if not os.path.exists(config['results_file_path']+'pickles/'):
        os.makedirs(config['results_file_path']+'pickles/')
    run_pso(ff,
    results_file_path = config['results_file_path'], 
    swarm_size = config['swarm_size'],
    n_max_try_runs= n_runs, 
    v_max= config['v_max'],
    w_inertia= config['w_inertia'],
    w_memory= config['w_memory'],
    w_neigh= config['w_neigh'],
    k= config['k'],
    vel_conv_threshold= config['vel_conv_threshold'],
    neighbourhood= config['neighbourhood'],
    max_iter= config['max_iter'])