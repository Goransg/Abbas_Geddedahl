from src.biosim.biome import *
import random as rd


class island:

    def __init__(self, map):

        """
            Number of animals per species in island, as dictionary.
            :param map: text-string consisting of letters H, L, D, W representing Highland, Lowland, Desert and Water.
            This sets the geographical map of the island.
            the map cannot have other than water cells in its outer boundary.
            """

        map_list = map.split()
        coord_map = []
        x = 0
        y = 0

        for line in map_list:

            # Making a coordinate system with nested lists through a nested for-loop.
            # The Biome class is decided by the type of cell in the map string.

            line_list = []
            y += 1
            if (y == 1 and line != 'W'*len(line)) or (y == len(map_list) and line != 'W' * len(line)):
                raise TypeError('The outline cells of the map needs to be water cells!')
            elif line[-1] != 'W' or line[0] != 'W':
                raise TypeError('The outline cells of the map needs to be water cells!')
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

    def species_count(self):
        """
            Counts the number of animal per species on the entire Island.
            :return species_amount: Integer representing the number of animals on the island.
        """

        species_amount = {
            'carnivores': 0,
            'herbivores': 0
        }
        for lst in self.coord_map:

            for x in lst:

                species_amount['carnivores'] += len(x.carn)
                species_amount['herbivores'] += len(x.herb)

        return species_amount

    def animal_count(self):
        """
            Counts the number of animal per species on the entire Island.
            :return animal_amount: a dictionary providing the count of each the two species on the island.
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
        yearly_functions = ['update_fodder', 'grazing', 'breeding', 'migration', 'aging', 'remove_population']

        for func in yearly_functions:
            if func == 'migration':
                self.migration()
            else:
                for lst in self.coord_map:

                    for x in lst:
                        exec("x.%s()" % (func))

    def migration(self):
        """
            Finds animals that are going to migrate, checks where they want to migrate, then moves them to the
            desired cell if it is habitable.
            """

        self.migrationreset()

        for y in range(len(self.coord_map)-1):

            for x in range(len(self.coord_map[y])-1):
                cur_cell = self.coord_map[x][y]
                migrators_herb = [herbivore for herbivore in cur_cell.herb if herbivore.migration()]
                migrators_carn = [carnivore for carnivore in cur_cell.carn if carnivore.migration()]

                for herbivore in migrators_herb:

                    new_x, new_y = migrationdestination(x, y)
                    new_cell = self.coord_map[new_x][new_y]

                    if new_cell.habitable:

                        new_cell.herb.append(herbivore)

                        herbivore.migrated = True

                for carnivore in migrators_carn:

                    new_x, new_y = migrationdestination(x, y)
                    new_cell = self.coord_map[new_x][new_y]

                    if new_cell.habitable:

                        new_cell.carn.append(carnivore)

                        carnivore.migrated = True

                cur_cell.herb = [herbivore for herbivore in cur_cell.herb if herbivore.migration() is False]
                cur_cell.carn = [carnivore for carnivore in cur_cell.carn if carnivore.migration() is False]

    def add_population(self, population):
        """
            Adds animals to a given cell.
            :param population: a list with a dictionary specifying the location of the animals,
            and a list of dictionaries specifying where to place the animals.
            """

        for specie in population:
            y_value = specie['loc'][0] - 1
            x_value = specie['loc'][1] - 1
            pop = specie['pop']

            self.coord_map[y_value][x_value].add_population(pop)

    def migrationreset(self):
        """
            Sets the "Migrated" flag for all animals to false, allowing them to migrate.
            """
        for row in self.coord_map:

            for cell in row:

                for carnivore in cell.carn:
                    carnivore.migrated = False

                for herbivore in cell.herb:
                    herbivore.migrated = False

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


def migrationdestination(cur_x, cur_y):
    """
         Decides where a given animal want to go to
        :param cur_x: Integer representing the x-location of the current cell of residence.
        :param cur_y: Integer representing the y-location of the current cell of residence.
        :return choice[0]: x-coordinate of the cell the animal want to go
        :return choice[1]: y-coordinate of the cell the animal want to go
        """
    choice = rd.choice([(cur_x + 1, cur_y), (cur_x - 1, cur_y), (cur_x, cur_y + 1), (cur_x, cur_y - 1)])

    return choice[0], choice[1]
