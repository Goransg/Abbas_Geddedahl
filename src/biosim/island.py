from src.biosim.biome import *
import textwrap


class island:

    def __init__(self, map):
        map_list = map.split()
        coord_map = []
        x = 0
        y = 0

        for line in map_list:
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












