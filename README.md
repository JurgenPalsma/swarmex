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
    1. Custom, from scratch implementations of the PSO and CSFLA algorithms, in the .py files in the root of the repository
    2. 3 months of 10-min FOREX data on 3 currency pairs, in the data/ folder, used to train/test the algorithms
    3. Configuration files, in the config/ folder
    4. Analysis notebooks in the analysis/ folder that cover 
                                    - the algorithm parameter tuning process
                                    - trading strategy performance on the test data
    5. Results of all the experimented and final strategies, in the results.zip file
    6. Project documentation, including UML and meeting powerpoints, in the docs/ folder

## The experiment:
    
    Installing the program:
    Recommended: 
        - Install [[Anaconda CLI]](https://anaconda.org/)
        - Install the required libraries:
        conda create --name <env> --file <this file>

    Setup libs
    conda create --name <env> --file <this file>
    or
    pip install requirements.txt
    Simple run example
    Umls and diagrams
    

### Training:
    Run on training data
    Or look in results file
    parmas analysis notebooks

### Testing:
    Run on test data
    or look in results file
    performance analysis notebooks





## References:
[[1]](http://www.kampouridis.net/papers/DC-GA.pdf) - M. Kampouridis and F. E. B. Otero, "Evolving trading strategies using directional changes," Expert Systems with Applications, vol. 73, pp. 145-160, 2017.
