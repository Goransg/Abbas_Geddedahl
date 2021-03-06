# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from src.biosim.biosim import BioSim

"""
Compatibility check for BioSim simulations.

This script shall function with biosim packages written for
the INF200 project June 2021.
"""

__author__ = "Hans Ekkehard Plesser, NMBU"
__email__ = "hans.ekkehard.plesser@nmbu.no"


if __name__ == '__main__':

    # geogr = """\
    #            WWWWWWWWWWWWWWWWWWWWW
    #            WWWWWWWWHWWWWLLLLLLLW
    #            WHHHHHLLLLWWLLLLLLLWW
    #            WHHHHHHHHHWWLLLLLLWWW
    #            WHHHHHLLLLLLLLLLLLWWW
    #            WHHHHHLLLDDLLLHLLLWWW
    #            WHHLLLLLDDDLLLHHHHWWW
    #            WWHHHHLLLDDLLLHWWWWWW
    #            WHHHLLLLLDDLLLLLLLWWW
    #            WHHHHLLLLDDLLLLWWWWWW
    #            WWHHHHLLLLLLLLWWWWWWW
    #            WWWHHHHLLLLLLLWWWWWWW
    #            WWWWWWWWWWWWWWWWWWWWW"""
    geogr = """WWWWWWWWWWWWWWWWWWWWW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHLLLLWWLLLLLLLWW
               WWHHLLLLLLLWWLLLLLLLW
               WWHHLLLLLLLWWLLLLLLLW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDWWLLLLLWWW
               WHHHHDDDDDDLLLLWWWWWW
               WWHHHHDDDDDDLWWWWWWWW
               WWHHHHDDDDDLLLWWWWWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHDDDDDDLLLLWWWWWW
               WWHHHHDDDDDLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWHHHHHHWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]

    sim = BioSim(island_map="WWWW\nWLHW\nWWWW",
                ini_pop=[],
                seed=1,
                vis_years=10, img_years=20)


    sim.simulate(num_years=2)
    print(sim.year)
    #sim.add_population(population=ini_carns)
    sim.simulate(num_years=3)
    print(sim.year)