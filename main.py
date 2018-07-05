from pso import PSO
from javafitness import JavaFitness
from particle import Particle

if __name__== "__main__":
    fitness_function = JavaFitness()

    #print("Testing with: w_inertia:%f, w_hist:%f, w_neigh:%f" %)
    for i in range(0, 10):
        print("Run: %i" % i)
        pso = PSO(swarm_size=10)
        pso.optimize(fitness_function)