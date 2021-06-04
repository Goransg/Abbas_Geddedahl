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
                self.herb.append(herbivore(specie['weight'], specie['age']))
            elif specie['species'] == 'Carnivore':
                self.carn.append(carnivore(specie['weight'], specie['age']))

    def remove_population(self):
        self.herb[:] = [specie for specie in self.herb if not specie.death()]
        self.carn[:] = [specie for specie in self.carn if not specie.death()]

    def breeding(self):

        pass

    def aging(self):
        for specie in self.herb:
            specie.aging()
        for specie in self.carn:
            specie.aging()

    def grazing(self):
        for specie in self.herb:
            if self.fodder>0:
                self.fodder = specie.feeding(self.fodder)
        for specie in self.carn:
            pass

    # def get_age(self):
    #     ages = []
    #     for specie in self.herb:
    #         ages.append(specie.age)
    #     return ages
    #
    # def get_weights(self):
    #     weights = []
    #     for specie in self.herb:
    #         weights.append(specie.weight)
    #     return weights
    #
    # def get_fitness(self):
    #     fitnesslist = []
    #     for specie in self.herb:
    #         fitnesslist.append(specie.fitness)
    #     return fitnesslist


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


# A = lowland((1, 1))
# A.add_population([{'species': 'Herbivore',
#                    'age': 5,
#                    'weight': 200}])
# A.add_population([{'species': 'Herbivore',
#                    'age': 25,
#                    'weight': 0}])
# A.add_population([{'species': 'Herbivore',
#                    'age': 25,
#                    'weight': 200}])
# print(A.herb)
# A.remove_population()
# print(A.herb)
# A.aging()
# print(A.get_age())
# print(A.get_weights())
# print(A.get_fitness())
# print(A.fodder)
# A.aging()
# A.grazing()
# print(A.get_age())
# print(A.get_weights())
# print(A.get_fitness())
# print(A.fodder)
