import math as m
import random as rd
import operator


class animal(object):

    def __init__(self, weight, age, seed=rd.randint(0, 9999999)):
        # self.species = species
        self.weight = weight
        self.age = age
        self.seed = seed
        rd.seed(a=self.seed)
        self.fitness = self.fitness_update()
        self.migrated = False

    def fitness_update(self):
        # Calculating the fitness of the animal; if the weight is negative or zero, the fitness will be zero.
        # Variables in use: a and w. The rest is defined for the respective species.

        if self.weight <= 0:
            fitness = 0

        else:
            fitness = (1 / (1 + m.e ** (self.phi_age * (self.age - self.a_half)))) * \
                      (1 / (1 + m.e ** (-self.phi_weight * (self.weight - self.w_half))))
        return fitness

    # def birth(self, n_animals):
    #     # Calculating the possibility and probability of birth, returning True if birth and false if not birth.
    #
    #     if self.weight <= self.zeta * (self.w_birth + self.sigma_birth):
    #         return False
    #
    #     else:
    #         birth_proba = min(1, self.gamma * self.fitness * (n_animals - 1))
    #
    #         if rd.uniform(0, 1) <= birth_proba:
    #             return True
    #
    #         else:
    #             return False

    def birth(self, n_animals, avg, std):
        # Calculating the possibility and probability of birth, returning True if birth and false if not birth.

        if self.weight <= self.zeta * (self.w_birth + self.sigma_birth):
            return None

        else:
            birth_proba = min(1, self.gamma * self.fitness * (n_animals - 1))

            if rd.uniform(0, 1) <= birth_proba:
                nw = rd.gauss(avg, std)
                if nw > 0 and ((self.xi * nw) > self.weight):
                    return None
                elif nw > 0:
                    return type(self)(nw, 0), self.weight - (self.xi * nw)

            else:
                return None

    def death(self):
        # Calculating the probability of death, also simulating if the death will occur.

        if self.weight <= 0:
            return True

        else:
            death_proba = self.omega * (1 - self.fitness)

            if rd.uniform(0, 1) <= death_proba:
                return True

            else:
                return False

    def migration(self):
        # Calculating probability of migration, and deciding whether the animal will migrate or not.

        migration_proba = self.mu * self.fitness
        print(self.mu)
        if rd.uniform(0, 1) <= migration_proba and self.migrated is False:
            return True
        else:
            return False

    def aging(self):
        # Increases the age of an animal and subtracts yearly weight loss

        self.age += 1
        self.weight -= (self.eta * self.weight)

        self.fitness = self.fitness_update()

    @classmethod
    def update_params(cls, paramchange):
        for param in paramchange[1].keys():
            classname = cls.__name__
            if param in dir(cls):
                try:
                    paramname = classname + '.' + param
                    exec("%s = %f" % (paramname, paramchange[1][param]))
                    print(paramchange[1][param])

                except:
                    warnings.warn(param + ' ' + 'is not a valid class parameter, and will not be updated.')
            else:
                raise ValueError('Unknown parameter inserted')


class herbivore(animal):
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

    def __init__(self, weight, age, seed=rd.randint(0, 9999999)):
        super().__init__(weight, age, seed)

    def feeding(self, f_available):
        # Takes amt of available fodder, adds the fodder eaten by animal to its weight.
        # If less than desired fodder (F) is present, it will eat all available.
        # Returns the remaining fodder in the cell after the animal has eaten.

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

    def __init__(self, weight, age, seed=rd.randint(0, 9999999)):
        super().__init__(weight, age, seed)

    def feeding(self, prey):

        # available_herbivores.sort(key=operator.attrgetter('fitness'))

        if prey.fitness > self.fitness:
            p_eat = 0

        elif (self.fitness - prey.fitness) > self.DeltaPhiMax:
            p_eat = 1

        else:
            p_eat = (self.fitness - prey.fitness) / self.DeltaPhiMax

        if rd.uniform(0, 1) <= p_eat and appetite > 0:
            return True

        else:
            return False
