The BioSim module
==========================


.. automodule:: biosim.biosim
  :members:

Coding examples
------------------
.. code-block:: python
   :caption: This is an example of a map for creation of an object in the BioSim class.
   :name: Example map

   island_map = """\
                  WWW
                  WHW
                  WWW"""

.. code-block:: python
   :caption: This is an example of an initial population in a cell in the island for creation of an object in the BioSim class.
   :name: Example population

       ini_herbs = [{'loc': (2, 7),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(200)]}]

.. code-block:: python
   :caption: This is an example of histogram specifications for creation of an object in the BioSim class.
   :name: Example histogram specs

       hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}}
.. code-block:: python
   :caption: This is an example of histogram specifications for creation of an object in the BioSim class. If image directory is provided, the standard value for image name and format is 'dv' and .png.

       sim = BioSim(island_map, ini_herbs, seed=1, vis_years=1,
                    hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                                'age': {'max': 60.0, 'delta': 2},
                                'weight': {'max': 60, 'delta': 2}},
                                img_dir='results3', img_base='sample',
                                img_years=1, log_file='res.txt')

.. code-block:: python
   :caption: Example of adding population after a certain time in the simulation. Here, the simulation is first ran for 100 years with the initial setup. After 100 years, a new population of animals is added to a given location, and the simulation continue for another 100 years. Movie is made from the images at last, in mp4 format. If blank, the standard value is mp4. gif can also be used.
   :name: Example simulation with added population

      sim.simulate(num_years=100)
       new_carns = [{'loc': (2, 7),
                     'pop': [{'species': 'Carnivore',
                              'age': 5,
                              'weight': 20}
                             for _ in range(50)]}]
       sim.add_population(population=new_carns)
       sim.simulate(num_years=100)
       sim.make_movie('mp4')
