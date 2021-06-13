#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Full island simulation with herbivores and carnivores.
"""

__author__ = 'Hans Ekkehard Plesser, NMBU'

import textwrap
from src.biosim.biosim import BioSim
import win32api,win32process,win32con
pid = win32api.GetCurrentProcessId()
handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)

if __name__ == '__main__':
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

    ini_herbs = [{'loc': (2, 7),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(200)]}]
    ini_carns = [{'loc': (2, 7),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]

    sim = BioSim(geogr, ini_herbs + ini_carns, seed=1, vis_years=1,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 img_dir='results',
                 img_base='sample')
    sim.simulate(400)
    sim.make_movie()

    input('Press ENTER')
