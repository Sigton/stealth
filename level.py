import pygame
import platforms
import guards
import entities
import healthbar
import leveltext
import constants
import terrain
import os


class Level:

    # Sprites associated with the level

    platform_list = None
    cosmetic_list = None
    keypads = None
    bombs = None
    doors = None
    guards = None
    entities = None
    level_text = None

    player = None

    # Background image
    background = None

    def __init__(self, player):

        # Constructor

        self.platform_list = pygame.sprite.Group()
        self.cosmetic_list = pygame.sprite.Group()
        self.keypads = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.guards = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()

        self.player = player

        self.keypad_array = []
        self.door_no = 0

    def update(self):

        # Update everything in the level
        self.platform_list.update()
        self.cosmetic_list.update()
        self.keypads.update()
        self.bombs.update()
        self.guards.update()
        self.entities.update()
        self.level_text.update()

    def draw(self, display):

        # Draw everything on this level
        display.fill(constants.BLACK)
        display.blit(self.background, (0, 0))

        # Draw the sprite lists
        self.platform_list.draw(display)
        self.cosmetic_list.draw(display)
        self.keypads.draw(display)
        self.bombs.draw(display)
        self.guards.draw(display)
        self.entities.draw(display)

    def create_platform(self, tile, x, y):
        platform = platforms.Platform(tile)
        platform.rect.x = x
        platform.rect.y = y
        self.platform_list.add(platform)

    def create_cosmetic(self, tile, x, y):
        platform = platforms.Platform(tile)
        platform.rect.x = x
        platform.rect.y = y
        self.cosmetic_list.add(platform)

    def create_keypad(self, x, y):
        new_keypad = entities.Keypad()

        new_keypad.rect.x = x
        new_keypad.rect.y = y

        new_keypad.progress_bar = healthbar.ProgressBar()
        new_keypad.progress_bar.parent = new_keypad
        new_keypad.progress_bar.level = self
        self.entities.add(new_keypad.progress_bar)

        self.keypads.add(new_keypad)
        self.keypad_array.append(new_keypad)

    def create_bomb(self, x, y):
        new_bomb = entities.Bomb()

        new_bomb.rect.x = x
        new_bomb.rect.y = y

        new_bomb.progress_bar = healthbar.ProgressBar()
        new_bomb.progress_bar.parent = new_bomb
        new_bomb.progress_bar.level = self
        self.entities.add(new_bomb.progress_bar)

        self.bombs.add(new_bomb)

    def create_door(self, x, y):
        new_door = entities.Door()

        new_door.rect.x = x
        new_door.rect.y = y

        new_door.level = self
        new_door.door_no = self.door_no

        self.platform_list.add(new_door)
        self.doors.add(new_door)

    def create_guard(self, x, y):
        new_guard = guards.Guard()

        new_guard.rect.x = x
        new_guard.rect.y = y

        new_guard.level = self
        new_guard.player = self.player
        self.entities.add(new_guard.torch)

        self.guards.add(new_guard)

    def render(self, data):

        self.door_no = 0
        self.keypad_array = []

        for tile in data:
            position = tile[0]
            tile_data = tile[1]

            if 'type' not in tile_data:
                print(tile)

            if tile_data['type'] == "Entity":

                if tile_data['tile'] == 24:
                    self.create_keypad((position[0]*24)+6, (position[1]*24)+5)

                elif tile_data['tile'] == 23:
                    self.door_no += 1
                    self.create_door(position[0]*24, position[1]*24)

                elif tile_data['tile'] == 21:
                    self.create_guard(position[0]*24, (position[1]*24)-24)

                elif tile_data['tile'] == 25:
                    self.create_bomb(position[0]*24, position[1]*24)

            elif tile_data['type'] == "Solid":
                self.create_platform(platforms.platforms[tile_data['tile']-1], position[0]*24, position[1]*24)

            elif tile_data['type'] == "Cosmetic":
                self.create_cosmetic(platforms.platforms[tile_data['tile']-1], position[0]*24, position[1]*24)


class Level01(Level):

    def __init__(self, player, write_data=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level1.json")
        tile_file = os.path.join("level_data", "layouts", "level1.png")
        type_file = os.path.join("level_data", "tile_types", "level1.png")

        level = terrain.LevelData(save_file, tile_file, type_file)
        if write_data:
            level.write_data()

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)

        self.level_text = leveltext.Level01()
        self.level_text.player = self.player


class Level02(Level):

    def __init__(self, player, write_data=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level2.json")
        tile_file = os.path.join("level_data", "layouts", "level2.png")
        type_file = os.path.join("level_data", "tile_types", "level2.png")

        level = terrain.LevelData(save_file, tile_file, type_file)
        if write_data:
            level.write_data()

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)

        self.level_text = leveltext.Level02()
        self.level_text.player = self.player


