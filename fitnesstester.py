from javafitness import JavaFitness, Fitness
from particle import Particle
from individual import Individual, IndividualFromRaw

import os
import json

fitness_function = JavaFitness()

ind = IndividualFromRaw(
                quantity= 22.380026,
                b_start= 0.617859,
                b_end= 0.992353,
                b_price= 0.999910,
                threshold_number=  5,
                threshold_weights= [0.847291, 0.735665,0.870022, 0.620758, 0.856554],
                q_short= 45.417683)


print(fitness_function.testFitness(ind))


"""
Parameter
quantity    22.380026
b_start      0.617859
b_end        0.992353
q_short     45.417683
b_price      0.999950
t1           0.847291
t2           0.735665
t3           0.870022
t4           0.620758
t5           0.856554

"""