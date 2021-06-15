from .animals import herbivore, carnivore
import random as rd


class biome:
    """
    The biome class

    :param loc: a tuple containing the coordinates of the cell.
    """
    f_max = None
    habitable = None

    def __init__(self, loc):
        self.loc = loc
        self.fodder = self.f_max
        self.herb = []
        self.carn = []

    def update_fodder(self):
        """
        Function to update fodder amount on yearly cycle
        """
        self.fodder = self.f_max

    @staticmethod
    def change_animalparams(species, params):
        """
        Changes the constant parameters of a given animal type.
        Runs function :func:`animals.animal.update_params` for the specified animal type.

        :param species: a text string representing the animal type to be updated
        :param params: a dictionary of constant names to be updated,
        with values they are going to be set to as values.
        """
        if species.lower() == 'herbivore':
            herbivore.update_params(params)
        elif species.lower() == 'carnivore':
            carnivore.update_params(params)
        else:
            raise KeyError('unknown species specified')

    def add_population(self, pop):
        """
        Function to add population in a specific cell.

        :param pop: List of dictionaries
        """
        for specie in pop:
            if specie['species'].lower() == 'herbivore':
                self.herb.append(herbivore(specie['weight'], specie['age']))
            elif specie['species'].lower() == 'carnivore':
                self.carn.append(carnivore(specie['weight'], specie['age']))

    def remove_population(self):
        """
        Simulates the yearly deaths in the cell.
        Runs the :func:`animals.animal.death` function for all animals in the cell.
        """
        self.herb[:] = [specie for specie in self.herb if not specie.death()]
        self.carn[:] = [specie for specie in self.carn if not specie.death()]

    def breeding(self):
        """
        Simulates the yearly births in the cell,
        adding the child objects and removing weight from mother.
        Runs the :func:`animals.animal.birth` function for all animals in the cell.
        """
        baby_herb = []
        baby_carn = []
        n_herb = len(self.herb)
        n_carn = len(self.carn)
        for specie in self.herb:
            result = specie.birth(n_herb)
            if result is not None:
                baby_herb.append(result)
                specie.weight -= specie.xi * result.weight
                specie.fitness_update()
        self.herb.extend(baby_herb)
        for specie in self.carn:
            result = specie.birth(n_carn)
            if result is not None:
                baby_carn.append(result)
                specie.weight -= specie.xi * result.weight
                specie.fitness_update()
        self.carn.extend(baby_carn)

    def aging(self):
        """
        Running the aging process for all animals in the cell,
        adding age and removing yearly weight loss.

        Runs the :func:`animals.animal.aging` function for all animals in the cell.
        """
        for specie in self.herb:
            specie.aging()
        for specie in self.carn:
            specie.aging()

    def grazing(self):
        """
        Simulates the yearly eating for the two species in the cell.
        Herbivores eat in random order, and carnivores eat in the order of descending fitness.
        Runs the :func:`animals.herbivore.feeding` function for all herbivores in the cell.
        Runs the :func:`animals.herbivore.feeding` function for all carnivores in the cell.
        """
        for specie in self.herb:
            if self.fodder > 0:
                self.fodder = specie.feeding(self.fodder)
        for specie in sorted(self.carn, key=lambda x: x.fitness, reverse=True):
            if len(self.herb) > 0:
                self.herb = specie.feeding(sorted(self.herb, key=lambda x: x.fitness))

    def migration(self, cell_list):
        """
        Runs the migration for all animals in the cell, finding where the animal wants to go,
        and if it is possible.
        If it is possible, the animals are moved.
        Runs the :func:`animals.herbivore.migration` function for all animals in the cell.

        :param cell_list: List of the neighbouring cells to the current cell.
        """
        # for specie in self.herb:
        #     if specie.migration():
        #         choice = rd.choice(cell_list)
        #         if choice.habitable:
        #             choice.immigration(specie)
        #             self.herb.remove(specie)
        # for specie in self.carn:
        #     if specie.migration():
        #         choice = rd.choice(cell_list)
        #         if choice.habitable:
        #             choice.immigration(specie)
        #             self.carn.remove(specie)
        for i in range(len(self.herb) - 1, -1, -1):
            if self.herb[i].migration():
                choice = rd.choice(cell_list)
                if choice.habitable:
                    self.herb[i].migrated = True
                    choice.herb.append(self.herb[i])
                    del self.herb[i]
        for i in range(len(self.carn) - 1, -1, -1):
            if self.carn[i].migration():
                choice = rd.choice(cell_list)
                if choice.habitable:
                    self.carn[i].migrated = True
                    choice.carn.append(self.carn[i])
                    del self.carn[i]

    @classmethod
    def update_params(cls, paramchange):
        """
        Changes the constant parameters for a given biome type.
        Parameter has to be known in the biome class.

        :param paramchange: A dictionary with the parameters to be changed,
        and the value they shall be changed to.
        """
        # for param in paramchange[1].keys():
        #     classname = cls.__name__
        #     if param in dir(cls):
        #         paramname = classname + '.' + param
        #         exec("%s = %f" % (paramname, paramchange[1][param]))
        for param in paramchange.keys():
            classname = cls.__name__
            if param in dir(cls):
                paramname = classname + '.' + param
                exec("%s = %f" % (paramname, paramchange[param]))
            else:
                raise ValueError('Unknown parameter inserted')
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
    """
    Representing a cell of type lowland.

    :param loc: a tuple containing the coordinates of the cell.
    """

    f_max = 800

    def __init__(self, loc):
        # self.f_max = 800
        self.habitable = True
        super().__init__(loc)


class highland(biome):
    """
    Representing a cell of type highland.

    :param loc: a tuple containing the coordinates of the cell.
    """

    f_max = 300

    def __init__(self, loc):
        # self.f_max = 300
        self.habitable = True
        super().__init__(loc)


class desert(biome):
    """
    Representing a cell of type desert

    :param loc: a tuple containing the coordinates of the cell.
    """

    f_max = 0

    def __init__(self, loc):
        # self.f_max = 0
        self.habitable = True
        super().__init__(loc)


class water(biome):

    """
    Representing a cell of type water.

    :param loc: a tuple containing the coordinates of the cell.
    """
    f_max = 0

    def __init__(self, loc):
        # self.f_max = 0
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
# print(A.carn)

# # Test Migration
# A = lowland((5, 5))
# B = lowland((5, 4))
# C = highland((5, 6))
# D = water((4, 5))
# E = desert((6, 5))
# A.add_population([{'species': 'Herbivore',
#                    'age': 25,
#                    'weight': 8000}])
# A.add_population([{'species': 'Herbivore',
#                    'age': 25,
#                    'weight': 0}])
# A.add_population([{'species': 'Herbivore',
#                    'age': 25,
#                    'weight': 8000}])
# print(len(A.herb)+len(A.carn))
# print(len(B.herb)+len(B.carn))
# print(len(C.herb)+len(C.carn))
# print(len(D.herb)+len(D.carn))
# print(len(E.herb)+len(E.carn))
# lst = [B, C, D, E]
# print(lst)
# A.migration(lst)
# print(len(A.herb) + len(A.carn))
# print(len(B.herb) + len(B.carn))
# print(len(C.herb) + len(C.carn))
# print(len(D.herb) + len(D.carn))
# print(len(E.herb) + len(E.carn))
