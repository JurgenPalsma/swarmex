from fitness import AFitnessFunction
from gateway import fGateway
from individual import Individual

class JavaFitness(AFitnessFunction):

    def __init__(self, port=27131):
        self.gateway = fGateway(port)
        pass

    def fitness(self, individual: Individual):
        return self.gateway.fitness(individual)
