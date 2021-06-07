from src.biosim import animals
import random as rd
import math as m

def test_creation_herb():
    # Testing if the weight and age of the individual are correct.

    weight = rd.randint(0,50)
    age = rd.randint(0,20)
    fitness = (1/(1+m.e**(0.6*(age-40))) * (1/(1+m.e**(-0.1*(weight-10)))))
    individual_herb = animals.herbivore(weight=weight, age=age, seed=12345)
    assert individual_herb.weight == weight
    assert individual_herb.age == age
    assert individual_herb.fitness == fitness

def test_creation_carn():
    # Testing if the weight and age of the individual are correct.

    weight = rd.randint(0,50)
    age = rd.randint(0,20)
    fitness = (1/(1+m.e**(0.3*(age-40))) * (1/(1+m.e**(-0.4*(weight-4)))))
    individual_carn = animals.carnivore(weight=weight, age=age, seed=45678)
    assert individual_carn.weight == weight
    assert individual_carn.age == age
    assert individual_carn.fitness == fitness

def test_death_bad_fitness():
    weight = 0
    age = 100
    individual = animals.carnivore(weight=weight, age=age, seed=245362)
    assert individual.death() is True


def test_death_good_fitness():
    weight = 50
    age = 2
    individual = animals.carnivore(weight=weight, age=age, seed=245362)
    assert individual.death() is False

def test_birth_bad_recreation():
    weight = 0
    age = 100
    individual = animals.carnivore(weight=weight, age=age, seed=45362)
    assert individual.birth(n_animals=0) is False

def test_birth_good_recreation():
    weight = 100
    age = 5
    individual = animals.carnivore(weight=weight, age=age, seed=86245)
    assert individual.birth(n_animals=500) is True

def test_migration_bad_fitness():
    weight = 0
    age = 100
    individual = animals.carnivore(weight=weight, age=age, seed=245362)
    assert individual.migration() is False

def test_migration_good_fitness():
    weight = 50
    age = 2
    individual = animals.carnivore(weight=weight, age=age, seed=7)
    assert individual.migration() is True

<<<<<<< HEAD
=======
def test_aging():
    weight = 50
    age = 2
    yearly_weightloss = 50 * 0.05
    individual = animals.herbivore(weight=weight, age=age, seed=245362)
    individual.aging()
    assert individual.age == 3
    assert individual.weight == (50 - yearly_weightloss)

def test_feeding():
    weight = 50
    age = 2
    yearly_weightgain = 10 * 0.9
    individual = animals.herbivore(weight=weight, age=age, seed=245362)
    left = individual.feeding(2000)
    assert individual.weight == (50 + yearly_weightgain)
    assert left == 1990

>>>>>>> branch_animal01

def test_parameterupdate_oneinstance():
     # Test if parameter updating affects the unintended subclass.
    weight = 50
    age = 2
    individual2 = animals.carnivore(age=age, weight=weight, seed=245362)
    individual2.update_params(('carnivore', {'beta': 0.5}))
    assert individual2.beta == 0.5







