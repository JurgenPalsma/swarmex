from optimizer import AOptimizer
from frog import Frog
import numpy as np 
import pandas as pd
from tools import setup_logging, calculate_average_fitness
import logging
import os
import pickle

class CSFLA(AOptimizer):
    """
    CSFLA algorithm encapsulation.
    """

    def __init__(self, n, m, sn, Gm = 10, Gs = 10, constraints={'quantity': {'min': 0, 'max': 100},
                                                                'b_start': {'min': 0.0, 'max': 1.0},
                                                                'b_end': {'min': 0.0, 'max': 1.0},
                                                                'b_price': {'min': 0.0, 'max': 1.0},
                                                                'threshold_weights': {'min': 0.0, 'max': 1.0},
                                                                'q_short': {'min': 0, 'max': 100}}):
        self.n = n # number of frogs in pop
        self.sn = sn # number of frogs picked for sub-memeplex
        self.m = m # number of memeplexes
        self.Gm = Gm
        self.Gs = Gs
        self.constraints = constraints

    def __populate(self):
        self.pop = [ Frog(function=self.ff,
                        constraints=self.constraints)
                        for i in range(self.n)]

        for idx, f in enumerate(self.pop):
            while f.current_fit.ret == 0:
                f = Frog(function=self.ff,
                        constraints=self.constraints)
            self.pop[idx] = f
           
    def __divide(self):
        memeplexes = list()
        for sub_list_count in range(self.m):
            memeplexes.append(self.pop[sub_list_count::self.m])
        return memeplexes

    def __subdivide(self, memeplex):
        memeplex.sort(key=lambda x: x.current_fit.ret, reverse=True)
        pbs = list()
        submemeplex = list()
        for i, f in enumerate(memeplex):
            pbs.append((2 * (self.n + 1 - i)) / (self.n * (self.n + 1)))
        
        for i in range(self.sn):
            submemeplex.append(np.random.choice(memeplex, 1, pbs)[0])
        return submemeplex


    def __evolve(self, sub):
        xb = sub[0]
        xw = sub[-1]
        xs = self.pop[0]
        r = np.random.uniform(0, 1)

        # Try to learn from local best
        xt = xb - xw
        xt.p = xw.p + r * (xt.p)
        if (xt.current_fit.ret > xw.current_fit.ret):
            sub[-1] = xt
            return sub

        else:
            # Try to learn from local best
            xt = xs - xw
            xt.p = xw.p + r * (xt.p)
            if (xt.current_fit.ret > xw.current_fit.ret):
                sub[-1] = xt
                return sub
            
            else:
                # Randomize the worst frog in the submemeplex
                sub[-1] = Frog(self.ff, self.constraints)
                return sub


    def optimize(self, ff):
        self.ff = ff

        self.__populate()

        self.pop.sort(key=lambda x: x.current_fit.ret, reverse=True) # sort by descending fitness

        gm = 0 # max generation
        gs = 0 # max memeplex iteration

        while gm < self.Gm:
            memeplexes = self.__divide()
            new_generation = list()
            for memeplex in memeplexes:
                submemeplex = self.__subdivide(memeplex)
                while gs < self.Gs:
                    submemeplex = self.__evolve(submemeplex)
                    gs += 1
                new_generation.extend(submemeplex)
            self.pop = new_generation
            self.pop.sort(key=lambda x: x.current_fit.ret, reverse=True) # sort by descending fitness
            #print("Generation: %d" % gm)
            #print(self.pop[0].current_fit)
            gm += 1

        return self.pop[0]
        
def run_csfla(fitness_function, n_try_runs, results_file_path, n, m, sn, Gm = 10, Gs =10):
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

    # Main loop
    for i in range(0, n_try_runs):

        csfla = CSFLA(20, 5, 3, 40, 40)
        frog = csfla.optimize(fitness_function)
        
        # Test the particle and add it to list if it's valid
        frog.test()
        if (frog.tf.value < -100) or (frog.tf.mdd == 0):
            logger.info("Run %d: frog not taken into account in average results: fitness is invalid" % i)
        else:
            tfitnesses[i] = frog.tf
            n_runs += 1

        # Log results
        frog.log(iteration=i, path=results_file_path)
        pickle.dump(frog.p, open(results_file_path+"/pickles/frog_run_"+str(i)+".pickle", "wb" ) )

    calculate_average_fitness(tfitnesses, results_file_path)

def run_csfla_from_config(ff, n_runs, config):
    if not os.path.exists(config['results_file_path']):
        os.makedirs(config['results_file_path'])
    if not os.path.exists(config['results_file_path']+'pickles/'):
        os.makedirs(config['results_file_path']+'pickles/')
    run_csfla(ff, n_runs, config['results_file_path'],
    n=config['n_frogs'],
    m=config['n_sm_frogs'],
    sn=config['n_memeplex'],
    Gm=config['max_generations'],
    Gs=config['max_sub_generations'])