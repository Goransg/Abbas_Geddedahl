from src.biosim.biome import *
import textwrap


class island:

    def __init__(self, map):
        map_list = map.split()
        coord_map = []
        x = 0
        y = 0

        for line in map_list:

            # Making a coordinate system with nested lists through a nested for-loop.
            # The Biome class is decided by the type of cell in the map string.

            line_list = []
            y += 1

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
        # Counts the number of animal per species on the entire Island, and returns it as a dictionary

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
        # Counts the number of animal per species on the entire Island, and returns it as a dictionary

        animal_amount = 0
        for lst in self.coord_map:

            for x in lst:

                animal_amount += len(x.carn)
                animal_amount += len(x.herb)

        return animal_amount

    def sim_year(self):
        # Goes through a yearly simulation

        for lst in self.coord_map:

            for x in lst:
                x.update_fodder()
                x.herb_feeding()
                x.carn_feeding()
                x.procreation()
                migrators, destinations = x.migration()
                transfer(migrators, destinations)
                x.aging()
                x.death()

    def transfer(self, migrators, destinations):
        # Transfers given migrators to given destinations

        for num in range(len(migrators)):

            self.coord_map[destinations[num][0]][destinations[num][1]].append(migrators[num])

    def add_population(self, population):
        # Adds a population to a given cell

        self.coord_map[population['loc'][0]][population['loc'][1]].add_population(population['pop'])




















