import pygame
import json
import os


class LevelData:

    # Writes/loads data to json files

    save_file = None
    load_dir1 = None
    load_dir2 = None

    tile_colors = [0, 986895, 2039583, 3092271, 4144959,
                   5197647, 6250335, 7303023, 8355711,
                   9408399, 10461087, 11513775, 12566463,
                   13619151, 14671839, 15724527, 16488,
                   38143, 13429247, 10081535, 16776960,
                   11776768, 65320, 2672680, 60159, 24027,
                   16793, 11110, 460551, 16173544, 7987,
                   12517631, 16711680, 5635840, 255, 16727808,
                   6502, 6691072]
    type_colors = [0, 986895, 2039583, 3092271]

    def __init__(self, savefile, loadfile1, loadfile2, level):

        # Constructor

        self.save_file = savefile

        self.load_dir1 = os.listdir(loadfile1)
        self.load_dir2 = os.listdir(loadfile2)

        self.load_files1 = []
        self.load_files2 = []

        for file in self.load_dir1:
            image = pygame.image.load(os.path.join("level_data", "layouts", level, file))
            self.load_files1 += [image]

        for file in self.load_dir1:
            image = pygame.image.load(os.path.join("level_data", "tile_types", level, file))
            self.load_files2 += [image]

        self.level_data = []

    def load_data(self):

        # Loads data from the json file

        with open(self.save_file, 'r') as infile:
            data = json.load(infile)

        return data

    def write_data(self):

        # Writes data to the json file

        block_types = (
            "Solid",
            "Cosmetic",
            "Entity",
            "Obstacle"
        )

        self.level_data = []

        z = 0
        for file in self.load_files1:

            pixel_array = pygame.PixelArray(file)
            pixel_array2 = pygame.PixelArray(self.load_files2[z])

            x = 0
            for column in pixel_array:
                y = 0
                for pixel in column:

                    new_tile = []
                    tile_data = {}

                    new_tile.append((x, y))

                    if pixel in self.tile_colors:
                        n = 0
                        for color in self.tile_colors:
                            n += 1
                            if pixel == color:
                                tile_data['tile'] = n

                        if pixel_array2[x][y] in self.type_colors:
                            n = 0

                            for color in self.type_colors:

                                if pixel_array2[x][y] == color:
                                    tile_data['type'] = block_types[n]
                                    break
                                n += 1
                    else:
                        tile_data['tile'] = 0
                        tile_data['type'] = None

                    new_tile.append(tile_data)
                    self.level_data.append(new_tile)
                    y += 1
                x += 1
            z += 1

        with open(self.save_file, "w") as outfile:
            json.dump(self.level_data, outfile)
