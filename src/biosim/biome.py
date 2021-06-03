from src.biosim.animals import *


class biome:
    f_max = None

    def __init__(self, loc):
        self.loc = loc
        self.fodder = self.f_max
        self.herb = []
        self.carn = []

    def add_population(self,pop):
        for specie in pop:
            specie['specie']
            self.herb.append()



class lowland(biome):

    def __init__(self, loc):
        self.f_max = 800
        super.__init__(loc)


class highland(biome):

    def __init__(self, loc):
        self.f_max = 300
        super.__init__(loc)


class desert(biome):

    def __init__(self, loc):
        self.f_max = 0
        super.__init__(loc)


class water(biome):

    def __init__(self, loc):
        self.f_max = 0
        super.__init__(loc)