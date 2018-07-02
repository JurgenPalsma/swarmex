from fitness import AFitnessFunction
from gateway import fGateway

class JavaFitness(AFitnessFunction):

    def __init__(self, port=27135):
        self.gateway = fGateway(port)
        pass

    def fitness(self, individual):
        return self.__convert_java_fitness(self.gateway.fitness(individual))

    def __convert_java_fitness(self, fitness):
        return fitness