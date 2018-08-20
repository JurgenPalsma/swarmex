# Optimizing FOREX trading strategies with natured-inspired machine learning 

The goal of the project is to optimize trading strategies based on Directional Changes using nature inspired optimization algorithms.

Algorithms used:

- Particle Swarm Optimization (PSO)
- A custom algo based on shuffled frog leaping - Continuous Shuffled Frog Leaping (CSFLA)

To do so, I use the trading strategy provided by [[1]](http://www.kampouridis.net/papers/DC-GA.pdf) which use Genetic Algorithms to find a suitable set of parameters for a Directional Change - based strategy.

The problem can be resumed to optimizing a fitness function - which is the performance of the trading strategy given a set of parameters.

To ensure robustness of my proposed algorithms, I test them with the same configuration that the authors in [[1]](http://www.kampouridis.net/papers/DC-GA.pdf).


# Contents
    Setup libs
    conda create --name <env> --file <this file>
    or
    pip install requirements.txt
    Simple run example


## The experiment:
    
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
