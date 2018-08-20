import logging
import logging.config
import pickle
import os
import json
from multiprocessing import Process
import subprocess
import time

def setup_logging(
    default_path='/config/logging.json',
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


from fitness import Fitness

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
    """
        Calculates an average fitness and logs it to file
    """
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
        f.write("file\tnumber of runs\tavg wealth\tavg return\tavg value\tavg profit\tavg mdd\tavg transactions\tavg short transactions\n")
        f.write("%s\t%d\t%s" % (log_path, n_runs, Af))
    pickle.dump(Af.__dict__, open(log_path+"pickles/average_fitness.pickle", "wb" ) )


import socket, errno
def socket_is_free(port):
    """
        Returns True if socket on given port is available
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            s.close()
            return False
        else:
            s.close()
            print(e)
            return False
    s.close()
    return True

def log_time(t, file, config):
    with open('./results/timing.csv', 'a') as f:
        f.write(file+ ',' + config + ',' + str(t) + ',')

def get_config_file(args):
    """
        Gets config file and checks if folders are writeable
    """
    # Error management
    if not os.path.exists(args.config):
        print("%s: config file not found" % args.config)
        quit()
    with open(args.config) as cfg_file:  
        cfg = json.load(cfg_file)
    if not os.path.exists(cfg['ga']['base_results_file_path']+"/ga"):
        os.makedirs(cfg['ga']['base_results_file_path']+"/ga")
    open('./results/timing.csv', 'w').close()
    with open('./results/timing.csv', 'a') as f:
        f.write("data,config,time,")
    return cfg

def run_ga(f, cfg):
    """
        Runs an instance of the GA as a sub-process and waits for it.
    """
    ga = Process(target=subprocess.call, args=((['java', '-jar', './dc/dc-ga.jar', f, '1000', '35', '4', '0.90', '0.10', '0.0025', '5', '200', '500000', '-1', '0.2', '3', '1', '0.01', '0', str(cfg['algos']['n_runs']), cfg['ga']['base_results_file_path'] ]),))
    ga.start()
    ga.join()
    return

def run_dc_serv(f):
    """
        Runs an instance of the dc generating server.
        Returns the port and process
    """
    port = 25499
    while not socket_is_free(port):
        port += 1
    serv = Process(target=subprocess.call, args=((['java', '-jar', './dc/dc-server.jar', f, '1000', '35', '4', '0.90', '0.10', '0.0025', '5', '200', '500000', '-1', '0.2', '3', '1', '0.01', str(port)]),))
    serv.start()
    time.sleep(1) # Give it some time to warm up
    return port, serv