import os
import sys
import json
import logging
import time
from multiprocessing import Process
import subprocess

from pso import run_pso_from_config
from csfla import run_csfla_from_config
from javafitness import JavaFitness, Fitness
from tools import setup_logging, socket_is_free

if __name__== "__main__":

    if len(sys.argv) == 3 and sys.argv[1] == '-c':
        # If running with config file
        if not os.path.exists(sys.argv[2]):
            print("%s: config file not found" % sys.argv[2])
            quit()
        with open(sys.argv[2]) as cfg_file:  
            cfg = json.load(cfg_file)

        if not os.path.exists(cfg['ga']['base_results_file_path']+"/ga"):
            os.makedirs(cfg['ga']['base_results_file_path']+"/ga")

        portgen = 25499

        for f in cfg['data']['files']:
            print("Running on file: %s" % f)
            # Run GA for this batch of data
            ga = Process(target=subprocess.call, args=((['java', '-jar', 'dc-ga.jar', f, '1000', '35', '4', '0.90', '0.10', '0.0025', '5', '200', '500000', '-1', '0.2', '3', '1', '0.01', '0', str(cfg['algos']['n_runs']), cfg['ga']['base_results_file_path'] ]),))
            ga.start()
            
            # Get a free socket to communicate with server
            while not socket_is_free(portgen):
                portgen += 1

            # launch dc server
            serv = Process(target=subprocess.call, args=((['java', '-jar', 'dc-server.jar', f, '1000', '35', '4', '0.90', '0.10', '0.0025', '5', '200', '500000', '-1', '0.2', '3', '1', '0.01', str(portgen)]),))
            serv.start()
            time.sleep(2)
            
            # Define fitness function for all algorithms
            ff = JavaFitness(port=portgen)

            # Define and run particle swarm optimization as a new process
            cfg['pso']['results_file_path'] = cfg['pso']['base_results_file_path'] + f + '/'
            pso = Process(target=run_pso_from_config, args=(ff, cfg['algos']['n_runs'], cfg['pso']))
            pso.start()

            # Define and run csfla
            cfg['csfla']['results_file_path'] = cfg['csfla']['base_results_file_path'] + f + '/'
            csfla = Process(target=run_csfla_from_config, args=(ff,cfg['algos']['n_runs'], cfg['csfla']))
            csfla.start()

            # Wait for all algorithms to finish and kill dc server
            csfla.join()
            pso.join()
            serv.terminate()
            portgen += 1
    else:
        print("Usage: python main.py -c config.json")