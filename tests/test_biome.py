import unittest
from src.biosim.biome import *
import random as rd


class biome_test(unittest.TestCase):

    def test_lowland_create(self):
        a = rd.randint(1, 50)
        b = rd.randint(1, 50)
        f_max = 800
        cell = lowland((a, b))
        self.assertEqual(cell.f_max, f_max)
        self.assertEqual(cell.habitable, True)

    def test_highland_create(self):
        a = rd.randint(1, 50)
        b = rd.randint(1, 50)
        f_max = 300
        cell = highland((a, b))
        self.assertEqual(cell.f_max, f_max)
        self.assertEqual(cell.habitable, True)

    def test_water_create(self):
        a = rd.randint(1, 50)
        b = rd.randint(1, 50)
        f_max = 0
        cell = water((a, b))
        self.assertEqual(cell.f_max, f_max)
        self.assertEqual(cell.habitable, False)

    def test_desert_create(self):
        a = rd.randint(1, 50)
        b = rd.randint(1, 50)
        f_max = 0
        cell = desert((a, b))
        self.assertEqual(cell.f_max, f_max)
        self.assertEqual(cell.habitable, True)

    def test_add_population(self):
        pop_size = 20
        pop = [{'species': 'Carnivore',
                'age': 5,
                'weight': 20}
               for _ in range(pop_size)]
        a = rd.randint(1, 50)
        b = rd.randint(1, 50)
        cell = desert((a, b))
        cell.add_population(pop)
        self.assertEqual(len(cell.carn)+len(cell.herb), pop_size)

    def test_remove_population(self):
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
        self.assertEqual(len(cell.carn) + len(cell.herb) < pop_size, True)


if __name__ == '__main__':
    unittest.main()
