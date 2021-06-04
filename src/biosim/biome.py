from src.biosim.animals import *


class biome:
    f_max = None

    def __init__(self, loc):
        self.loc = loc
        self.fodder = self.f_max
        self.herb = []
        self.carn = []

    def update_fodder(self):
        self.fodder = self.f_max

    def add_population(self, pop):
        for specie in pop:
            if specie['species'] == 'Herbivore':
                self.herb.append(herbivore(specie['age'], specie['weight']))
            elif specie['species'] == 'Carnivore':
                self.carn.append(herbivore(specie['age'], specie['weight']))

    def remove_population(self):
        self.herb[:] = [specie for specie in self.herb if not specie.death()]
        self.carn[:] = [specie for specie in self.carn if not specie.death()]

    def grazing(self):
        pass

    def breeding(self):
        pass








class lowland(biome):

    def __init__(self, loc):
        self.f_max = 800
        super().__init__(loc)


class highland(biome):

    def __init__(self, loc):
        self.f_max = 300
        super().__init__(loc)


class desert(biome):

    def __init__(self, loc):
        self.f_max = 0
        super().__init__(loc)


class water(biome):

    def __init__(self, loc):
        self.f_max = 0
        super().__init__(loc)

A = lowland((1,1))
A.add_population([{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}])
A.add_population([{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}])
A.add_population([{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}])
print(A.herb)
A.remove_population()
print(A.herb)