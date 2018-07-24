# Optimizing FOREX trading strategies with natured-inspired machine learning 

The goal of the project is to optimize trading strategies based on Directional Changes using nature inspired optimization algorithms.

Algorithms used:

- Particle Swarm Optimization (PSO)
- A custom algo based on shuffled frog leaping - Continuous Shuffled Frog Leaping (CSFLA)

To do so, I use the trading strategy provided by [[1]](http://www.kampouridis.net/papers/DC-GA.pdf) which use Genetic Algorithms to find a suitable set of parameters for a Directional Change - based strategy.

The problem is this resumed to optimizing a fitness function - which is the performance of the trading strategy given a set of parameters.

To ensure robustness of my proposed algorithm, I test it with the same configuration that the authors in [[1]](http://www.kampouridis.net/papers/DC-GA.pdf).


## Running the experiment:

**The following steps allow you to test a condensed experiment so that you don't waste your time - the Genetic Algorithm's results are already provided, and the PSO is only ran 3 times.**


Step 1: run the java server which generates directional change events from the FOREX data (a sample is provided) under the same conditions as in [[1]](http://www.kampouridis.net/papers/DC-GA.pdf).
```
java -jar dc-server.jar data/fx-spot_EUR_GBP_10min_201308.txt:fx-spot_EUR_GBP_10min_201308:0:20:21:27 1000 35 4 0.90 0.10 0.0025 5 200 500000 -1 0.2 3 1 0.01
```

Step 2: run the PSO algorithm 
```
python main.py
```

Step 3 (optional): run a Kolmogorov-Smirnov test on GA and PSO generated individuals to make sure we sample from the same distribution and that our results are not just random (results from longer experiments are provided when running the test)
```
python kstest.py 
```


## References:
[[1]](http://www.kampouridis.net/papers/DC-GA.pdf) - M. Kampouridis and F. E. B. Otero, "Evolving trading strategies using directional changes," Expert Systems with Applications, vol. 73, pp. 145-160, 2017.
