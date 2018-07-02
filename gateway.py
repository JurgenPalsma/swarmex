from py4j.java_gateway import JavaGateway, GatewayParameters
from individual import Individual

class pjGateWay:

    def __init__(self, port):
        self.port = port
        self.way = JavaGateway(gateway_parameters=GatewayParameters(port=self.port))


class fGateway(pjGateWay):

    def __init__(self, port):
        pjGateWay.__init__(self, port)
        self.ga = self.way.entry_point
    
    def fitness(self, individual: Individual):        
        j_indiv = self.__convert_individual_p_to_j(individual)
        
        
        return  self.way.fitnessGateway(j_indiv)
        #self.__convert_fitness_j_to_p(self.way.fitnessGateway(j_indiv))
        
    def __convert_individual_p_to_j(self, individual: Individual):
        p_len = 5 + len(individual.threshold_weights)
        t_indiv = self.way.new_array(self.way.jvm.double, p_len)

        t_indiv[0] = individual.quantity
        t_indiv[1] = individual.b_start
        t_indiv[2] = individual.b_end
        t_indiv[3] = individual.q_short
        t_indiv[4] = individual.b_price
        
        for i in range(0, individual.threshold_number):
            t_indiv[i + 5] = individual.threshold_weights[i]
        return t_indiv

    def __convert_fitness_j_to_p(self, fitness):
        # TODO
        return fitness

#gateway = fGateway(27135)
#individual = [134.0, 0.3434593504962303, 0.8807313175318929, 0.0, 0.9790021314573502, 0.296501, 0.398711, 0.639533, 0.833413, 0.700392]
#print(gateway.fitness(individual))