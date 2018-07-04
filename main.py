from pso import PSO
from javafitness import JavaFitness
from particle import Particle

if __name__== "__main__":
    fitness_function = JavaFitness()
    #pso = PSO()
    #pso.optimize(fitness_function)
    p = Particle( fitness_function,
        constraints={'quantity': {'min': 0, 'max': 100},
        'b_start': {'min': 0.0, 'max': 1.0},
        'b_end': {'min': 0.0, 'max': 1.0},
        'b_price': {'min': 0.0, 'max': 1.0},
        'threshold_weights': {'min': 0.0, 'max': 1.0},
        'q_short': {'min': 0, 'max': 100}})