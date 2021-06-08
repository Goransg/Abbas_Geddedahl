from src.biosim.animals import *


class biome:
    f_max = None
    habitable = None

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
        for specie in self.herb:
            n = len(self.herb)
            result = specie.birth(n)
            if result is not None:
                self.herb.append(result)
                specie.weight -= specie.xi * result.weight
        for specie in self.carn:
            n = len(self.carn)
            result = specie.birth(n)
            if result is not None:
                self.carn.append(result)
                specie.weight -= specie.xi * result.weight

    def aging(self):
        for specie in self.herb:
            specie.aging()
        for specie in self.carn:
            specie.aging()

    def grazing(self):
        for specie in self.herb:
            if self.fodder > 0:
                self.fodder = specie.feeding(self.fodder)
        # for specie in sorted(self.carn, key=lambda x: x.fitness, reverse=True):
        #    if len(self.herb) > 0:
        #        specie.feeding(sorted(self.herb, key=lambda x: x.fitness))

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
        self.habitable = True
        super().__init__(loc)


class highland(biome):

    def __init__(self, loc):
        self.f_max = 300
        self.habitable = True
        super().__init__(loc)


class desert(biome):

    def __init__(self, loc):
        self.f_max = 0
        self.habitable = True
        super().__init__(loc)


class water(biome):

    def __init__(self, loc):
        self.f_max = 0
        self.habitable = False
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
#                    'weight': 8000}])
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
# print(len(A.herb))
# A.breeding()
# print(len(A.herb))
# print(A.get_age())
# print(A.get_weights())
# print(A.get_fitness())
