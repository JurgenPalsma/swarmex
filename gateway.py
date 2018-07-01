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
