from src.biosim import island
from src.biosim import biome
import random as rd

def test_migration():
    rd.seed(a=16577)
    geo = island.island('''
    LLL
    LLW
    LLL''')

    geo.coord_map[1][1].add_population([{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)])
    geo.migration()

    assert len(geo.coord_map[1][1].herb) < 50
    assert (len(geo.coord_map[2][1].herb) + len(geo.coord_map[0][1].herb) + len(geo.coord_map[1][0].herb) + len(geo.coord_map[1][1].herb)) == 50
    assert len(geo.coord_map[1][2].herb) == 0