import pygame

import spritesheet
import platforms
import math
import constants


class Door(platforms.Platform):

    # A door gets opened by keypads

    keypad = None
    level = None
    door_no = 0

    def __init__(self, tile, x, y, layer):

        # Call the parents constructor
        platforms.Platform.__init__(self, tile, x, y, layer)

    def set_keypad(self):

        # Set the keypad that operates this door
        # It does by finding the keypad set to this
        # doors id in the door_linkup dictionary

        self.keypad = self.level.keypad_array[self.level.door_linkup[self.door_no-1]]

    def update(self):

        # Update the status of the door
        # If its keypad is activated then
        # the door should be removed from the
        # platform list. This way it is no
        # longer drawn nor collided with
        if self.keypad.progress >= 10:
            self.level.platform_list.remove(self)

    def draw(self, display):

        # Draw the image of the door to the display
        display.blit(self.image, (self.rect.x, self.rect.y))


class Keypad(pygame.sprite.Sprite):

    progress_bar = None

    def __init__(self, x, y, level):

        # Constructor

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the level the keypad is located in
        self.level = level

        # Get the images for both when the keypad is active and not
        self.sprite_sheet = spritesheet.SpriteSheet("resources/keypad.png")

        self.image_off = self.sprite_sheet.get_image(0, 0, 12, 14)
        self.image_on = self.sprite_sheet.get_image(12, 0, 12, 14)

        self.image = self.image_off

        # Set the keypads rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Keep track of where it started so when
        # we reset the level we know where to put it
        self.start_x = x
        self.start_y = y

        # Set references to the sounds the keypad makes
        self.beep_sound = self.level.sound_engine.beep_sound
        self.beep_sound.set_volume(0.25)
        self.hiss_sound = self.level.sound_engine.hiss_sound
        self.hiss_sound.set_volume(0.25)

        # So we don't keep on playing the sounds
        # this is used to check whether we've not
        # played the sound yet.
        self.played_sound = False

        # How much is required for the keypad to be activated
        self.progress = 0

    def update(self):

        # Update the image if the pad is activated
        if self.progress >= 10:
            self.image = self.image_on
            if not self.played_sound:
                # Play the beep of the keypad activating
                # and the hiss of the door opening
                self.level.sound_engine.que_sound([self.beep_sound, 0])
                self.level.sound_engine.que_sound([self.hiss_sound, 0])

                # Say the keypad has played its sounds
                self.played_sound = True

    def reset(self):

        # Reset the keypads progress, image and progress bar
        self.progress = 0
        self.image = self.image_off
        self.played_sound = False
        self.progress_bar.level.entities.add(self.progress_bar)


class RechargingKeypad(Keypad):

    def __init__(self, x, y, level):

        # Constructor

        # Call the parents constructor
        Keypad.__init__(self, x, y, level)

        # Set a reference to the sounds this sprites plays
        self.click_sound = self.level.sound_engine.click_sound

        # How long between ticks
        self.timer_threshold = 70
        self.timer = self.timer_threshold

    def update(self):

        # Update the image if the pad is activated
        if self.progress >= 10:
            self.image = self.image_on
            if not self.played_sound:
                # If the keypad was activated then play the beep
                self.level.sound_engine.que_sound([self.beep_sound, 0])
                self.played_sound = True

        # If the keypad is not active then it can still play the sound
        if self.progress < 10 and self.played_sound:
            self.played_sound = False

        # When the keypad is off again
        # switch back to the off image
        if self.progress == 0:
            self.image = self.image_off

        # When its time for the progress to go down,
        # reduce the progress and play the click.
        if self.timer == 0:
            if self.progress > 0:
                self.timer = self.timer_threshold
                self.progress -= 1
                self.level.sound_engine.que_sound([self.click_sound, 0])

        else:
            self.timer -= 1


