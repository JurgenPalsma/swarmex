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

Everything is pre-configured and can be modified in the ```config.json ``` file
```
python main.py -c config.json
```

Step 2 (optional): analyse the results by running the ipython notebook(s) with [jupyter](http://jupyter.readthedocs.io/en/latest/running.html) 

Step 3 (optional): run a Kolmogorov-Smirnov test on GA and PSO generated individuals to make sure we sample from the same distribution and that our results are not just random (results from longer experiments are provided when running the test)
```
python kstest.py 
```


## References:
[[1]](http://www.kampouridis.net/papers/DC-GA.pdf) - M. Kampouridis and F. E. B. Otero, "Evolving trading strategies using directional changes," Expert Systems with Applications, vol. 73, pp. 145-160, 2017.
