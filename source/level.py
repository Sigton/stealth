import pygame

import platforms
import guards
import entities
import progressbar
import guard_parts
import text
import constants
import terrain
import os


class Level:

    # Sprites associated with the level
    # Each of these gets assigned a Group instance
    # To hold a different type of sprite
    platform_list = None
    cosmetic_list = None
    obstacle_list = None
    keypads = None
    bombs = None
    doors = None
    guards = None
    entities = None
    level_text = None
    ladders = None
    lasers = None
    non_draw = None
    sky = None

    # Reference to the player
    player = None

    # Background image
    background = None
    background_x = 0
    background_y = 0

    # How far the level has scrolled
    world_shift_x = 0
    world_shift_y = 0
    at_edge_x = False
    at_edge_y = False

    # The start point of the level
    start_x = 0
    start_y = 0

    # If the level is running in fast mode
    fast = False

    def __init__(self, player, controls, sound_engine):

        # Constructor

        # Instantiate all of the groups

        # Platforms are anything the player collides with
        self.platform_list = pygame.sprite.Group()
        # Cosmetics are ignored by the player
        self.cosmetic_list = pygame.sprite.Group()
        # Obstacles kill the player
        self.obstacle_list = pygame.sprite.Group()
        # Keypads operate other platforms
        self.keypads = pygame.sprite.Group()
        # Bombs are bombs
        self.bombs = pygame.sprite.Group()
        # Doors are anything that can be controlled by a keypad
        # Also includes cameras
        self.doors = pygame.sprite.Group()
        # Guards are simply guards
        self.guards = pygame.sprite.Group()
        # Entities are any miscellaneous
        self.entities = pygame.sprite.Group()
        # All the levels level text
        self.level_text = pygame.sprite.Group()
        # Anything the player can climb
        self.ladders = pygame.sprite.Group()
        # Lasers from the cameras
        self.lasers = pygame.sprite.Group()
        # Anything that requires to be updated but not drawn to the display
        self.non_draw = pygame.sprite.Group()
        # This is the sky, only used on level 10
        self.sky = pygame.sprite.GroupSingle()

        # Set reference to the player
        self.player = player

        # Vars used to control the setup of keypads and doors
        self.keypad_array = []
        self.door_no = 0

        # How many layers the level has
        self.layer_range = 0

        # Load the controls
        self.controls = controls

        self.sound_engine = sound_engine

        # Load the background
        self.background = pygame.image.load("resources/background.png").convert()
        self.fast_background = pygame.image.load("resources/background_fast.png").convert()

    def update(self):

        # Update everything in the level that needs updated
        # Some groups such as cosmetics don't require updates
        self.obstacle_list.update()
        self.ladders.update()
        self.keypads.update()
        self.doors.update()
        self.bombs.update()
        self.guards.update()
        self.entities.update()
        self.lasers.update()
        self.non_draw.update()

    def draw(self, display):

        # Draw everything on this level

        # Start by drawing the background
        display.fill(constants.BLACK)
        if self.fast:
            display.blit(self.fast_background, (0, 0))
        else:
            display.blit(self.background, ((self.world_shift_x//4), (self.world_shift_y//-4)))

        # Draw the sky
        if len(self.sky.sprites()):
            self.sky.sprites()[0].draw(display)

        # Draw the sprite lists

        # Loop the number of times there are layers
        for layer in range(self.layer_range):

            # Get all the tiles that are in that layer and draw them
            # Repeat this for most of the groups
            cosmetics = [cosmetic for cosmetic in self.cosmetic_list.sprites() if cosmetic.layer == layer+1]
            for cosmetic in cosmetics:
                cosmetic.draw(display)

            obstacles = [obstacle for obstacle in self.obstacle_list.sprites() if obstacle.layer == layer+1]
            for obstacle in obstacles:
                obstacle.draw(display)

            ladders = [ladder for ladder in self.ladders.sprites() if ladder.layer == layer+1]
            for ladder in ladders:
                ladder.draw(display)

            # Draw lasers on the top layer
            if layer == self.layer_range-1:
                # Draw the sights from cameras
                for laser in self.lasers.sprites():
                    laser.draw(display)

            # Platforms need to be drawn after the lasers
            platforms = [platform for platform in self.platform_list.sprites() if platform.layer == layer + 1]
            for platform in platforms:
                platform.draw(display)

        # Draw other things that layers don't apply to
        self.level_text.draw(display)
        self.keypads.draw(display)
        self.bombs.draw(display)
        self.guards.draw(display)
        self.entities.draw(display)

    def shift_world(self, shift_x, shift_y):

        # Scroll the level left/right
        self.world_shift_x += shift_x

        self.at_edge_x = False

        # If the level has been scrolled to the edge, then set the at_edge var to true
        # This stops the level from scrolling any further
        if self.world_shift_x >= 0:
            self.at_edge_x = True
            self.world_shift_x = 0

        # Do the same again for the other diretion
        elif self.world_shift_x <= -(960 + (960 - constants.SCREEN_WIDTH)):
            self.at_edge_x = True
            self.world_shift_x = -(960 + (960 - constants.SCREEN_WIDTH))

        # If the level can scroll,
        if not self.at_edge_x:
            # Move everything in the level
            for platform in self.platform_list:
                platform.rect.x += shift_x
            for cosmetic in self.cosmetic_list:
                cosmetic.rect.x += shift_x
            for obstacle in self.obstacle_list:
                obstacle.rect.x += shift_x
            for ladder in self.ladders:
                ladder.rect.x += shift_x
            for keypad in self.keypads:
                keypad.rect.x += shift_x
            for bomb in self.bombs:
                bomb.rect.x += shift_x
            for guard in self.guards:
                guard.rect.x += shift_x
            for entity in self.entities:
                entity.rect.x += shift_x
            for text in self.level_text:
                text.rect.x += shift_x
            for sprite in self.non_draw:
                # Lasers position themselves relative to their parents,
                # so they do not need scrolled
                if not isinstance(sprite, entities.Laser):
                    sprite.rect.x += shift_x
            for sprite in self.sky:
                sprite.rect.x += shift_x

        # Repeat the process for the y axis
        self.world_shift_y += shift_y

        # Set the edges of the level
        self.at_edge_y = False
        if self.world_shift_y <= 0:
            self.at_edge_y = True
            self.world_shift_y = 0

        elif self.world_shift_y >= (720 + (720 - constants.SCREEN_HEIGHT)):
            self.at_edge_y = True
            self.world_shift_y = (720 + (720 - constants.SCREEN_HEIGHT))

        if not self.at_edge_y:
            # Move everything in the level
            for platform in self.platform_list:
                platform.rect.y -= shift_y
            for cosmetic in self.cosmetic_list:
                cosmetic.rect.y -= shift_y
            for obstacle in self.obstacle_list:
                obstacle.rect.y -= shift_y
            for ladder in self.ladders:
                ladder.rect.y -= shift_y
            for keypad in self.keypads:
                keypad.rect.y -= shift_y
            for bomb in self.bombs:
                bomb.rect.y -= shift_y
            for guard in self.guards:
                guard.rect.y -= shift_y
            for entity in self.entities:
                entity.rect.y -= shift_y
            for text in self.level_text:
                text.rect.y -= shift_y
            for sprite in self.non_draw:
                if not isinstance(sprite, entities.Laser):
                    sprite.rect.y -= shift_y
            for sprite in self.sky:
                sprite.rect.y -= shift_y

    def reset_world(self):

        # Moves platforms back to their original position
        for platform in self.platform_list:
            platform.rect.x = platform.start_x
            platform.rect.y = platform.start_y

        for cosmetic in self.cosmetic_list:
            cosmetic.rect.x = cosmetic.start_x
            cosmetic.rect.y = cosmetic.start_y

        for obstacle in self.obstacle_list:
            obstacle.rect.x = obstacle.start_x
            obstacle.rect.y = obstacle.start_y

        for ladder in self.ladders:
            ladder.rect.x = ladder.start_x
            ladder.rect.y = ladder.start_y

        for keypad in self.keypads:
            keypad.rect.x = keypad.start_x
            keypad.rect.y = keypad.start_y

        for bomb in self.bombs:
            bomb.rect.x = bomb.start_x
            bomb.rect.y = bomb.start_y

        for guard in self.guards:
            guard.rect.x = guard.start_x
            guard.rect.y = guard.start_y

        for entity in self.entities:
            entity.rect.x = entity.start_x
            entity.rect.y = entity.start_y

        for text in self.level_text:
            text.rect.x = text.start_x
            text.rect.y = text.start_y

        for sprite in self.non_draw:
            # Again lasers move themselves
            # so don't need to be adjusted jere
            if not isinstance(sprite, entities.Laser):
                sprite.rect.x = sprite.start_x
                sprite.rect.y = sprite.start_y

        for sprite in self.sky:
            sprite.rect.x = sprite.start_x
            sprite.rect.y = sprite.start_y

        self.world_shift_x = 0
        self.world_shift_y = 0

    def set_scrolling(self):

        # Scroll the level to the start position
        self.shift_world(self.start_x, self.start_y)

    def reset_objects(self):

        # Reset anything done to any objects in the level

        # If any doors have been opened,
        # then close them again
        [self.platform_list.add(door) for door in self.doors
         if door not in self.platform_list and isinstance(door, entities.Door)]

        # Reset any progress on keypads
        [keypad.reset() for keypad in self.keypads if isinstance(keypad, entities.Keypad)]

        # Reset any bombs
        [bomb.reset() for bomb in self.bombs.sprites()]
        [bomb.reset() for bomb in self.non_draw.sprites() if isinstance(bomb, entities.Bomb)]

        # Delete any fired bullets
        self.entities.remove([bullet for bullet in self.entities if isinstance(bullet, guard_parts.Bullet)])

    def create_platform(self, tile, x, y, layer):
        # Create a new platform
        # then add it to the list of platforms
        platform = platforms.Platform(tile, x, y, layer)
        self.platform_list.add(platform)

    def create_cosmetic(self, tile, x, y, layer):
        platform = platforms.Platform(tile, x, y, layer)
        self.cosmetic_list.add(platform)

    def create_obstacle(self, tile, x, y, layer):
        platform = platforms.Platform(tile, x, y, layer)
        self.obstacle_list.add(platform)

    def create_anim_obs(self, tile, x, y, layer):
        platform = platforms.AnimatedPlatform(tile, x, y, layer)
        self.obstacle_list.add(platform)

    def create_keypad(self, x, y):
        new_keypad = entities.Keypad(x, y, self)

        new_keypad.progress_bar = progressbar.ProgressBar()
        new_keypad.progress_bar.parent = new_keypad
        new_keypad.progress_bar.level = self
        new_keypad.progress_bar.rect.x = new_keypad.rect.centerx
        new_keypad.progress_bar.rect.y = new_keypad.rect.y - 20
        new_keypad.progress_bar.start_x = new_keypad.progress_bar.rect.x
        new_keypad.progress_bar.start_y = new_keypad.progress_bar.rect.y
        self.entities.add(new_keypad.progress_bar)

        self.keypads.add(new_keypad)
        self.keypad_array.append(new_keypad)

    def create_recharging_keypad(self, x, y):
        new_keypad = entities.RechargingKeypad(x, y, self)

        new_keypad.progress_bar = progressbar.ProgressBar()
        new_keypad.progress_bar.parent = new_keypad
        new_keypad.progress_bar.level = self
        new_keypad.progress_bar.rect.x = new_keypad.rect.centerx
        new_keypad.progress_bar.rect.y = new_keypad.rect.y - 20
        new_keypad.progress_bar.start_x = new_keypad.progress_bar.rect.x
        new_keypad.progress_bar.start_y = new_keypad.progress_bar.rect.y
        self.entities.add(new_keypad.progress_bar)

        self.keypads.add(new_keypad)
        self.keypad_array.append(new_keypad)

    def create_bomb(self, x, y):
        new_bomb = entities.Bomb(x, y)

        new_bomb.progress_bar = progressbar.ProgressBar()
        new_bomb.progress_bar.parent = new_bomb
        new_bomb.level = self
        new_bomb.progress_bar.level = self

        self.non_draw.add(new_bomb)

    def create_door(self, tile, x, y, layer):
        new_door = entities.Door(tile, x, y, layer)

        new_door.level = self
        new_door.door_no = self.door_no

        self.platform_list.add(new_door)
        self.doors.add(new_door)

    def create_guard(self, x, y):
        new_guard = guards.Guard(x, y)

        new_guard.level = self
        new_guard.player = self.player
        self.entities.add(new_guard.torch)

        self.guards.add(new_guard)

    def create_hguard(self, x, y):
        new_hguard = guards.HostileGuard(x, y, self)

        new_hguard.player = self.player
        self.entities.add(new_hguard.arm)

        self.guards.add(new_hguard)

    def create_ladder(self, tile, x, y, layer):
        new_ladder = platforms.Platform(tile, x, y, layer)
        self.ladders.add(new_ladder)

    def create_camera(self, tile, x, y, direction):
        new_camera = entities.Camera(x, y, tile, self)
        new_laser = entities.Laser(new_camera, self.player)
        new_camera.laser = new_laser
        new_camera.camera_no = self.door_no

        if not direction:
            new_laser.angle = 26

        self.entities.add(new_camera)
        self.doors.add(new_camera)
        self.lasers.add(new_laser)

    def create_sky(self, tile, x, y, layer):
        sky = entities.Sky(tile, x, y, layer)
        sky.level = self
        self.sky.add(sky)

    def render(self, data):

        self.door_no = 0
        self.keypad_array = []

        layer = 1
        n = 0
        for tile in data:
            position = tile[0]
            tile_data = tile[1]

            if 'type' not in tile_data:
                print(tile)

            if tile_data['type'] == "Door":
                self.door_no += 1
                if 39 < tile_data['tile'] < 42:
                    self.create_camera(platforms.platforms[tile_data['tile']-1],
                                       position[0]*24, position[1]*24, tile_data['tile']-40)
                else:
                    self.create_door(platforms.platforms[tile_data['tile']-1],
                                     position[0]*24, position[1]*24, layer)

            elif tile_data['type'] == "Entity":

                if tile_data['tile'] == 44:
                    self.create_keypad((position[0]*24)+6, (position[1]*24)+5)

                elif tile_data['tile'] == 42:
                    self.create_guard(position[0]*24, (position[1]*24)-24)

                elif tile_data['tile'] == 45:
                    self.create_bomb(position[0]*24, position[1]*24)

                elif tile_data['tile'] == 46:
                    self.create_hguard(position[0]*24, (position[1]*24)-24)

                elif tile_data['tile'] == 48:
                    self.create_recharging_keypad((position[0]*24)+6, (position[1]*24)+5)

            elif tile_data['type'] == "Solid":
                if tile_data['tile'] == 26:
                    self.create_platform(platforms.platforms[tile_data['tile']-1],
                                         position[0]*24, (position[1]*24)+20, layer)
                else:
                    self.create_platform(platforms.platforms[tile_data['tile']-1],
                                         position[0]*24, position[1]*24, layer)

            elif tile_data['type'] == "Cosmetic":
                if tile_data['tile'] == 25:
                    self.create_ladder(platforms.platforms[tile_data['tile']-1],
                                       position[0]*24, position[1]*24, layer)
                elif tile_data['tile'] == 39:
                    self.create_sky(platforms.platforms[tile_data['tile'] - 1],
                                    position[0] * 24, position[1] * 24, layer)
                else:
                    self.create_cosmetic(platforms.platforms[tile_data['tile']-1],
                                         position[0]*24, position[1]*24, layer)

            elif tile_data['type'] == "Obstacle":
                if tile_data['tile'] == 23:
                    if self.fast:
                        self.create_obstacle(platforms.platforms[tile_data['tile']-1][0],
                                             position[0]*24, position[1]*24, layer)
                    else:
                        self.create_anim_obs(platforms.platforms[tile_data['tile'] - 1],
                                             position[0] * 24, position[1] * 24, layer)
                else:
                    self.create_obstacle(platforms.platforms[tile_data['tile']-1],
                                         position[0]*24, position[1]*24, layer)
            n += 1
            if n % 4800 == 0:
                layer += 1


class Level01(Level):

    def __init__(self, player, write_data=False, fast=False, controls=None, sound_engine=None):

        # Call the parents constructor
        Level.__init__(self, player, controls, sound_engine)

        save_file = os.path.join("level_data", "level1.json")
        tile_file = os.path.join("level_data", "layouts", "level1")
        type_file = os.path.join("level_data", "tile_types", "level1")

        # How many layers the level has
        self.layer_range = 2

        self.fast = fast

        level = terrain.LevelData(save_file, tile_file, type_file, "level1")
        if write_data:
            level_data = level.write_data(fast)
        else:
            level_data = level.load_data()

        # Then render
        self.render(level_data)

        # Add the level text
        self.level_text.add(text.LevelText("Use {} and {} to walk left/right".format(
            pygame.key.name(self.controls["WALK_LEFT"]),
            pygame.key.name(self.controls["WALK_RIGHT"])
        ), 36, 960))
        self.level_text.add(text.LevelText("Use {} to jump!".format(
            pygame.key.name(self.controls["JUMP"])
        ), 36, 990))
        self.level_text.add(text.LevelText("Don't fall!", 615, 600))
        self.level_text.add(text.LevelText("Nearly there...", 975, 600))
        self.level_text.add(text.LevelText("Down we go", 1750, 450))

        # Set start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to start position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level02(Level):

    def __init__(self, player, write_data=False, fast=False, controls=None, sound_engine=None):

        # Call the parents constructor
        Level.__init__(self, player, controls, sound_engine)

        save_file = os.path.join("level_data", "level2.json")
        tile_file = os.path.join("level_data", "layouts", "level2")
        type_file = os.path.join("level_data", "tile_types", "level2")

        # How many layers the level has
        self.layer_range = 2

        self.fast = fast

        self.door_linkup = {0: 1,
                            1: 1,
                            2: 0,
                            3: 0,
                            4: 2,
                            5: 2,
                            6: 2,
                            7: 2,
                            8: 2}

        level = terrain.LevelData(save_file, tile_file, type_file, "level2")
        if write_data:
            level_data = level.write_data(fast)
        else:
            level_data = level.load_data()

        # Then render
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        # Add the level text
        self.level_text.add(text.LevelText("Watch out for the acid!", 100, 1300))
        self.level_text.add(text.LevelText("Nice!", 850, 1150))
        self.level_text.add(text.LevelText("This is tricky,", 50, 860))
        self.level_text.add(text.LevelText("good luck!", 50, 885))
        self.level_text.add(text.LevelText("Use {} to hack the keypad.".format(
            pygame.key.name(self.controls["ACTION"])
        ), 360, 50))
        self.level_text.add(text.LevelText("Once the keypad is hacked,", 360, 75))
        self.level_text.add(text.LevelText("the door will open.", 360, 100))
        self.level_text.add(text.LevelText("And again", 585, 270))
        self.level_text.add(text.LevelText("Jump!", 800, 370))
        self.level_text.add(text.LevelText("Congrats!", 1150, 700))
        self.level_text.add(text.LevelText("Choose your path", 1300, 625))

        # Set start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to start position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level03(Level):

    def __init__(self, player, write_data=False, fast=False, controls=None, sound_engine=None):

        # Call the parents constructor
        Level.__init__(self, player, controls, sound_engine)

        save_file = os.path.join("level_data", "level3.json")
        tile_file = os.path.join("level_data", "layouts", "level3")
        type_file = os.path.join("level_data", "tile_types", "level3")

        # How many layers the level has
        self.layer_range = 2

        self.fast = fast

        self.door_linkup = {0: 0,
                            1: 0}

        level = terrain.LevelData(save_file, tile_file, type_file, "level3")
        if write_data:
            level_data = level.write_data(fast)
        else:
            level_data = level.load_data()

        # Then render
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        # Add the level text
        self.level_text.add(text.LevelText("Watch out for the guards!", 110, 1075))
        self.level_text.add(text.LevelText("They're searching with torches,", 110, 1100))
        self.level_text.add(text.LevelText("Make sure they don't catch you!", 110, 1125))
        self.level_text.add(text.LevelText("Try to find a way to get past the guard.", 110, 1150))
        self.level_text.add(text.LevelText("Press the jump key", 700, 1300))
        self.level_text.add(text.LevelText("to climb ladders!", 700, 1325))
        self.level_text.add(text.LevelText("Here's another guard.", 500, 900))
        self.level_text.add(text.LevelText("Let go to slide down ladders.", 800, 800))
        self.level_text.add(text.LevelText("These are tricky jumps!", 1120, 1355))
        self.level_text.add(text.LevelText("Press {}".format(
            pygame.key.name(self.controls["CROUCH"])
        ), 1635, 1060))
        self.level_text.add(text.LevelText("to slide through", 1635, 1085))
        self.level_text.add(text.LevelText("tight spaces.", 1635, 1110))
        self.level_text.add(text.LevelText("Jump onto", 1200, 875))
        self.level_text.add(text.LevelText("the ladders.", 1200, 900))
        self.level_text.add(text.LevelText("You can also crouch", 920, 350))
        self.level_text.add(text.LevelText("under torches!", 920, 375))
        self.level_text.add(text.LevelText("Good job!", 200, 200))
        self.level_text.add(text.LevelText("Watch out here...", 1275, 425))

        # Set start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to start position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level04(Level):

    def __init__(self, player, write_data=False, fast=False, controls=None, sound_engine=None):

        # Call the parents constructor
        Level.__init__(self, player, controls, sound_engine)

        self.save_file = os.path.join("level_data", "level4.json")
        self.tile_file = os.path.join("level_data", "layouts", "level4")
        self.type_file = os.path.join("level_data", "tile_types", "level4")

        # How many layers the level has
        self.layer_range = 2

        self.fast = fast

        self.door_linkup = {0: 0,
                            1: 0,
                            2: 0,
                            3: 1,
                            4: 1}

        level = terrain.LevelData(self.save_file, self.tile_file, self.type_file, "level4")

        if write_data:
            level_data = level.write_data(fast)
        else:
            level_data = level.load_data()

        # Render it
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        # Add the level text
        self.level_text.add(text.LevelText("Up we go!", 80, 1060))
        self.level_text.add(text.LevelText("Crawl through ventilation shafts", 144, 90))
        self.level_text.add(text.LevelText("Doors aren't", 664, 130))
        self.level_text.add(text.LevelText("always vertical", 664, 155))
        self.level_text.add(text.LevelText("Slide through here!", 588, 476))
        self.level_text.add(text.LevelText("You'll need to hang about on these ladders.", 1200, 1350))
        self.level_text.add(text.LevelText("Here's some complex jumps", 1500, 700))

        # Set the start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to the starting position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level05(Level):

    def __init__(self, player, write_data=False, fast=False, controls=None, sound_engine=None):

        # Call the parents constructor
        Level.__init__(self, player, controls, sound_engine)

        self.save_file = os.path.join("level_data", "level5.json")
        self.tile_file = os.path.join("level_data", "layouts", "level5")
        self.type_file = os.path.join("level_data", "tile_types", "level5")

        # How many layers the level has
        self.layer_range = 2

        self.fast = fast

        self.door_linkup = {0: 0,
                            1: 0,
                            2: 1,
                            3: 1,
                            4: 2,
                            5: 2}

        level = terrain.LevelData(self.save_file, self.type_file, self.type_file, "level5")

        if write_data:
            level_data = level.write_data(fast)
        else:
            level_data = level.load_data()

        # Then render it
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        # Add the level text
        level_text = text.LevelText("Easy way out...", 700, 1350)
        self.level_text.add(level_text)
        level_text = text.LevelText("Ah, some doors.", 1600, 1350)
        self.level_text.add(level_text)
        level_text = text.LevelText("These jumps aren't easy!", 290, 670)
        self.level_text.add(level_text)
        level_text = text.LevelText("Here's a keypad.", 70, 30)
        self.level_text.add(level_text)
        level_text = text.LevelText("You need perfect timing for this.", 1560, 550)
        self.level_text.add(level_text)
        level_text = text.LevelText("Watch out for the acid!", 400, 1050)
        self.level_text.add(level_text)

        # Set the start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to the starting position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level06(Level):

    def __init__(self, player, write_data=False, fast=False, controls=None, sound_engine=None):

        # Call the parents constructor
        Level.__init__(self, player, controls, sound_engine)

        self.save_file = os.path.join("level_data", "level6.json")
        self.tile_file = os.path.join("level_data", "layouts", "level6")
        self.type_file = os.path.join("level_data", "tile_types", "level6")

        # How many layers the level has
        self.layer_range = 2

        self.fast = fast

        self.door_linkup = {0: 1,
                            1: 2,
                            2: 2,
                            3: 2,
                            4: 2,
                            5: 2,
                            6: 0}

        level = terrain.LevelData(self.save_file, self.tile_file, self.type_file, "level6")

        if write_data:
            level_data = level.write_data(fast)
        else:
            level_data = level.load_data()

        # Then render it
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        # Add the level text
        level_text = text.LevelText("Don't get caught by the camera!", 435, 1210)
        self.level_text.add(level_text)
        level_text = text.LevelText("Use the keypad to turn off the camera,", 435, 1235)
        self.level_text.add(level_text)
        level_text = text.LevelText("But it will turn on again soon!", 490, 1260)
        self.level_text.add(level_text)
        level_text = text.LevelText("Have fun with this bit...", 425, 600)
        self.level_text.add(level_text)
        level_text = text.LevelText("Better start running!", 100, 35)
        self.level_text.add(level_text)
        level_text = text.LevelText("Almost there...", 1680, 75)
        self.level_text.add(level_text)

        # Set the start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to the starting position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level07(Level):

    def __init__(self, player, write_data=False, fast=False, controls=None, sound_engine=None):

        # Call the parents constructor
        Level.__init__(self, player, controls, sound_engine)

        self.save_file = os.path.join("level_data", "level7.json")
        self.tile_file = os.path.join("level_data", "layouts", "level7")
        self.type_file = os.path.join("level_data", "tile_types", "level7")

        self.layer_range = 2

        self.fast = fast

        self.door_linkup = {0: 0,
                            1: 0,
                            2: 0,
                            3: 2,
                            4: 4,
                            5: 3,
                            6: 5,
                            7: 1,
                            8: 2,
                            9: 4,
                            10: 3,
                            11: 5,
                            12: 2,
                            13: 4,
                            14: 3,
                            15: 5,
                            16: 2,
                            17: 4,
                            18: 3,
                            19: 5,
                            20: 2,
                            21: 4,
                            22: 3,
                            23: 5,
                            24: 2,
                            25: 4,
                            26: 3,
                            27: 5,
                            28: 6}

        level = terrain.LevelData(self.save_file, self.tile_file, self.type_file, "level7")

        if write_data:
            level_data = level.write_data(fast)
        else:
            level_data = level.load_data()

        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        # Add the level text
        level_text = text.LevelText("if you get stuck then press", 80, 1060)
        self.level_text.add(level_text)
        level_text = text.LevelText("{} to restart the level".format(
            pygame.key.name(self.controls["RESTART"])
        ), 80, 1085)
        self.level_text.add(level_text)
        level_text = text.LevelText("Remember this trick?", 180, 550)
        self.level_text.add(level_text)
        level_text = text.LevelText("You really need to be fast here!", 800, 380)
        self.level_text.add(level_text)
        level_text = text.LevelText("You're past the security!", 890, 1230)
        self.level_text.add(level_text)
        level_text = text.LevelText("Use {} to plant bombs".format(
            pygame.key.name(self.controls["ACTION"])
        ), 890, 1255)
        self.level_text.add(level_text)
        level_text = text.LevelText("on each of the power supplies", 890, 1280)
        self.level_text.add(level_text)
        level_text = text.LevelText("Once you've placed the bomb", 1200, 1230)
        self.level_text.add(level_text)
        level_text = text.LevelText("use {} to activate it!".format(
            pygame.key.name(self.controls["ACTION"])
        ), 1200, 1255)
        self.level_text.add(level_text)
        level_text = text.LevelText("There are guards protecting these ones", 1480, 1070)
        self.level_text.add(level_text)
        level_text = text.LevelText("And a nice easy finish!", 1150, 800)
        self.level_text.add(level_text)
        level_text = text.LevelText("You can't go to the next level", 1500, 800)
        self.level_text.add(level_text)
        level_text = text.LevelText("until all the bombs are active", 1500, 825)
        self.level_text.add(level_text)

        self.start_x = 0
        self.start_y = 719

        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level08(Level):

    def __init__(self, player, write_data=False, fast=False, controls=None, sound_engine=None):

        Level.__init__(self, player, controls, sound_engine)

        self.save_file = os.path.join("level_data", "level8.json")
        self.tile_file = os.path.join("level_data", "layouts", "level8")
        self.type_file = os.path.join("level_data", "tile_types", "level8")

        self.layer_range = 2

        self.fast = fast

        self.door_linkup = {0: 0,
                            1: 0,
                            2: 0,
                            3: 0,
                            4: 1,
                            5: 1,
                            6: 1}

        level = terrain.LevelData(self.save_file, self.tile_file, self.type_file, "level8")

        if write_data:
            level_data = level.write_data(fast)
        else:
            level_data = level.load_data()

        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        # Add the level text
        level_text = text.LevelText("You've angered the guards!", 150, 1225)
        self.level_text.add(level_text)
        level_text = text.LevelText("They now have firearms.", 150, 1250)
        self.level_text.add(level_text)
        level_text = text.LevelText("Bullets will hurt you.", 150, 1275)
        self.level_text.add(level_text)
        level_text = text.LevelText("Try to dodge or hide from them!", 150, 1300)
        self.level_text.add(level_text)
        level_text = text.LevelText("There's another one up there!", 625, 1000)
        self.level_text.add(level_text)
        level_text = text.LevelText("You'll need to run right over him", 580, 780)
        self.level_text.add(level_text)
        level_text = text.LevelText("Big jump up head!", 150, 625)
        self.level_text.add(level_text)
        level_text = text.LevelText("i wonder what's down there...", 900, 600)
        self.level_text.add(level_text)
        level_text = text.LevelText("Ah, you made it!", 1300, 1250)
        self.level_text.add(level_text)
        level_text = text.LevelText("The keypad is up this way", 1590, 950)
        self.level_text.add(level_text)

        self.start_x = 0
        self.start_y = 719

        self.reset_world()
        self.set_scrolling()


class Level09(Level):

    def __init__(self, player, write_data=False, fast=False, controls=None, sound_engine=None):

        Level.__init__(self, player, controls, sound_engine)

        self.save_file = os.path.join("level_data", "level9.json")
        self.tile_file = os.path.join("level_data", "layouts", "level9")
        self.type_file = os.path.join("level_data", "tile_types", "level9")

        self.layer_range = 2

        self.fast = fast

        self.door_linkup = {0: 0,
                            1: 0,
                            2: 0}

        level = terrain.LevelData(self.save_file, self.tile_file, self.type_file, "level9")

        if write_data:
            level_data = level.write_data(fast)
        else:
            level_data = level.load_data()

        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        level_text = text.LevelText("There are lots of guards!", 70, 1080)
        self.level_text.add(level_text)
        level_text = text.LevelText("You really need to be quick...", 300, 1000)
        self.level_text.add(level_text)

        self.start_x = 0
        self.start_y = 719

        self.reset_world()
        self.set_scrolling()


class Level10(Level):

    def __init__(self, player, write_data=False, fast=False, controls=None, sound_engine=None):

        Level.__init__(self, player, controls, sound_engine)

        self.save_file = os.path.join("level_data", "level10.json")
        self.tile_file = os.path.join("level_data", "layouts", "level10")
        self.type_file = os.path.join("level_data", "tile_types", "level10")

        self.layer_range = 2

        self.fast = fast

        self.door_linkup = {0: 0,
                            1: 0}

        level = terrain.LevelData(self.save_file, self.tile_file, self.type_file, "level10")

        if write_data:
            level_data = level.write_data(self.fast)
        else:
            level_data = level.load_data()

        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        level_text = text.LevelText("Good luck!", 70, 1080)
        self.level_text.add(level_text)
        level_text = text.LevelText("Guards everywhere!", 200, 380)
        self.level_text.add(level_text)
        level_text = text.LevelText("Leap of faith", 300, 100)
        self.level_text.add(level_text)
        level_text = text.LevelText("Still more guards!", 1360, 750)
        self.level_text.add(level_text)
        level_text = text.LevelText("This was very cruel", 1050, 1090)
        self.level_text.add(level_text)
        level_text = text.LevelText("You did it!", 1750, 1090)
        self.level_text.add(level_text)

        self.start_x = 0
        self.start_y = 719

        self.reset_world()
        self.set_scrolling()
