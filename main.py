import os
import sys
import json
import logging
import time
from multiprocessing import Process
import subprocess
import argparse

from pso import run_pso_from_config
from csfla import run_csfla_from_config
from javafitness import JavaFitness, Fitness
from tools import setup_logging, socket_is_free

from individual import IndividualFromRaw

def run_multiple_pso(path, datafile, ff, cfg):
    """
        Runs multiple pso experiments when -p flag is passed.
        Takes a path to list of configurations (json file) and executes each provided config on a different process
    """
    logger = logging.getLogger(__name__)
    if not os.path.exists(path):
        logger.error("%s: pso config file not found" % path)
        quit()
    with open(path) as cfg_file:  
        psocfg = json.load(cfg_file)

    experiments = []

    for p in psocfg:
        logger.info('PSO: Running configuration: %s, results in: %s' % (p, psocfg[p]['base_results_file_path']))
        psocfg[p]['results_file_path'] = psocfg[p]['base_results_file_path'] + datafile + '/'
        pso = Process(target=run_pso_from_config, args=(ff, cfg['algos']['n_runs'], psocfg[p]))
        pso.start()
        experiments.append(pso)

    for e in experiments:
        e.join()

def run_multiple_csfla(path, datafile, ff, cfg):
    """
        Runs multiple csfla experiments when -f flag is passed.
        Takes a path to list of configurations (json file) and executes each provided config on a different process
    """
    logger = logging.getLogger(__name__)
    if not os.path.exists(path):
        logger.error("%s: csfla config file not found" % path)
        quit()
    with open(path) as cfg_file:  
        csflacfg = json.load(cfg_file)

    experiments = []

    for p in csflacfg:
        print('CSFLA: Running configuration: %s, results in: %s' % (p, csflacfg[p]['base_results_file_path']))
        logger.info('CSFLA: Running configuration: %s, results in: %s' % (p, csflacfg[p]['base_results_file_path']))
        csflacfg[p]['results_file_path'] = csflacfg[p]['base_results_file_path'] + datafile + '/'
        csfla = Process(target=run_csfla_from_config, args=(ff, cfg['algos']['n_runs'], csflacfg[p]))
        csfla.start()
        experiments.append(csfla)

    for e in experiments:
        e.join()

if __name__== "__main__":

    argp = argparse.ArgumentParser()

    #-db DATABSE -u USERNAME -p PASSWORD -size 20
    argp.add_argument("-c", "--config", help="Config file path", required=True)
    argp.add_argument("-p", "--pso", help="Path to pso configurations file")
    argp.add_argument("-f", "--csfla", help="Path to csfla configurations file")
    argp.add_argument("-d", "--default", help="Run default config for all unspecified algorithms")
    argp.add_argument("-o", "--only", help="Run only specified flagged algorithms", action='store_true')


    args = argp.parse_args()

    if not os.path.exists(args.config):
        print("%s: config file not found" % args.config)
        quit()
    with open(args.config) as cfg_file:  
        cfg = json.load(cfg_file)

    if not os.path.exists(cfg['ga']['base_results_file_path']+"/ga"):
        os.makedirs(cfg['ga']['base_results_file_path']+"/ga")

    portgen = 25499

    for f in cfg['data']['files']:
        print("Running on file: %s" % f)
    
        #Run GA for this batch of data
        ga = Process(target=subprocess.call, args=((['java', '-jar', 'dc-ga.jar', f, '1000', '35', '4', '0.90', '0.10', '0.0025', '5', '200', '500000', '-1', '0.2', '3', '1', '0.01', '0', str(cfg['algos']['n_runs']), cfg['ga']['base_results_file_path'] ]),))
        ga.start()
        
        # Get a free socket to communicate with server
        while not socket_is_free(portgen):
            portgen += 1

        # launch dc server
        serv = Process(target=subprocess.call, args=((['java', '-jar', 'dc-server.jar', f, '1000', '35', '4', '0.90', '0.10', '0.0025', '5', '200', '500000', '-1', '0.2', '3', '1', '0.01', str(portgen)]),))
        serv.start()
        # give it some time to warm up
        time.sleep(1) 
        
        # Define fitness function for all algorithms
        ff = JavaFitness(port=portgen)
        
        if args.csfla:
            run_multiple_csfla(args.csfla, f, ff, cfg)
        elif not args.only:
            #Define and run csfla
            cfg['csfla']['results_file_path'] = cfg['csfla']['base_results_file_path'] + f + '/'
            csfla = Process(target=run_csfla_from_config, args=(ff,cfg['algos']['n_runs'], cfg['csfla']))
            csfla.start()

        if args.pso:
            run_multiple_pso(args.pso, f, ff, cfg)
        elif not args.only:
            # Define and run particle swarm optimization as a new process
            cfg['pso']['results_file_path'] = cfg['pso']['base_results_file_path'] + f + '/'
            pso = Process(target=run_pso_from_config, args=(ff, cfg['algos']['n_runs'], cfg['pso']))
            pso.start()



        # Wait for all algorithms to finish and kill dc server
        if not args.pso and not args.only:
            pso.join()
        if not args.csfla and not args.only:
            csfla.join()
        serv.terminate()
        portgen += 1
