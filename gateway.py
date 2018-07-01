from py4j.java_gateway import JavaGateway, GatewayParameters

gateway = JavaGateway(gateway_parameters=GatewayParameters(port=27135))
ga = gateway.entry_point

double_class = gateway.jvm.double

indiv = gateway.new_array(double_class, 10)

indiv[0] = 134.0
indiv[1] = 0.3434593504962303
indiv[2] = 0.8807313175318929
indiv[3] = 0.0
indiv[4] = 0.9790021314573502
indiv[5] = 0.296501
indiv[6] = 0.398711
indiv[7] = 0.639533
indiv[8] = 0.833413
indiv[9] = 0.700392

print(ga.fitnessGateway(indiv))
