# Optimizing FOREX trading strategies with natured-inspired machine learning 

The goal of the project is to optimize trading strategies based on Directional Changes using nature inspired optimization algorithms.

Algorithms used:

- Particle Swarm Optimization (PSO)
- A custom algo based on shuffled frog leaping - Continuous Shuffled Frog Leaping (CSFLA)

To do so, I use the trading strategy provided by [[1]](http://www.kampouridis.net/papers/DC-GA.pdf) which use Genetic Algorithms to find a suitable set of parameters for a Directional Change - based strategy.

The problem can be resumed to optimizing a fitness function - which is the performance of the trading strategy given a set of parameters.

To ensure robustness of my proposed algorithms, I test them with the same configuration that the authors in [[1]](http://www.kampouridis.net/papers/DC-GA.pdf).


# Contents
This repository contains:
   1. Custom, from scratch implementations of the PSO and CSFLA algorithms, in the `.py` files in the root of the repository
   2. 3 months of 10-min FOREX data on 3 currency pairs, in the `data/` folder, used to train/test the algorithms
   3. Configuration files, in the `config/` folder
   4. Analysis notebooks in the `analysis/` folder that cover 
                                    - the algorithm parameter tuning process
                                    - trading strategy performance on the test data
   5. Results of all the experimented and final strategies, in the `results.zip` file
   6. Project documentation, including UML and meeting powerpoints, in the `docs/` folder

# The experiment:
## Installing required packages:

1. Recommended installation:
   - Install [Anaconda CLI](https://anaconda.org/) , See [docs](https://conda.io/docs/user-guide/tasks/manage-environments.html)
   - Install the required libraries:
```
# Make sure to replace <envname> with the name of your env
conda create --name <envname> --file requirements.txt
```
On Windows, in your Anaconda Prompt, run `activate <envname>`

On macOS and Linux, in your Terminal Window, run `source activate <envname>`

OR Installation with pip (less recommended)
   - Install the required libraries with [pip](https://pypi.org/project/pip/):
```
    pip install requirements.txt
```
2. Install an [Ipython](https://jupyter.org/) notebook reader (provided by [Anaconda CLI](https://anaconda.org/) )

## Running a short demo:
If you simply to test out the system, you can run the simplified (and thus poorly performing!) algorithms on one month of data for one currency pair:
```
    python main.py -c ./config/demo.json
```

## Running the full experiment (optional):
The full experiment generates all the configurations results (51 PSO configurations, 41 CSFLA configurations) on test and training data. This can take up to several days if your machine has low computational power. 

__Pre-computed results__ can be extracted from the given `results.zip` file:
```
    unzip results.zip
```

Otherwise, to run the full experiment:

__On the training data__:
```
    python main.py -c ./config/training_config.json -p config/algos/pso_param_exp_configs.json -f config/algos/csfla_param_exp_configs.json -o
    python main.py -c ./config/training_config.json -p config/algos/pso_configs.json -f config/algos/csfla_params_config_2.json -o
    python main.py -c ./config/training_config.json -p config/algos/pso_configs_2.json -f config/algos/csfla_configs.json -o
    python main.py -c ./config/training_config.json -p config/algos/pso_configs_3.json -o
```

__On the testing data__:
```
    python main.py -c ./config/testing_config.json -p config/algos/pso.json -f config/algos/csfla.json -g
```

## Analysing the results

__Static notebooks__:

To read the notebooks without making changes and having to get the data, you can open the `.html` files in the 
`analysis/` folder.

The `test_data_analysis.html` file presents an analysis of the results of the algorithms on the test 

The `preliminary_pso_tuning_analysis.html` and `indepth_pso_tuning.html` files present parameter tuning analysis of the PSO.

The `preliminary_csfla_tuning_analysis.html` and `indepth_csfla_tuning.html` files present parameter tuning analysis of the CSFLA.


__To run the interactive notebooks__:

Make sure you have either extracted the provided results, or generated the training data.

Run the Ipython notebooks in the `analysis/` folder.

The `test_data_analysis.ipynb` notebook presents an interactive analysis of the results of the algorithms on the test 

The `preliminary_pso_tuning_analysis.ipynb` and `indepth_pso_tuning.ipynb` notebooks present interactive parameter tuning analysis of the PSO.

The `preliminary_csfla_tuning_analysis.ipynb` and `indepth_csfla_tuning.ipynb` notebooks present interactive parameter tuning analysis of the CSFLA.


## References:
[[1]](http://www.kampouridis.net/papers/DC-GA.pdf) - M. Kampouridis and F. E. B. Otero, "Evolving trading strategies using directional changes," Expert Systems with Applications, vol. 73, pp. 145-160, 2017.