class Bomb(pygame.sprite.Sprite):

    # Bombs are placed by the player
    # once they are placed they can be activated

    progress_bar = None
    level = None

    def __init__(self, x, y):

        # Constructor

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Load and set the sprites images
        self.sprite_sheet = spritesheet.SpriteSheet("resources/bomb.png")

        self.image_off = self.sprite_sheet.get_image(0, 0, 24, 24)
        self.image_on = self.sprite_sheet.get_image(24, 0, 24, 24)

        self.image = self.image_off

        # Set the rectangle, position and start position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start_x = x
        self.start_y = y

        # A beep sound to be played when the bomb is activated
        self.beep_sound = self.level.sound_engine.beep_sound
        self.played_sound = False

        # How much is required for the bomb to be activated
        self.progress = 0

        # Bools to control the state of the bomb
        self.placed = False
        self.has_placed = False

    def update(self):

        if not self.has_placed:
            if self.placed:
                # If the bomb has just been placed then
                # remove it from the non_draw group
                # and add it to the bombs group.
                # It also needs to be given a progress bar bar
                self.level.non_draw.remove(self)
                self.level.bombs.add(self)
                self.level.entities.add(self.progress_bar)
                self.has_placed = True
        else:
            # Update the image if the bomb is activated
            if self.progress >= 10:
                if not self.played_sound:
                    # When the bomb is activated then
                    # set its image and play the beep sound
                    self.image = self.image_on
                    self.level.sound_engine.que_sound([self.beep_sound, 0])
                    self.played_sound = True

    def reset(self):

        # Reset the bomb to its original inactive, unplaced state
        self.level.bombs.remove(self)
        self.level.non_draw.add(self)
        self.level.entities.remove(self.progress_bar)
        self.progress = 0
        self.played_sound = False
        self.placed = False
        self.image = self.image_off


class Crosshair(pygame.sprite.Sprite):

    # The crosshair is purely cosmetic
    # It simply fits the theme better than a mouse pointer

    def __init__(self):

        # Constructor

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the image
        sprite_sheet = spritesheet.SpriteSheet("resources/crosshair.png")

        self.image = sprite_sheet.get_image(0, 0, 24, 24)

        # Set the rectangle
        self.rect = self.image.get_rect()

        # This is where the mouse is at
        self.mouse_x = 0
        self.mouse_y = 0

    def update(self):

        # Get the position of the mouse pointer
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # Then position itself relevant to that
        self.rect.x = self.mouse_x - self.rect.width/2
        self.rect.y = self.mouse_y - self.rect.height/2

    def draw(self, display):

        # Draw off-screen where it cant be seen when the mouse is also off-screen
        if self.mouse_x <= 6 or self.mouse_x >= 954 or self.mouse_y <= 6 or self.mouse_y >= 714:
            display.blit(self.image, (-24, -24))
        else:
            # Otherwise draw to its rect position
            display.blit(self.image, (self.rect.x, self.rect.y))


class ExclamationMark(pygame.sprite.Sprite):

    def __init__(self, guard):

        pygame.sprite.Sprite.__init__(self)

        self.guard = guard

        sprite_sheet = spritesheet.SpriteSheet("resources/exclamation.png")
        self.image = sprite_sheet.get_image_srcalpha(0, 0, 29, 43)

        self.rect = self.image.get_rect()
        self.rect.centerx = self.guard.rect.centerx
        self.rect.y = self.guard.rect.y - 36

        self.start_x = self.rect.x
        self.start_y = self.rect.y
        self.timer = 120

    def update(self):

        self.guard.level.entities.remove(self)


class Camera(pygame.sprite.Sprite):

    camera_no = 0

    def __init__(self, x, y, image, level):

        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = spritesheet.SpriteSheet("resources/terrain.png")
        self.image = sprite_sheet.get_image(image[0],
                                            image[1],
                                            image[2],
                                            image[3])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start_x = self.rect.x
        self.start_y = self.rect.y

        self.level = level

        self.laser = None
        self.keypad = None

    def update(self):

        # Update the status of the door
        if self.keypad.progress >= 10:
            self.level.lasers.remove(self.laser)
            self.level.non_draw.add(self.laser)

    def set_keypad(self):
        # Set the keypad that operates this door
        self.keypad = self.level.keypad_array[self.level.door_linkup[self.camera_no-1]]


