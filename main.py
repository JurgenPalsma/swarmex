from pso import PSO
from csfla import CSFLA
from javafitness import JavaFitness, Fitness
from individual import Individual

import os
import sys
import json
import logging
import logging.config
from multiprocessing import Process

import subprocess

R_FILE_PATH = ""
GA_R_FILE_PATH = ""

def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def calculate_average_fitness(tfitnesses, log_path):
    
    Avalue = 0
    Au_sell= 0
    Au_buy= 0
    Anoop= 0
    Arealised_profit= 0
    Amdd= 0
    Aret= 0
    Awealth= 0
    Ano_of_transactions= 0
    n_runs = len(tfitnesses)

    for f in tfitnesses:
        Avalue += tfitnesses[f].value
        Au_sell += tfitnesses[f].u_sell
        Au_buy += tfitnesses[f].u_buy
        Anoop += tfitnesses[f].noop
        Arealised_profit += tfitnesses[f].realised_profit
        Amdd += tfitnesses[f].mdd
        Aret += tfitnesses[f].ret
        Awealth += tfitnesses[f].wealth
        Ano_of_transactions += tfitnesses[f].no_of_transactions

    Af = Fitness(value= Avalue / n_runs,
                u_sell= Au_sell / n_runs,
                u_buy= Au_buy / n_runs,
                noop= Anoop / n_runs,
                realised_profit= Arealised_profit / n_runs,
                mdd= Amdd / n_runs,
                ret= Aret / n_runs,
                wealth= Awealth / n_runs,
                no_of_transactions= Ano_of_transactions / n_runs)
    
    open(log_path + 'results.txt', 'w').close()
    with open(log_path + 'results.txt', 'a') as f:
        f.write("number of runs\tavg wealth\tavg return\tavg value\tavg profit\tavg mdd\tavg transactions\tavg short transactions\n")
        f.write("%d\t%s" % (n_runs, Af))
        print("Average fitness: %s" % Af)

def run_ga(datafile):
    subprocess.call(['java', '-jar', 'dc-ga.jar', datafile, '1000', '35', '4', '0.90', '0.10', '0.0025', '5', '200', '500000', '-1', '0.2', '3', '1', '0.01'])

def run_pso(port = 27134):
    # Setup Logging
    setup_logging()
    logger = logging.getLogger(__name__)
    open(R_FILE_PATH + 'testfitness.txt', 'w').close()
    open(R_FILE_PATH + 'trainfitness.txt', 'w').close()

    with open(R_FILE_PATH + 'testfitness.txt', 'a') as f:
        f.write("run\twealth\treturn\tvalue\tprofit\tmdd\ttransactions\tshort transactions\n")
    with open(R_FILE_PATH + 'trainfitness.txt', 'a') as f:
        f.write("run\twealth\treturn\tvalue\tprofit\tmdd\ttransactions\tshort transactions\n")

    # Set the fitness function
    fitness_function = JavaFitness(port=port)

    # Init variables
    n_runs = 0
    n_try_runs = 10
    tfitnesses = {}

    # Main loop
    for i in range(0, n_try_runs):

        # Initialize the swarm
        pso = PSO(swarm_size=40)

        # Optimize with swarm
        particle = pso.optimize(fitness_function)
        
        # Test the particle and add it to list if it's valid
        particle.test()
        if (particle.tf.value < -100) or (particle.tf.mdd == 0):
            logger.info("Run %d: particle not taken into account in average results: fitness is invalid" % i)
        else:
            tfitnesses[i] = particle.tf
            n_runs += 1

        # Log results
        particle.log(iteration=i, path=R_FILE_PATH)

    calculate_average_fitness(tfitnesses, R_FILE_PATH)

def run_csfla(port = 27134):
    # Setup Logging
    setup_logging()
    logger = logging.getLogger(__name__)
    open(CSFLA_R_FILE_PATH + 'testfitness.txt', 'w').close()
    open(CSFLA_R_FILE_PATH + 'trainfitness.txt', 'w').close()

    with open(CSFLA_R_FILE_PATH + 'testfitness.txt', 'a') as f:
        f.write("run\twealth\treturn\tvalue\tprofit\tmdd\ttransactions\tshort transactions\n")
    with open(CSFLA_R_FILE_PATH + 'trainfitness.txt', 'a') as f:
        f.write("run\twealth\treturn\tvalue\tprofit\tmdd\ttransactions\tshort transactions\n")

    # Set the fitness function
    fitness_function = JavaFitness(port=port)

    # Init variables
    n_runs = 0
    n_try_runs = 10
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
        frog.log(iteration=i, path=CSFLA_R_FILE_PATH)

    calculate_average_fitness(tfitnesses, CSFLA_R_FILE_PATH)
    pass

if __name__== "__main__":

    if len(sys.argv) != 2:
        DATA_FILE_PATH = 'data/fx-spot_EUR_GBP_10min_201310.txt'
        R_FILE_PATH = "results/pso/fx-spot_EUR_GBP_10min_201310/"
        CSFLA_R_FILE_PATH = "results/csfla/fx-spot_EUR_GBP_10min_201310/"
        GA_R_FILE_PATH = "results/ga/fx-spot_EUR_GBP_10min_201310"
    else:
        DATA_FILE_PATH = 'data/' + sys.argv[1] + '.txt'
        R_FILE_PATH = 'results/pso/' + sys.argv[1]  + '/'
        CSFLA_R_FILE_PATH ='results/csfla/' + sys.argv[1]  + '/'
        GA_R_FILE_PATH ='results/ga/' + sys.argv[1]

    if not os.path.exists(DATA_FILE_PATH):
        print("%s: File not found" % DATA_FILE_PATH)
        quit()

    if not os.path.exists(R_FILE_PATH):
        os.makedirs(R_FILE_PATH)

    if not os.path.exists(CSFLA_R_FILE_PATH):
        os.makedirs(CSFLA_R_FILE_PATH)
    
    if not os.path.exists(GA_R_FILE_PATH):
        os.makedirs(GA_R_FILE_PATH)
    
    #run_ga(DATA_FILE_PATH + ':'+ GA_R_FILE_PATH +':0:20:21:27')
    #run_pso()
    run_csfla()