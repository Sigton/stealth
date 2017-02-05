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

    # How far the level has scrolled
    world_shift_x = 0
    world_shift_y = 0
    at_edge_x = False
    at_edge_y = False

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

    def shift_world(self, shift_x, shift_y):

        # Scroll the level left/right
        self.world_shift_x += shift_x

        self.at_edge_x = False
        # Set boundaries
        if self.world_shift_x >= 0:
            self.at_edge_x = True
            self.world_shift_x = 0

        elif self.world_shift_x <= -960:
            self.at_edge_x = True
            self.world_shift_x = -960

        if not self.at_edge_x:
            # Move everything in the level
            for platform in self.platform_list:
                platform.rect.x += shift_x
            for cosmetic in self.cosmetic_list:
                cosmetic.rect.x += shift_x
            for keypad in self.keypads:
                keypad.rect.x += shift_x
            for door in self.doors:
                door.rect.x += shift_x
            for bomb in self.bombs:
                bomb.rect.x += shift_x
            for guard in self.guards:
                guard.rect.x += shift_x
            for entity in self.entities:
                entity.rect.x += shift_x

        self.world_shift_y += shift_y

        self.at_edge_y = False
        if self.world_shift_y <= 0:
            self.at_edge_y = True
            self.world_shift_y = 0

        elif self.world_shift_y >= 720:
            self.at_edge_y = True
            self.world_shift_y = 720

        if not self.at_edge_y:
            # Move everything in the level
            for platform in self.platform_list:
                platform.rect.y -= shift_y
            for cosmetic in self.cosmetic_list:
                cosmetic.rect.y -= shift_y
            for keypad in self.keypads:
                keypad.rect.y -= shift_y
            for door in self.doors:
                door.rect.y -= shift_y
            for bomb in self.bombs:
                bomb.rect.y -= shift_y
            for guard in self.guards:
                guard.rect.y -= shift_y
            for entity in self.entities:
                entity.rect.y -= shift_y

    def reset_world(self):

        # Moves platforms back to their original position
        for platform in self.platform_list:
            platform.rect.x -= self.world_shift_x
            platform.rect.y -= self.world_shift_y

        for cosmetic in self.cosmetic_list:
            cosmetic.rect.x -= self.world_shift_x
            cosmetic.rect.y -= self.world_shift_y

        for keypad in self.keypads:
            keypad.rect.x -= self.world_shift_x
            keypad.rect.y -= self.world_shift_y

        for door in self.doors:
            door.rect.x -= self.world_shift_x
            door.rect.y -= self.world_shift_y

        for bomb in self.bombs:
            bomb.rect.x -= self.world_shift_x
            bomb.rect.y -= self.world_shift_y

        for guard in self.guards:
            guard.rect.x -= self.world_shift_x
            guard.rect.y -= self.world_shift_y

        for entity in self.entities:
            entity.rect.x -= self.world_shift_x
            entity.rect.y -= self.world_shift_y

        self.world_shift_x = 0
        self.world_shift_y = 0

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

    def create_hguard(self, x, y):
        new_hguard = guards.HostileGuard()

        new_hguard.rect.x = x
        new_hguard.rect.y = y

        new_hguard.level = self
        new_hguard.player = self.player
        self.entities.add(new_hguard.arm)

        self.guards.add(new_hguard)

    def render(self, data):

        self.door_no = 0
        self.keypad_array = []

        for tile in data:
            position = tile[0]
            tile_data = tile[1]

            if 'type' not in tile_data:
                print(tile)

            if tile_data['type'] == "Entity":

                if tile_data['tile'] == 28:
                    self.create_keypad((position[0]*24)+6, (position[1]*24)+5)

                elif tile_data['tile'] == 27:
                    self.door_no += 1
                    self.create_door(position[0]*24, position[1]*24)

                elif tile_data['tile'] == 25:
                    self.create_guard(position[0]*24, (position[1]*24)-24)

                elif tile_data['tile'] == 29:
                    self.create_bomb(position[0]*24, position[1]*24)

                elif tile_data['tile'] == 31:
                    self.create_hguard(position[0]*24, (position[1]*24)-24)

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

        # Set start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to start position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)
