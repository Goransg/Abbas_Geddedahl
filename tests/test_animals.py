from src.biosim import animals
import random as rd
import math as m

def test_creation_herb():
    # Testing if the weight and age of the individual are correct.

    weight = rd.randint(0,50)
    age = rd.randint(0,20)
    fitness = (1/(1+m.e**(0.6*(age-40))) * (1/(1+m.e**(-0.1*(weight-10)))))
    individual_herb = animals.herbivore(weight=weight, age=age)
    assert individual_herb.weight == weight
    assert individual_herb.age == age
    assert individual_herb.fitness == fitness

def test_creation_carn():
    # Testing if the weight and age of the individual are correct.

    weight = rd.randint(0,50)
    age = rd.randint(0,20)
    fitness = (1/(1+m.e**(0.3*(age-40))) * (1/(1+m.e**(-0.4*(weight-4)))))
    individual_carn = animals.carnivore(weight=weight, age=age)
    assert individual_carn.weight == weight
    assert individual_carn.age == age
    assert individual_carn.fitness == fitness

def test_death_bad_fitness():
    # Testing if an animal will die if the fitness is poor

    weight = 0
    age = 100
    individual = animals.carnivore(weight=weight, age=age)
    assert individual.death() is True


def test_death_good_fitness():
    # Testing if an animal will not die if the fitness is good

    weight = 50
    age = 2
    individual = animals.carnivore(weight=weight, age=age)
    assert individual.death() is False

def test_birth_bad_recreation(mocker):
    # Testing if an animal will recreate if the fitness is poor

    weight = 0
    age = 100
    individual = animals.carnivore(weight=weight, age=age)
    mocker.patch('src.biosim.animals.animal.migration', return_value=None)
    assert individual.birth(n_animals=0) is None

def test_birth_good_recreation():
    # Testing if an animal will recreate if the fitness is good

    weight = 100
    age = 5
    individual = animals.carnivore(weight=weight, age=age)
    assert individual.birth(n_animals=500) is not None

def test_migration_bad_fitness(mocker):
    # Testing if an animal will migrate if the fitness is poor

    weight = 0
    age = 100
    individual = animals.carnivore(weight=weight, age=age)
    mocker.patch('src.biosim.animals.animal.migration', return_value=False)
    assert individual.migration() is False

def test_migration_good_fitness(mocker):
    # Testing if an animal will migrate if the fitness is good

    weight = 500
    age = 2
    individual = animals.carnivore(weight=weight, age=age)
    mocker.patch('src.biosim.animals.animal.migration', return_value=True)
    assert individual.migration() is True

def test_aging():
    # Testing the aging and yearly weight decrease function

    weight = 50
    age = 2
    yearly_weightloss = 50 * 0.05
    individual = animals.herbivore(weight=weight, age=age)
    individual.aging()
    assert individual.age == 3
    assert individual.weight == (50 - yearly_weightloss)

def test_feeding_herbivore():
    # Testing the feeding function for herbivores

    weight = 50
    age = 2
    yearly_weightgain = 10 * 0.9
    individual = animals.herbivore(weight=weight, age=age)
    left = individual.feeding(2000)
    assert individual.weight == (50 + yearly_weightgain)
    assert left == 1990


def test_feeding_carnivore():
    # Testing the feeding function for carnivores

    weight = 50
    age = 2
    yearly_weightgain = 10 * 0.75
    individual = animals.carnivore(weight=weight, age=age)
    individual.DeltaPhiMax = 1
    left = individual.feeding([animals.herbivore(weight=10, age=300), animals.herbivore(weight=60, age=1)])
    assert len(left) == 1
    assert individual.weight == (weight + yearly_weightgain)



def test_parameterupdate_oneinstance():
     # Test if parameter updating affects the unintended subclass.
    weight = 50
    age = 2
    individual2 = animals.carnivore(age=age, weight=weight)
    individual2.update_params(({'beta': 0.5}))
    assert individual2.beta == 0.5







