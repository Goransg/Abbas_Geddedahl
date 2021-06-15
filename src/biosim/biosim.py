# -*- coding: utf-8 -*-
import logging
from biosim.island import island
from biosim.visualization import Graphics
import random as rd


class BioSim:
    """
    :param island_map: Multi-line string specifying island geography
    :param ini_pop: List of dictionaries specifying initial population
    :param seed: Integer used as random number seed
    :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
    :param cmax_animals: Dict specifying color-code limits for animal densities
    :param hist_specs: Specifications for histograms, see below
    :param vis_years: years between visualization updates (if 0, disable graphics)
    :param img_dir: String with path to directory for figures
    :param img_base: String with beginning of file name for figures
    :param img_fmt: String with file type for figures, e.g. 'png'
    :param img_years: years between visualizations saved to files (default: vis_years)
    :param log_file: If given, write animal counts to this file
    If ymax_animals is None, the y-axis limit should be adjusted automatically.
    If cmax_animals is None, sensible, fixed default values should be used.
    cmax_animals is a dict mapping species names to numbers, e.g.,
    {'Herbivore': 50, 'Carnivore': 20}
    hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
    For each property, a dictionary providing the maximum value and the bin width must be
    given, e.g.,
    {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
    Permitted properties are 'weight', 'age', 'fitness'.
    If img_dir is None, no figures are written to file. Filenames are formed as
    f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'
    where img_number are consecutive image numbers starting from 0.
    img_dir and img_base must either be both None or both strings.
    Initial population is initialized through the :func:`island.island.add_population` function.
    The geographical map is made into a :class:`island.island` class object.
    Visualization is initializes as a :class:`visualization.Graphics` object.
    Logging is initialized.
    """

    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.vis_years = vis_years
        self.img_dir = img_dir
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.img_years = img_years if img_years is not None else vis_years
        self.log_file = log_file
        self.hist_specs = hist_specs
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = seed
        self.island = island(island_map)
        self.add_population(self.ini_pop)
        rd.seed(a=self.seed)
        self.cur_year = 0
        self.graphs = Graphics(self.hist_specs, self.img_dir, self.img_base, self.img_fmt)
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='[%(levelname)s]%(module)s.%(funcName)s - '
                                   '%(asctime)s - %(message)s',
                            filemode='w')

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species,
        passing the information down to the :func:`island.island.change_animalparams`

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species.lower() not in ['herbivore', 'carnivore']:
            raise ValueError('Invalid specie')
        else:
            self.island.change_animalparams(species, params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.
        Passes the information down to the `island.island.change_landscapeparams` function.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape not in ['H', 'L', 'D', 'W']:
            raise ValueError('Invalid landscape')
        else:
            self.island.change_landscapeparams(landscape, params)

    def simulate(self, num_years):
        """
        Running simulation while visualizing the result.
        Function :func:`island.island.sim_year` is ran each year.
        Function :func:`visualization.Graphics.setup` is ran upon beginning.
        Function :func:`visualization.Graphics.update` is ran each year,
        with data from several functions from
        the :class:`island.island` object.

        :param num_years: number of years to simulate
        """

        if num_years != 0:
            self.graphs.setup(self.cur_year + num_years, self.img_years, self.island_map)
            for year in range(self.cur_year, self.cur_year + num_years):
                self.cur_year += 1
                if self.log_file is not None:
                    logg_string = dict(Year=self.year, Total_Animals=self.island.animal_count(),
                                       Animal_per_specie=self.island.species_count())
                    logging.info(logg_string)
                self.island.sim_year()
                if self.vis_years != 0:
                    if year % self.vis_years == 0:
                        herb, carn = self.island.distrubution()
                        all_animals = self.island.animal_count()
                        n_herbivores = self.island.species_count()['Herbivore']
                        n_carnivores = self.island.species_count()['Carnivore']
                        w_herbivores, w_carnivores, f_herbivores, \
                        f_carnivores, a_herbivores, a_carnivores = self.island.get_bincounts()
                        self.graphs.update(year, herb, carn, all_animals, n_herbivores,
                                           n_carnivores, w_herbivores, w_carnivores, f_herbivores,
                                           f_carnivores, a_herbivores, a_carnivores)
        else:
            raise ValueError('Invalid simulation years')

    def add_population(self, population):
        """
        Add a population to a given locations on the island.
        Runs the :func:`island.island.add_population` function.

        :param population: List of dictionaries specifying population
        """

        self.island.add_population(population)

    @property
    def year(self):
        """
        Last year simulated.

        :return self.cur_year: Integer indicating the last year being simulated in the simulation.
        """
        return self.cur_year

    @property
    def num_animals(self):
        """
        Total number of animals on island.
        Runs the :func:`island.island.animal_count` function.

        :return animals_on_island: Integer representing the number of animals on the island.
        """

        animals_on_island = self.island.animal_count()

        return animals_on_island

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.
        Runs the :func:`island.island.species_count` function.

        :return island.species_count: dictionary with species as key and
        integers representing species counts as values.
        """

        return self.island.species_count()

    def make_movie(self, movie_format):
        """
        Create MPEG4 movie from visualization images saved.
        Runs the :func:`visualization.Graphics.make_movie` function.

        :param movie_format: String indicating the desired format of the movie.
        """

        self.graphs.make_movie(movie_format)
