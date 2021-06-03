import math as m
import random as rd


class animal(object):

    def __init__(self, species, weight, age, seed = rd.randint(0,9999999)):
        self.species = species
        self.weight = weight
        self.age = age
        self.seed = seed
        rd.seed(a=self.seed)

    def fitness(self):
        # Calculating the fitness of the animal; if the weight is negative or zero, the fitness will be zero.
        # Variables in use: a and w. The rest is defined for the respective species.

        if self.weight <= 0:
            self.fitness = 0

        else:
            self.fitness = (1/(1+m.e**(self.phi_age*(self.age-self.a_half)))) * \
                           (1/(1+m.e**(-self.phi_weight*(self.weight-self.w_half))))

#   @classmethod
#   def update_params(cls, paramchange):
#      if paramchange[0].lower() == 'carnivore':
#
#        individual = carnivore(age=2, weight=30, seed=12345)
#
#        elif paramchange[0].lower() == 'herbivore':
#            individual = herbivore(age=2, weight=30, seed=12345)
#
#       else:
#            raise ValueError(" Unknown Species entered ")

#        for param in paramchange[1].keys():
#
#            try:
#                paramname = exec("individual.%s" % (param))
#                paramname = paramdict[param]

#            except:
#                warnings.warn(param + ' ' + 'is not a valid class parameter, and will not be updated.')

    def birth(self, n_animals):
        # Calculating the possibility and probability of birth, returning True if birth and false if not birth.

        if self.weight <= self.zeta * (self.w_birth + self.sigma_birth):
            return False

        else:
            birth_proba = min(1, self.gamma * self.fitness * (n_animals - 1))

            if rd.uniform(0, 1) <= birth_proba:
                return True

            else:
                return False

    def death(self):
        # Calculating the probability of death, also simulating if the death will occur.

        if self.weight <= 0:
            return True

        else:
            death_proba = self.omega * (1 - self.fitness)

            if rd.uniform(0,1) <= death_proba:
                return True

            else:
                return False

    def migration(self):
        # Calculating probability of migration, and deciding whether the animal will migrate or not.

        migration_proba = self.mu * self.fitness

        if rd.uniform(0,1) <= migration_proba:
            return True
        else:
            return False


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

    def __init__(self, age, weight, seed = rd.randint(0,9999999)):
        self.seed = seed
        self.weight = weight
        self.age = age

        self.fitness()

'''
    def feeding(self, F_actual):
        # Annual eating and weight loss calculated into annual weight change for the animal

        self.weight += (self.beta * F_actual) - (self.eta * self.weight)
'''


class carnivore(animal):

    def __init__(self, age, weight, seed = rd.randint(0,9999999)):
        self.seed = seed
        self.weight = weight
        self.age = age
        self.w_birth = 6
        self.sigma_birth = 1
        self.beta = 0.75
        self.eta = 0.125
        self.a_half = 40
        self.phi_age = 0.3
        self.w_half = 4
        self.phi_weight = 0.4
        self.mu = 0.4
        self.gamma = 0.8
        self.zeta = 3.5
        self.xi = 1.1
        self.omega = 0.8
        self.F = 50
        self.DeltaPhiMax = 10
        self.fitness()


'''

    def feeding(self, w_herb_tot_year):
        # Annual eating and weight loss calculated into annual weight change for the animal
        
        self.weight += self.beta * w_herb_tot_year - (self.eta * self.weight)

'''