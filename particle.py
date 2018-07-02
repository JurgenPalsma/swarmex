from fitness import Fitness

class Particle:
    
    def __init__(self):
        self.current_fit = Fitness()
        self.historical_fit = Fitness()
        self.neighbour_fit = Fitness()
        self.coordinates = []
        self.velocity = []

    def update_velocity(self):
        pass

    def __clamp(self):
        pass
    
    def __compute_neighbour_fitness(self):
        pass