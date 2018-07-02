from pso import PSO
from javafitness import JavaFitness

if __name__== "__main__":
    fitness_function = JavaFitness()
    pso = PSO()
    pso.optimize(fitness_function)