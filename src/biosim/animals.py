import math as m

class animal(object):


    def __init__(self, species, weight, age):
        self.species = species
        self.weight = weight
        self.age = age

    def fitness(self, weight, age):
        if weight <= 0:
            self.fitness = 0
        else:
            self.fitness = (1/(1+m.e**(phi_age*(a-a_half)))) * (1/(1+m.e**(-phi_weight*(w-w_half))))

    def birth(self):
        # rd.random normal distribution W_birth, and standard deviation

    def migration(self):

    def death(self):




class herbivore(animal):
    def __init__(self, age, weight):
        self.w_birth = 8
        self.sigma_birth = 1.5
        self.beta = 0.9
        self.eta = 0.05
        self.a_half = 40
        self.phi_age = 0.6
        self.w_half = 10
        self.mu = 0.25
        self.gamma = 0.2
        self.zeta = 3.5
        self.xi = 1.2
        self.omega = 0.4
        self.F = 10

    def feeding(self, F_actual):
        weight +=





class carnivore(animal):
    def __init__(self, age, weight):
        self.w_birth = 6
        self.sigma_birth = 1
        self.beta = 0.75
        self.eta = 0.125
        self.a_half = 40
        self.phi_age = 0.3
        self.w_half = 4
        self.mu = 0.4
        self.gamma = 0.8
        self.zeta = 3.5
        self.xi = 1.1
        self.omega = 0.8
        self.F = 50
        self.DeltaPhiMax = 10

        def feeding(self):