from pso import PSO
from javafitness import JavaFitness
from particle import Particle

if __name__== "__main__":
    fitness_function = JavaFitness()
    pso = PSO(swarm_size=5)
    pso.optimize(fitness_function)