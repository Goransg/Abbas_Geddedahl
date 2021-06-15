import math as m
import random as rd


class animal(object):
    """
    Represents an individual animal of any of the two kinds.

    :param weight: Float number representing the weight of an animal
    :param age: Integer representing the age of an animal
    """

    def __init__(self, weight, age):

        self.weight = weight
        self.age = age
        self.fitness = self.fitness_update()
        self.migrated = False

    def fitness_update(self):
        """
        Calculating the fitness of the animal; if the weight is negative or zero, the fitness will be zero.
        The fitness is otherwise calculated as follows:

        .. math::
            \\frac{1}{1-e^{\\theta_{a}({a-a_{\\frac{1}{2}}})}}\\times\\frac{1}{1-e^{-\\theta_{w}({w-w_{\\frac{1}{2}}})}}

        Where a is the animal age, w is the animal weight, and the rest are constants from the animals' species.
        :return fitness: float number between 0 and 1
        """


        if self.weight <= 0:
            fitness = 0

        else:
            fitness = (1 / (1 + m.e ** (self.phi_age * (self.age - self.a_half)))) * \
                      (1 / (1 + m.e ** (-self.phi_weight * (self.weight - self.w_half))))
        return fitness

    def birth(self, n_animals):
        """
        Calculating the probability of an individual animal giving birth, and whether it should happen or not.
        If the weight of the mother is less than the weight of the child + the standard deviation of birthweight, the
        birth will not occur.
        Otherwise, the probability of an animal giving birth is:

        .. math::
            min(1, \\gamma \\times \\Phi \\times(N-1)

        Where :math:`\\Phi` is the animal fitness and N is the number of animals in the cell of the same species.
        The rest are constants from the animals' subclass

        :param n_animals: Integer representing the number of animals on the island.
        :return child object/None: returning a child object if birth is given, or None if not.
        """

        if (self.weight <= self.zeta * (self.w_birth + self.sigma_birth)) or n_animals < 2:
            return None

        else:
            birth_proba = min(1, self.gamma * self.fitness * (n_animals - 1))

            if rd.uniform(0, 1) <= birth_proba:
                nw = rd.gauss(self.w_birth, self.sigma_birth)
                if nw > 0 and ((self.xi * nw) < self.weight):
                    return type(self)(nw, 0)
                else:
                    return None

            else:
                return None

    def death(self):
        """
        Calculating the probability of death for a given animal, and deciding if death will occur or not.
        If an animal's weight is zero or less, the animal will die. Otherwise, the probability of any anymal dying
        during any year is:

        .. math::
            \\omega(1-\\Phi)

        Where omega is a constant from the animal species, and Phi is the fitness of the animal.

        :return boolean: returning True if the animal dies and false if it survives.
        """

        if self.weight <= 0:
            return True

        else:
            death_proba = self.omega * (1 - self.fitness)
            if rd.uniform(0, 1) <= death_proba:
                return True

            else:
                return False

    def migration(self):
        """
        Calculating probability of migration, and deciding whether the animal will migrate or not.

        The probability of an animal migrating in a given year is as follows:

        .. math::
            \\mu \\times \\Phi

        Where :math:`\\Phi` is the animal's fitness and :math:`\\mu` is a constant of the species.

        :return boolean: returning True if the animal migrates and false if it stays in its current cell.
        """

        migration_proba = self.mu * self.fitness
        if rd.uniform(0, 1) <= migration_proba and self.migrated is False:
            return True
        else:
            return False

    def aging(self):
        """
        Increases the age of an animal and subtracts yearly weight loss.
        Fitness is updated for the animal after the weight loss.

        """

        self.age += 1
        self.weight -= (self.eta * self.weight)

        self.fitness = self.fitness_update()
        self.migrated = False

    @classmethod
    def update_params(cls, paramchange):
        """
        Changes the constant parameters for a given animal type.
        Parameter has to be known in the animals' class.

        :param paramchange: A dictionary with the parameters to be changed, and the value they shall be changed to.
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


class herbivore(animal):
    """
    Object representing an animal of the herbivore kind.

    :param age: Age of the animal
    :param weight: Weight of the animal

    """
    w_birth = 8
    sigma_birth = 1.5
    beta = 0.9
    eta = 0.05
    a_half = 40
    phi_age = 0.6
    w_half = 10
    phi_weight = 0.1
    mu = 0.25
    gamma = 0.2
    zeta = 3.5
    xi = 1.2
    omega = 0.4
    F = 10

    def __init__(self, weight, age):
        super().__init__(weight, age)

    def feeding(self, f_available):
        """
        Takes amount of available fodder, adds the fodder eaten by animal to its weight, and updates fitness.
        If less than desired fodder (F) is present, it will eat all available.

        :param f_available: Integer representing the amount of available fodder in the cell.
        :return cur_fodder: Integer representing the amount of fodder left in the cell after the animal has eaten.
        """

        cur_fodder = f_available

        if f_available >= self.F:
            self.weight += (self.beta * self.F)
            cur_fodder -= self.F

        else:
            self.weight += (self.beta * f_available)
            cur_fodder -= f_available

        self.fitness = self.fitness_update()

        return cur_fodder


class carnivore(animal):
    """
    Object representing an animal of the carnivore kind.

    :param age: Age of the animal
    :param weight: Weight of the animal

    """
    w_birth = 6
    sigma_birth = 1
    beta = 0.75
    eta = 0.125
    a_half = 40
    phi_age = 0.3
    w_half = 4
    phi_weight = 0.4
    mu = 0.4
    gamma = 0.8
    zeta = 3.5
    xi = 1.1
    omega = 0.8
    F = 50
    DeltaPhiMax = 10

    def __init__(self, weight, age):
        super().__init__(weight, age)

    def feeding(self, available_herbivores):
        """
        Simulates the carnivore trying to eat the herbivores in a cell.
        The carnivore will try to eat herbivores as long as it has appetite (F), or until all herbivores are hunted.
        This is done by calculating the probability of the carnivore eating a given herbivore,
        and decides whether it will happen or not.
        If the fitness of a herbivore is larger than that of the carnivore, the probability of the carnivore eating
        the herbivore is 0. If the carnivore has DeltaPhiMax more fitness than the herbivore, the probability is 1.
        If the carnivore eats a herbivore, its weight is increased, and herbivore is removed from cell.
        If none of the above occur, the probability is calculated as follows:

        .. math::
            \\frac{\\Phi_{carn}-\\Phi_{herb}}{\\Delta\\Phi_{max}}

        Where :math:`\\Phi` is the fitness of the respective animals and :math:`\\Delta\\Phi_{max}` is a constant
        of the carnivores.
        Fitness of the carnivore is updated after it has eaten what it wants or hunted all herbivores.

        :param available_herbivores: list of herbivores available in the cell, sorted by ascending fitness.
        :return living_herbivores: list of herbivores alive in the cell after the carnivore has hunted.
        """

        appetite = self.F
        living_herbivores = available_herbivores

        for prey in available_herbivores:

            if prey.fitness > self.fitness:
                p_eat = 0

            elif (self.fitness - prey.fitness) > self.DeltaPhiMax:
                p_eat = 1

            else:
                p_eat = (self.fitness - prey.fitness) / self.DeltaPhiMax

            if rd.uniform(0, 1) <= p_eat and appetite > 0:
                living_herbivores.remove(prey)
                self.weight += prey.weight * self.beta
                appetite -= prey.weight

        self.fitness = self.fitness_update()

        return living_herbivores