class Laser(pygame.sprite.Sprite):

    def __init__(self, camera, player):

        pygame.sprite.Sprite.__init__(self)

        self.camera = camera
        self.player = player

        self.start_point = (self.camera.rect.centerx, self.camera.rect.centery - 5)
        self.end_point = (self.camera.rect.centerx + 1, self.camera.rect.centery + 1)

        self.angle = 154

        self.start_x = 0
        self.start_y = 0

        self.vector = None

    def update(self):

        # Draw the line that the camera sees
        # Using the camera angle, follow it's line of perspective until you hit a platform
        # Then draw a line connecting the two points

        self.start_point = (self.camera.rect.centerx, self.camera.rect.centery - 5)

        if self.vector is None:
            x_angle = math.cos(math.radians(self.angle))
            y_angle = math.sin(math.radians(self.angle))

            platforms = [platform for platform in self.camera.level.platform_list.sprites()]

            # Calculate end point
            at_platform = False
            dist = 0
            while not at_platform:
                dist += 30
                self.end_point = (self.start_point[0] + dist * x_angle,
                                  self.start_point[1] + dist * y_angle)

                for platform in platforms:
                    if platform.rect.collidepoint(self.end_point):
                        at_platform = True

            self.vector = (self.end_point[0] - self.start_point[0],
                           self.end_point[1] - self.start_point[1])
        else:
            self.end_point = (self.start_point[0]+self.vector[0],
                              self.start_point[1]+self.vector[1])

        if self in self.camera.level.non_draw:
            if self.camera.keypad.progress == 0:
                self.camera.level.non_draw.remove(self)
                self.camera.level.lasers.add(self)

    def draw(self, display):

        pygame.draw.line(display, constants.RED,
                         (self.start_point[0], self.start_point[1]),
                         (self.end_point[0], self.end_point[1]), 1)

    def test_collision(self):

        if self.start_point[0] - self.end_point[0] > 0:

            if self.start_point[0] < self.player.rect.left or self.end_point[0] > self.player.rect.right:
                return False
        else:
            if self.start_point[0] > self.player.rect.right or self.end_point[0] < self.player.rect.left:
                return False
        if self.start_point[1] > self.player.rect.bottom or self.end_point[1] < self.player.rect.top:
            return False

        for n in range(10):
            try:
                line_gradient = (self.end_point[1] - self.start_point[1]) /\
                                (self.end_point[0] - self.start_point[0])
                player_gradient = (self.player.rect.y+self.player.rect.height*((n*10)/100) - self.start_point[1]) /\
                                  (self.player.rect.x - self.start_point[0])
            except ZeroDivisionError:
                return False

            diff = player_gradient - line_gradient

            if abs(diff) < 0.05 - n/500:
                return True

        return False


class Sky(pygame.sprite.Sprite):

    level = None

    def __init__(self, sprite_sheet_data, x, y, layer=1):

        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = spritesheet.SpriteSheet("resources/sky.png")

        self.full_image = sprite_sheet.get_image(sprite_sheet_data[0],
                                                 sprite_sheet_data[1],
                                                 sprite_sheet_data[2],
                                                 sprite_sheet_data[3])

        self.image = pygame.Surface([240, 1152]).convert()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start_x = x
        self.start_y = y

        # The layer the tile is in
        self.layer = layer

    def draw(self, display):

        # To make the sky look more believable make it scroll slower
        # than the rest of the platforms.
        # This is complicated for the sky
        # since it's position needs to move relative to the rest of the tiles
        self.image.fill(constants.BLACK)

        self.image.blit(self.full_image, ((self.level.world_shift_x//-4)-240,
                                          (self.level.world_shift_y//4)))
        display.blit(self.image, (self.rect.x, self.rect.y))
