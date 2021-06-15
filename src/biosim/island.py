import numpy as np
from biosim.biome import water, highland, lowland, desert


class island:
    """
    An object representing the group of cells, acting as an island.
    This sets the geographical map of the island using biome objects, seen in :class:`biome.biome`.
    the map cannot have other than water cells in its outer boundary.

    :param map: text-string consisting of letters H, L, D, W
    representing Highland, Lowland, Desert and Water.
    """

    def __init__(self, map):

        map_list = map.split()
        coord_map = []
        x = 0
        y = 0
        line_len = len(map_list[0])

        for line in map_list:

            # Making a coordinate system with nested lists through a nested for-loop.
            # The Biome class is decided by the type of cell in the map string.

            line_list = []
            y += 1
            if len(line) != line_len:
                raise ValueError('Inconsistent line length')

            if (y == 1 and line != 'W' * len(line)) or (
                    y == len(map_list) and line != 'W' * len(line)):
                raise ValueError('The outline cells of the map needs to be water cells!')
            elif line[-1] != 'W' or line[0] != 'W':
                raise ValueError('The outline cells of the map needs to be water cells!')
            else:
                for cell in line:
                    x += 1

                    if cell.upper() == 'W':
                        line_list.append(water((x, y)))

                    elif cell.upper() == 'H':
                        line_list.append(highland((x, y)))

                    elif cell.upper() == 'L':
                        line_list.append(lowland((x, y)))

                    elif cell.upper() == 'D':
                        line_list.append(desert((x, y)))

                    else:
                        raise ValueError(cell + ' ' + 'Is an unrecognized biome type')

            coord_map.append(line_list)

        self.coord_map = coord_map

    @staticmethod
    def change_landscapeparams(land, params):
        """
        Changes the constant parameters of a given animal type.
        Uses the function :func:`biome.biome.update_params`.

        :param land: a text string representing the landscape type to be updated
        :param params: a dictionary of constant names to be updated,
        with values they are going to be set to as values.
        """
        if land == 'H':
            highland.update_params(params)
        elif land == 'L':
            lowland.update_params(params)
        elif land == 'W':
            raise KeyError('Water parameter can not be changed')
        elif land == 'D':
            raise KeyError('Desert parameter can not be changed')
        else:
            raise KeyError('unknown cell type specified')

    def species_count(self):
        """
        Counts the number of animal per species on the entire Island.

        :return species_amount: Integer representing the number of animals on the island.
        """

        species_amount = {
            'Carnivore': 0,
            'Herbivore': 0
        }
        for lst in self.coord_map:

            for x in lst:
                species_amount['Carnivore'] += len(x.carn)
                species_amount['Herbivore'] += len(x.herb)

        return species_amount

    def change_animalparams(self, species, params):
        """
        Passes changes of animal parameters to the function :func:`biome.biome.change_animalparams`

        :param species: String representing the species to update parameters for
        :param params: Dictionary with parameter names and new values
        """
        self.coord_map[0][0].change_animalparams(species, params)

    def animal_count(self):
        """
        Counts the number of animal per species on the entire Island.

        :return animal_amount: a dictionary with the count of each the two species on the island.
        """

        animal_amount = 0
        for lst in self.coord_map:

            for x in lst:
                animal_amount += len(x.carn)
                animal_amount += len(x.herb)

        return animal_amount

    def sim_year(self):
        """
        Goes through a yearly simulation, and executes the yearly function in sequence.
        """
        yearly_functions = ['update_fodder', 'grazing', 'breeding',
                            'migration', 'aging', 'remove_population']

        for func in yearly_functions:
            if func == 'migration':
                self.migration()
            else:
                for lst in self.coord_map:

                    for x in lst:
                        if len(x.herb) + len(x.carn) > 0:
                            exec("x.%s()" % func)

    def migration(self):
        """
        Runs the :func:`biome.biome.migration` function for all cells on the island,
        providing the neighbouring cells for each.
        """

        for y in range(len(self.coord_map) - 1):

            for x in range(len(self.coord_map[y]) - 1):
                cur_cell = self.coord_map[y][x]
                neighbours = []
                try:
                    neighbours = [self.coord_map[y][x-1], self.coord_map[y-1][x],
                                  self.coord_map[y][x+1], self.coord_map[y+1][x]]
                except IndexError:
                    pass
                if len(neighbours) > 0:
                    cur_cell.migration(neighbours)

    def add_population(self, populations):
        """
        Adds animals to a given cell, given in coordinates starting at (1,1).
        Runs the :func:`biome.biome.add_population` function for the desired cell.

        :param populations: a list with a dictionary specifying the location of the animals,
        """

        for population in populations:
            if population['loc'][0] > 0 and population['loc'][1] > 0:
                y_value = population['loc'][0] - 1
                x_value = population['loc'][1] - 1
            else:
                raise KeyError('Please use coordinate values larger than 0!')
            pop = population['pop']

            self.coord_map[y_value][x_value].add_population(pop)

    def distrubution(self):
        """
        Counts the number of animal per species on the entire Island.

        :return herbdist: a nested list representing the amount of herbivores per cell.
        :return carndist: a nested list representing the amount of carnivores per cell.
        """

        herbdist = []
        carndist = []

        for row in self.coord_map:
            yherb = []
            ycarn = []

            for cell in row:
                yherb.append(len(cell.herb))
                ycarn.append(len(cell.carn))

            herbdist.append(yherb)
            carndist.append(ycarn)

        return herbdist, carndist

    def get_bincounts(self):
        """
        Fetches information for the histograms.

        :return 6 x 2d-arrays: representing weight, fitness and age for the animals in the cells.
        """
        herbweights = []
        carnweights = []
        herbfitness = []
        carnfitness = []
        herbage = []
        carnage = []

        for row in self.coord_map:
            for cell in row:
                if len(cell.herb) > 0:
                    herbweights.append(np.array([int(animal.weight) for animal in cell.herb],
                                                dtype=object))
                    herbfitness.append(np.array([round(animal.fitness, 1) for animal in cell.herb],
                                                dtype=object))
                    herbage.append(np.array([int(animal.age) for animal in cell.herb],
                                            dtype=object))

                if len(cell.herb) > 0:
                    carnweights.append(np.array([int(animal.weight) for animal in cell.carn],
                                                dtype=object))
                    carnfitness.append(np.array([round(animal.fitness, 1) for animal in cell.carn],
                                                dtype=object))
                    carnage.append(np.array([int(animal.age) for animal in cell.carn],
                                            dtype=object))

        return np.array(herbweights, dtype=object), np.array(carnweights, dtype=object), \
            np.array(herbfitness, dtype=object), np.array(carnfitness, dtype=object), \
            np.array(herbage, dtype=object), np.array(carnage, dtype=object)
