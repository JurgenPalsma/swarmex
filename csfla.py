from optimizer import AOptimizer
from frog import Frog
import numpy as np 
import pandas as pd

class CSFLA(AOptimizer):
    """
    CSFLA algorithm encapsulation.
    """

    def __init__(self, n, m, sn, Gm = 10, Gs = 10, constraints={'quantity': {'min': 0, 'max': 100},
                                                                'b_start': {'min': 0.0, 'max': 1.0},
                                                                'b_end': {'min': 0.0, 'max': 1.0},
                                                                'b_price': {'min': 0.0, 'max': 1.0},
                                                                'threshold_weights': {'min': 0.0, 'max': 1.0},
                                                                'q_short': {'min': 0, 'max': 100}}):
        self.n = n # number of frogs in pop
        self.sn = sn # number of frogs picked for sub-memeplex
        self.m = m # number of memeplexes
        self.Gm = Gm
        self.Gs = Gs
        self.constraints = constraints

    def __populate(self):
        self.pop = [ Frog(function=self.ff,
                        constraints=self.constraints)
                        for i in range(self.n)]

        for idx, f in enumerate(self.pop):
            while f.current_fit.ret == 0:
                f = Frog(function=self.ff,
                        constraints=self.constraints)
            self.pop[idx] = f
           
    def __divide(self):
        memeplexes = list()
        for sub_list_count in range(self.m):
            memeplexes.append(self.pop[sub_list_count::self.m])
        return memeplexes

    def __subdivide(self, memeplex):
        memeplex.sort(key=lambda x: x.current_fit.ret, reverse=True)
        pbs = list()
        submemeplex = list()
        for i, f in enumerate(memeplex):
            pbs.append((2 * (self.n + 1 - i)) / (self.n * (self.n + 1)))
        
        for i in range(self.sn):
            submemeplex.append(np.random.choice(memeplex, 1, pbs)[0])
        return submemeplex


    def __evolve(self, sub):
        xb = sub[0]
        xw = sub[-1]
        xs = self.pop[0]
        r = np.random.uniform(0, 1)

        # Try to learn from local best
        xt = xb - xw
        xt.p = xw.p + r * (xt.p)
        if (xt.current_fit.ret > xw.current_fit.ret):
            sub[-1] = xt
            return sub

        else:
            # Try to learn from local best
            xt = xs - xw
            xt.p = xw.p + r * (xt.p)
            if (xt.current_fit.ret > xw.current_fit.ret):
                sub[-1] = xt
                return sub
            
            else:
                # Randomize the worst frog in the submemeplex
                sub[-1] = Frog(self.ff, self.constraints)
                return sub


    def optimize(self, ff):
        self.ff = ff

        self.__populate()

        self.pop.sort(key=lambda x: x.current_fit.ret, reverse=True) # sort by descending fitness

        gm = 0 # max generation
        gs = 0 # max memeplex iteration

        while gm < self.Gm:
            memeplexes = self.__divide()
            new_generation = list()
            for memeplex in memeplexes:
                submemeplex = self.__subdivide(memeplex)
                while gs < self.Gs:
                    submemeplex = self.__evolve(submemeplex)
                    gs += 1
                new_generation.extend(submemeplex)
            self.pop = new_generation
            self.pop.sort(key=lambda x: x.current_fit.ret, reverse=True) # sort by descending fitness
            #print("Generation: %d" % gm)
            #print(self.pop[0].current_fit)
            gm += 1

        return self.pop[0]
        

        