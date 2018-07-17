from pso import PSO
from javafitness import JavaFitness, Fitness
from particle import Particle
from individual import Individual

import os
import json
import logging
import logging.config

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

def calculate_average_fitness(tfitnesses):
    
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
    
    open('results/result.txt', 'w').close()
    with open('results/result.txt', 'a') as f:
        f.write("number of runs\tavg wealth\tavg return\tavg value\tavg profit\tavg mdd\tavg transactions\tavg short transactions\n")
        f.write("%d\t%s" % (n_runs, Af))

if __name__== "__main__":

    # Setup Logging
    setup_logging()
    logger = logging.getLogger(__name__)
    open('results/testfitness.txt', 'w').close()
    open('results/trainfitness.txt', 'w').close()

    with open('results/testfitness.txt', 'a') as f:
        f.write("run\twealth\treturn\tvalue\tprofit\tmdd\ttransactions\tshort transactions\n")
    with open('results/trainfitness.txt', 'a') as f:
        f.write("run\twealth\treturn\tvalue\tprofit\tmdd\ttransactions\tshort transactions\n")

    # Set the fitness function
    fitness_function = JavaFitness()

    # Init variables
    n_runs = 0
    n_try_runs = 3
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
        particle.log(i)

    calculate_average_fitness(tfitnesses)    