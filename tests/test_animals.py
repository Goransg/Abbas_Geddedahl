import math as m
import random as rd

from scipy import stats

from biosim.animals import herbivore, carnivore


def test_creation_herb():
    # Testing if the weight and age of the individual are correct.
    weight = rd.randint(0, 50)
    age = rd.randint(0, 20)
    fitness = (1 / (1 + m.e ** (0.6 * (age - 40))) * (1 / (1 + m.e ** (-0.1 * (weight - 10)))))
    individual_herb = herbivore(weight=weight, age=age)
    assert individual_herb.weight == weight
    assert individual_herb.age == age
    assert individual_herb.fitness == fitness


def test_creation_carn():
    # Testing if the weight and age of the individual are correct.
    weight = rd.randint(0, 50)
    age = rd.randint(0, 20)
    fitness = (1 / (1 + m.e ** (0.3 * (age - 40))) * (1 / (1 + m.e ** (-0.4 * (weight - 4)))))
    individual_carn = carnivore(weight=weight, age=age)
    assert individual_carn.weight == weight
    assert individual_carn.age == age
    assert individual_carn.fitness == fitness


def test_death_bad_fitness():
    # Testing if an animal will die if the fitness is poor
    weight = 0
    age = 100
    individual = carnivore(weight=weight, age=age)
    assert individual.death() is True


def test_death_good_fitness():
    # Testing if an animal will not die if the fitness is good
    weight = 50
    age = 2
    individual = carnivore(weight=weight, age=age)
    assert individual.death() is False


def test_birth_bad_recreation(mocker):
    # Testing if an animal will recreate if the fitness is poor
    weight = 0
    age = 100
    individual = carnivore(weight=weight, age=age)
    mocker.patch('biosim.animals.animal.migration', return_value=None)
    assert individual.birth(n_animals=0) is None


def test_birth_good_recreation():
    # Testing if an animal will recreate if the fitness is good
    weight = 100
    age = 5
    individual = carnivore(weight=weight, age=age)
    assert individual.birth(n_animals=500) is not None


def test_migration_bad_fitness(mocker):
    # Testing if an animal will migrate if the fitness is poor
    weight = 0
    age = 100
    individual = carnivore(weight=weight, age=age)
    mocker.patch('biosim.animals.animal.migration', return_value=False)
    assert individual.migration() is False


def test_migration_good_fitness(mocker):
    # Testing if an animal will migrate if the fitness is good
    weight = 500
    age = 2
    individual = carnivore(weight=weight, age=age)
    mocker.patch('biosim.animals.animal.migration', return_value=True)
    assert individual.migration() is True


def test_aging():
    # Testing the aging and yearly weight decrease function
    weight = 50
    age = 2
    individual = herbivore(weight=weight, age=age)
    individual.aging()
    assert individual.age == 3
    assert individual.weight == (50 - 50 * individual.eta)


def test_feeding_herbivore():
    # Testing the feeding function for herbivores
    weight = 50
    age = 2
    yearly_weightgain = 10 * herbivore.beta
    individual = herbivore(weight=weight, age=age)
    left = individual.feeding(2000)
    assert individual.weight == (50 + yearly_weightgain)
    assert left == 1990


def test_feeding_carnivore():
    # Testing the feeding function for carnivores
    weight = 50
    age = 2
    individual = carnivore(weight=weight, age=age)
    individual.DeltaPhiMax = 1
    left = individual.feeding([herbivore(weight=10, age=300), herbivore(weight=100, age=1)])
    assert len(left) == 1
    assert individual.weight == (weight + 10 * individual.beta)


def test_parameterupdate_oneinstance_post_creation():
    # Test if parameter updating affects the unintended subclass.
    weight = 50
    age = 2
    individual2 = carnivore(age=age, weight=weight)
    individual2.update_params(({'beta': 0.5}))
    assert individual2.beta == 0.5


def test_parameterupdate_oneinstance_pre_creation():
    # Test if parameter updating affects the unintended subclass.
    weight = 50
    age = 2
    herbivore.update_params(({'eta': 0.7}))
    individual = herbivore(age=age, weight=weight)
    assert individual.eta == 0.7


def test_parameterupdate():
    # Test if parameter updating affects the unintended subclass.
    herbivore.update_params(({'mu': 0.3}))
    assert herbivore.mu == 0.3


def test_stat_death():
    # Statistical test for probability of death,
    # checking that the probabilty of hypothesis correctness is more than 5%
    test_animals = [carnivore(age=2, weight=50) for _ in range(50)]
    p = test_animals[0].omega * (1 - test_animals[0].fitness)
    successes = [subject for subject in test_animals if subject.death() is True]
    p_hyp = stats.binom_test(len(successes), n=len(test_animals), p=p)
    assert p_hyp >= 0.05


def test_stat_birth():
    # Statistical test for probability of birth,
    # checking if probabilty of hypothesis correctness is more than 5%
    test_animals = [carnivore(age=5, weight=20) for _ in range(50)]
    p = min(1, test_animals[0].gamma * test_animals[0].fitness * 49)
    all_res = [subject for subject in test_animals]
    successes = [i for i in all_res if i]
    p_hyp = stats.binom_test(len(successes), n=len(test_animals), p=p)
    assert p_hyp >= 0.05


def test_stat_migr():
    # Statistical test for probability of migration,
    # checking if probabilty of hypothesis correctness is more than 5%
    test_animals = [carnivore(age=5, weight=30) for _ in range(50)]
    p = test_animals[0].mu * test_animals[0].fitness
    successes = [subject for subject in test_animals if subject.migration() is True]
    p_hyp = stats.binom_test(len(successes), n=len(test_animals), p=p)
    assert p_hyp >= 0.05


def test_stat_prey():
    # Statistical test for probability of preying,
    # checking if probabilty of hypothesis correctness is more than 5%
    test_carnivore = carnivore(age=3, weight=30)
    test_herbivores = [herbivore(age=10, weight=10) for _ in range(50)]
    p = (test_carnivore.fitness - test_herbivores[0].fitness) / test_carnivore.DeltaPhiMax
    survivors = test_carnivore.feeding(test_herbivores)
    p_hyp = stats.binom_test(len(survivors), n=50, p=(1 - p))
    assert p_hyp >= 0.05