class Level03(Level):

    def __init__(self, player, write_data=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level3.json")
        tile_file = os.path.join("level_data", "layouts", "level3.png")
        type_file = os.path.join("level_data", "tile_types", "level3.png")

        self.door_linkup = {0: 1,
                            1: 1,
                            2: 2,
                            3: 2,
                            4: 0,
                            5: 0}

        level = terrain.LevelData(save_file, tile_file, type_file)
        if write_data:
            level.write_data()

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        self.level_text = leveltext.Level03()
        self.level_text.player = self.player


class Level04(Level):

    def __init__(self, player, write_data=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level4.json")
        tile_file = os.path.join("level_data", "layouts", "level4.png")
        type_file = os.path.join("level_data", "tile_types", "level4.png")

        self.door_linkup = {0: 8,
                            1: 8,
                            2: 7,
                            3: 7,
                            4: 6,
                            5: 6,
                            6: 5,
                            7: 5,
                            8: 4,
                            9: 4,
                            10: 3,
                            11: 3,
                            12: 1,
                            13: 1,
                            14: 0,
                            15: 0,
                            16: 2,
                            17: 2}

        level = terrain.LevelData(save_file, tile_file, type_file)
        if write_data:
            level.write_data()

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        self.level_text = leveltext.Level04()
        self.level_text.player = self.player


class Level05(Level):

    def __init__(self, player, write_data=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level5.json")
        tile_file = os.path.join("level_data", "layouts", "level5.png")
        type_file = os.path.join("level_data", "tile_types", "level5.png")

        self.door_linkup = {0: 0,
                            1: 0,
                            2: 1,
                            3: 1}

        level = terrain.LevelData(save_file, tile_file, type_file)
        if write_data:
            level.write_data()

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        self.level_text = leveltext.Level05()
        self.level_text.player = self.player


class Level06(Level):

    def __init__(self, player, write_data=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level6.json")
        tile_file = os.path.join("level_data", "layouts", "level6.png")
        type_file = os.path.join("level_data", "tile_types", "level6.png")

        self.door_linkup = {0: 0,
                            1: 0,
                            2: 1,
                            3: 1}

        level = terrain.LevelData(save_file, tile_file, type_file)
        if write_data:
            level.write_data()

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        self.level_text = leveltext.Level06()
        self.level_text.player = self.player


class Level07(Level):

    def __init__(self, player, write_data=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level7.json")
        tile_file = os.path.join("level_data", "layouts", "level7.png")
        type_file = os.path.join("level_data", "tile_types", "level7.png")

        level = terrain.LevelData(save_file, tile_file, type_file)
        if write_data:
            level.write_data()

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)

        self.level_text = leveltext.Level07()
        self.level_text.player = self.player


class Level08(Level):

    def __init__(self, player, write_data=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level8.json")
        tile_file = os.path.join("level_data", "layouts", "level8.png")
        type_file = os.path.join("level_data", "tile_types", "level8.png")

        self.door_linkup = {0: 0,
                            1: 0,
                            2: 1,
                            3: 1}

        level = terrain.LevelData(save_file, tile_file, type_file)
        if write_data:
            level.write_data()

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        self.level_text = leveltext.Level08()
        self.level_text.player = self.player


class Level09(Level):

    def __init__(self, player, write_data=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level9.json")
        tile_file = os.path.join("level_data", "layouts", "level9.png")
        type_file = os.path.join("level_data", "tile_types", "level9.png")

        self.door_linkup = {0: 0,
                            1: 0,
                            2: 2,
                            3: 2,
                            4: 1,
                            5: 1}

        level = terrain.LevelData(save_file, tile_file, type_file)
        if write_data:
            level.write_data()

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        self.level_text = leveltext.Level09()
        self.level_text.player = self.player


class Level10(Level):

    def __init__(self, player, write_data=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level10.json")
        tile_file = os.path.join("level_data", "layouts", "level10.png")
        type_file = os.path.join("level_data", "tile_types", "level10.png")

        self.door_linkup = {0: 3,
                            1: 3,
                            2: 3,
                            3: 4,
                            4: 4,
                            5: 4,
                            6: 0,
                            7: 0,
                            8: 0,
                            9: 1,
                            10: 1,
                            11: 1,
                            12: 2,
                            13: 2,
                            14: 2}

        level = terrain.LevelData(save_file, tile_file, type_file)
        if write_data:
            level.write_data()

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        self.level_text = leveltext.Level10()
        self.level_text.player = self.player


class Level11(Level):

    def __init__(self, player, write_data=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level11.json")
        tile_file = os.path.join("level_data", "layouts", "level11.png")
        type_file = os.path.join("level_data", "tile_types", "level11.png")

        level = terrain.LevelData(save_file, tile_file, type_file)
        if write_data:
            level.write_data()

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)

        self.level_text = leveltext.Level11()
        self.level_text.player = self.player
