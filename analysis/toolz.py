import json
import pandas as pd
import matplotlib.pyplot as plt
import pickle

def get_config(file='../config/config.json'):
    with open(file) as cfg_file:  
     return json.load(cfg_file)

def extract_currency(filename):
    # Quick workaround to currency pair name from 10 min data files
    return filename[(filename.find('spot_') + 5) :  filename.find('spot_') + 12]

def extract_month(filename):
    # Quick workaround to extract name from 10 min data files
    return filename[(filename.find('min_') + 4) :  filename.find('min_') + 10]

def get_all_config_results(cfg, filepath):
    # A bit messy. Creates a table of resulted fitness for each algorithm configuration on each month
    with open(filepath) as cfg_file:  
     all_cfg = json.load(cfg_file)
    df = pd.DataFrame(columns=['config name','data file','mdd', 'no_of_short_selling_transactions', 'no_of_transactions', 'noop', 'realised_profit', 'ret', 'u_buy', 'u_sell', 'value', 'wealth'])
    for config in all_cfg:
        for f in cfg['data']['files']:
            fp = '../' + all_cfg[config]['base_results_file_path'] + f + '/pickles/average_fitness.pickle'
            p = pd.Series(pickle.load(open(fp,"rb")), name=(config+' '+f))
            p['config name'] = config
            p['data file'] = f
            p['month'] = extract_month(f)
            p['currency'] = extract_currency(f)
            df = df.append(p)
    return df

def get_ga_results(cfg):
    return pd.concat((pd.read_csv(
                    '../' + cfg['ga']['base_results_file_path'] + f + '/average_fitness.csv'
                    ) for f in cfg['data']['files'])).reset_index().drop('index',1)

def get_monthly_ga_results(cfg):
    # A bit messy. Creates a table of resulted fitness for each algorithm configuration on each month
    df = pd.DataFrame(columns=['config name','data file'])
    for f in cfg['data']['files']:
        p = pd.read_csv('../' + cfg['ga']['base_results_file_path'] + f + '/average_fitness.csv')
        p['config name'] = 'ga'
        p['data file'] = f
        p['month'] = extract_month(f)
        p['currency'] = extract_currency(f)
        p.index = ['ga'+ ' ' + f]
        df = df.append(p,sort=False)
    df.rename(columns={'noOfTransactions':'no_of_transactions', 'noOfShortSellingTransactions':'no_of_short_selling_transactions', 'return':'ret'}, inplace=True)
    return df

def plot_configs(df):
    plt.plot(df.loc['value'], label='fitness')
    plt.plot(df.loc['mdd'])
    plt.plot(df.loc['ret'], label='return')
    plt.xticks(rotation=20)
    plt.xlabel('Configurations', size=14)
    plt.ylabel('Value', size=14)
    plt.title("Average fitness value on test months for 4 currency pairs")
    plt.legend()
    plt.show()

def plot_time(df):
    plt.plot(df.loc['time'])
    plt.xticks(rotation=20)
    plt.xlabel('Configurations', size=14)
    plt.ylabel('Execution time', size=14)
    plt.title("Average exec time on test months for 4 currency pairs")
    plt.legend()
    plt.show()

def get_algo_configurations(file):
    with open(file) as cfg_file:  
        c = json.load(cfg_file)
    return pd.DataFrame(c)