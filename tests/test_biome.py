from biosim.biome import lowland, highland, desert, water
import random as rd


def test_lowland_create():
    a = rd.randint(1, 50)
    b = rd.randint(1, 50)
    f_max = lowland.f_max
    cell = lowland((a, b))
    assert cell.f_max == f_max
    assert cell.habitable is True


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
    mocker.patch('biosim.biome.animal.migration', return_value=True)
    A.migration(cell_lst)
    total_pop = len(A.carn) + len(A.herb) + len(B.carn) + len(B.herb) + len(C.carn) + len(C.herb) \
        + len(D.carn) + len(D.herb) + len(E.carn) + len(E.herb)
    assert total_pop == pop_size
    assert len(A.carn) + len(A.herb) < total_pop


def test_parameterupdate_oneinstance_post_creation():
    # Test if parameter updating affects the unintended subclass.

    testcell = highland((3, 3))
    testcell.update_params(({'f_max': 40}))
    assert testcell.f_max == 40


def test_parameterupdate_oneinstance_pre_creation():
    # Test if parameter updating affects the unintended subclass.
    testcell = lowland((5, 3))
    testcell.update_params(({'f_max': 50}))
    assert testcell.f_max == 50


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
