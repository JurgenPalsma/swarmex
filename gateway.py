from py4j.java_gateway import JavaGateway, GatewayParameters

class pjGateWay:

    def __init__(self, port):
        self.port = port
        self.way = JavaGateway(gateway_parameters=GatewayParameters(port=self.port))


class fGateway(pjGateWay):

    def __init__(self, port):
        pjGateWay.__init__(self, port)
        self.ga = self.way.entry_point
    
    def fitness(self, individual):
        j_indiv = self.way.new_array(self.way.jvm.double, len(individual))
        
        for i in range(0, len(individual)):
            j_indiv[i] = individual[i]
        
        return self.way.fitnessGateway(j_indiv)

#gateway = fGateway(27135)
#individual = [134.0, 0.3434593504962303, 0.8807313175318929, 0.0, 0.9790021314573502, 0.296501, 0.398711, 0.639533, 0.833413, 0.700392]
#print(gateway.fitness(individual))