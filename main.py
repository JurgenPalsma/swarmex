import os
import sys
import logging
from timeit import Timer
import argparse
from multiprocessing import Process

from pso import run_pso_from_config, run_multiple_pso
from csfla import run_csfla_from_config, run_multiple_csfla
from javafitness import JavaFitness, Fitness
from tools import setup_logging, socket_is_free, log_time, get_config_file, run_dc_serv, run_ga

def get_args():
    argp = argparse.ArgumentParser()
    argp.add_argument("-c", "--config", help="Config file path", required=True)
    argp.add_argument("-p", "--pso", help="Path to pso configurations file")
    argp.add_argument("-f", "--csfla", help="Path to csfla configurations file")
    argp.add_argument("-d", "--default", help="Run default config for all unspecified algorithms")
    argp.add_argument("-o", "--only", help="Run only specified flagged algorithms", action='store_true')
    argp.add_argument("-g", "--ga", help="Run ga",  action='store_true')
    return argp.parse_args()

if __name__== "__main__":
 
    args = get_args()
    cfg = get_config_file(args)
    
    if not args.only or args.ga:
        # Run GA
        for f in cfg['data']['files']:
            t = Timer(lambda: run_ga(f, cfg))
            log_time(t.timeit(number=1), f, 'ga')

    if not args.only or args.csfla:
        for f in cfg['data']['files']:
            # Create a new dc generating server and assign it the fitness function
            port, serv = run_dc_serv(f)
            ff = JavaFitness(port=port)

            # Run CSFLA
            if args.csfla:
                run_multiple_csfla(args.csfla, f, ff, cfg)
            elif not args.only:
                cfg['csfla']['results_file_path'] = cfg['csfla']['base_results_file_path'] + f + '/'
                csfla = Process(target=run_csfla_from_config, args=(ff,cfg['algos']['n_runs'], cfg['csfla']))
                csfla.start()
            if not args.csfla and not args.only:
                csfla.join()
            serv.terminate()

    if not args.only or args.pso:
        for f in cfg['data']['files']:
                # Create a new dc generating server and assign it the fitness function
                port, serv = run_dc_serv(f)
                ff = JavaFitness(port=port)

                # Run PSO
                if args.pso:
                    run_multiple_pso(args.pso, f, ff, cfg)
                elif not args.only:
                    cfg['pso']['results_file_path'] = cfg['pso']['base_results_file_path'] + f + '/'
                    pso = Process(target=run_pso_from_config, args=(ff, cfg['algos']['n_runs'], cfg['pso']))
                    pso.start()
                if not args.pso and not args.only:
                    pso.join()
                serv.terminate()
