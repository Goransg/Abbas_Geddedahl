from biosim.biome import lowland, highland, desert, water
import random as rd


def test_lowland_create():
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    f_max = lowland.f_max
    cell = lowland((a, b))
    assert cell.f_max == f_max
    assert cell.habitable is True

def test_update_fodder():
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    f_max = lowland.f_max
    cell = lowland((a, b))
    cell.update_fodder()
    assert cell.fodder == f_max

def test_highland_create():
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    f_max = highland.f_max
    cell = highland((a, b))
    assert cell.f_max == f_max
    assert cell.habitable is True


def test_water_create():
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    f_max = water.f_max
    cell = water((a, b))
    assert cell.f_max == f_max
    assert cell.habitable is False


def test_desert_create():
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    f_max = desert.f_max
    cell = desert((a, b))
    assert cell.f_max == f_max
    assert cell.habitable is True


def test_add_population():
    pop_size = 20
    pop = [{'species': 'Carnivore',
            'age': 5,
            'weight': 20}
           for _ in range(pop_size)]
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    cell = desert((a, b))
    cell.add_population(pop)
    assert len(cell.carn) + len(cell.herb) == pop_size


def test_remove_population():
    pop_size = 20
    pop = [{'species': 'Carnivore',
            'age': 50,
            'weight': 5}
           for _ in range(pop_size)]
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    cell = desert((a, b))
    cell.add_population(pop)
    cell.remove_population()
    assert len(cell.carn) + len(cell.herb) < pop_size


def test_ageing():
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    low_cell = lowland((5, 5))
    pop_size = 20
    pop = [{'species': 'Carnivore',
            'age': 5,
            'weight': 20}
           for _ in range(pop_size)]
    low_cell.add_population(pop)
    age_now = low_cell.carn[0].age
    low_cell.aging()
    age_new = low_cell.carn[0].age

    assert age_new == age_now + 1

def test_grazing():
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    f_max = lowland.f_max
    low_cell = lowland((5, 5))
    pop_size = 20
    pop_herb = [{'species': 'herbivore',
            'age': 5,
            'weight': 20}
           for _ in range(pop_size)]
    pop_carn = [{'species': 'Carnivore',
            'age': 5,
            'weight': 20}
           for _ in range(pop_size)]
    low_cell.add_population(pop_carn + pop_herb)
    low_cell.grazing()
    assert low_cell.fodder < f_max


def test_migration(mocker):
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    A = lowland((a, b))
    B = lowland((a - 1, b))
    C = highland((a + 1, b))
    D = water((a, b - 1))
    E = desert((a, b + 1))
    cell_lst = [B, C, D, E]
    pop_size = 20
    pop = [{'species': 'Carnivore',
            'age': 5,
            'weight': 20}
           for _ in range(pop_size)]
    A.add_population(pop)
    mocker.patch('biosim.animals.animal.migration', return_value=True)
    A.migration(cell_lst)
    total_pop = len(A.carn) + len(A.herb) + len(B.carn) + len(B.herb) + len(C.carn) + len(C.herb) \
        + len(D.carn) + len(D.herb) + len(E.carn) + len(E.herb)
    assert total_pop == pop_size
    assert len(A.carn) + len(A.herb) < total_pop

def test_cell_procreation(mocker):
    # test no babies are born
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    A = lowland((a, b))
    pop_size = 20
    pop = [{'species': 'Carnivore',
            'age': 5,
            'weight': 20}
           for _ in range(pop_size)]
    A.add_population(pop)
    mocker.patch('biosim.animals.animal.birth', return_value=None)
    A.breeding()

    assert len(A.carn) + len(A.herb) == pop_size


def test_parameterupdate_oneinstance_post_creation():
    # Test if parameter updating affects the unintended subclass.

    testcell = highland((3, 3))
    testcell.update_params(({'f_max': 40}))
    assert testcell.f_max == 40


def test_parameterupdate_oneinstance_pre_creation():
    # Test if parameter updating affects the unintended subclass.
    testcell = lowland((5, 3))
    testcell.update_params(({'f_max': 50}))
    assert lowland.f_max == 50


def test_parameterupdate():
    # Test if parameter updating affects the unintended subclass.
    lowland.update_params(({'f_max': 90}))
    assert lowland.f_max == 90


def test_biome_parameterupdate_oneinstance_post_creation():
    # Test if parameter updating affects the unintended subclass.

    testcell = highland((3, 3))
    highland.update_params(({'f_max': 40}))
    assert testcell.f_max == 40


def test_biome_parameterupdate_oneinstance_pre_creation():
    # Test if parameter updating affects the unintended subclass.
    testcell2 = lowland((5, 3))
    lowland.update_params(({'f_max': 50}))
    assert testcell2.f_max == 50


def test_biome_parameterupdate():
    # Test if parameter updating affects the unintended subclass.
    lowland.update_params(({'f_max': 90}))
    assert lowland.f_max == 90


def test_animal_parameterupdate_intended():
    # Test if parameter updating affects the unintended subclass.
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    low_cell = lowland((5, 5))
    pop_size = 20
    pop = [{'species': 'Carnivore',
            'age': 5,
            'weight': 20}
           for _ in range(pop_size)]
    low_cell.add_population(pop)
    low_cell.change_animalparams('Herbivore', ({'mu': 0.5}))
    assert low_cell.carn[0].mu == 0.4


def test_animal_parameterupdate_unintended():
    # Test if parameter updating affects the unintended subclass.
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    low_cell = lowland((5, 5))
    pop_size = 20
    pop = [{'species': 'Herbivore',
            'age': 5,
            'weight': 20}
           for _ in range(pop_size)]
    low_cell.add_population(pop)
    low_cell.change_animalparams('Herbivore', ({'beta': 0.5}))
    assert low_cell.herb[0].beta == 0.5