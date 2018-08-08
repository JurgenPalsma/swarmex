# Optimizing FOREX trading strategies with natured-inspired machine learning 

The goal of the project is to optimize trading strategies based on Directional Changes using nature inspired optimization algorithms.

Algorithms used:

- Particle Swarm Optimization (PSO)
- A custom algo based on shuffled frog leaping - Continuous Shuffled Frog Leaping (CSFLA)

To do so, I use the trading strategy provided by [[1]](http://www.kampouridis.net/papers/DC-GA.pdf) which use Genetic Algorithms to find a suitable set of parameters for a Directional Change - based strategy.

The problem is this resumed to optimizing a fitness function - which is the performance of the trading strategy given a set of parameters.

To ensure robustness of my proposed algorithm, I test it with the same configuration that the authors in [[1]](http://www.kampouridis.net/papers/DC-GA.pdf).


## Running the experiment:

Step 1: run the algorithms

Config files are configurated for an example experiment. The example experiment only runs for one currency pair, on one month of 10 minute data.
```
python main.py -c config/config.json
```

Everything is configurable, feel free to check the configs files and the different running flags
```
python main.py -h
```



Step 2 (optional): analyse the results by running the ipython notebooks in the ```analysis/``` folder with [jupyter](http://jupyter.readthedocs.io/en/latest/running.html) 


Step 3 (optional, not automated yet): run a Friedman statistical test on generated individuals


## References:
[[1]](http://www.kampouridis.net/papers/DC-GA.pdf) - M. Kampouridis and F. E. B. Otero, "Evolving trading strategies using directional changes," Expert Systems with Applications, vol. 73, pp. 145-160, 2017.
