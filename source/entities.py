import pygame

import spritesheet
import platforms
import math
import constants


class Door(platforms.Platform):

    keypad = None
    level = None
    door_no = 0

    def __init__(self, tile, x, y, layer):

        # Call the parents constructor
        platforms.Platform.__init__(self, tile, x, y, layer)

        self.hiss_sound = pygame.mixer.Sound("resources/hiss.wav")
        self.hiss_sound.set_volume(0.25)

    def set_keypad(self):
        # Set the keypad that operates this door
        self.keypad = self.level.keypad_array[self.level.door_linkup[self.door_no-1]]

    def update(self):

        # Update the status of the door
        if self.keypad.progress >= 10:
            self.level.platform_list.remove(self)
            pygame.mixer.Sound.play(self.hiss_sound)

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))


class Keypad(pygame.sprite.Sprite):

    progress_bar = None

    def __init__(self, x, y):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/keypad.png")

        self.image_off = self.sprite_sheet.get_image(0, 0, 12, 14)
        self.image_on = self.sprite_sheet.get_image(12, 0, 12, 14)

        self.image = self.image_off

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start_x = x
        self.start_y = y

        self.beep_sound = pygame.mixer.Sound("resources/beep.wav")
        self.beep_sound.set_volume(0.25)
        self.played_sound = False

        # How much is required for the keypad to be activated
        self.progress = 0

    def update(self):

        # Update the image if the pad is activated
        if self.progress >= 10:
            self.image = self.image_on
            if not self.played_sound:
                pygame.mixer.Sound.play(self.beep_sound)
                self.played_sound = True


class Bomb(pygame.sprite.Sprite):

    progress_bar = None

    def __init__(self, x, y):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/bomb.png")

        self.image_off = self.sprite_sheet.get_image(0, 0, 24, 24)
        self.image_on = self.sprite_sheet.get_image(24, 0, 24, 24)

        self.image = self.image_off

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start_x = x
        self.start_y = y

        self.beep_sound = pygame.mixer.Sound("resources/beep.wav")
        self.beep_sound.set_volume(0.25)
        self.played_sound = True

        # How much is required for the bomb to be activated
        self.progress = 0

    def update(self):

        # Update the image if the bomb is activated
        if self.progress >= 10:
            self.image = self.image_on
            if not self.played_sound:
                pygame.mixer.Sound.play(self.beep_sound)
                self.played_sound = True


class Crosshair(pygame.sprite.Sprite):

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the image
        sprite_sheet = spritesheet.SpriteSheet("resources/crosshair.png")

        self.image = sprite_sheet.get_image(0, 0, 24, 24)

        self.rect = self.image.get_rect()

        self.mouse_x = 0
        self.mouse_y = 0

    def update(self):

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        self.rect.x = self.mouse_x - self.rect.width/2
        self.rect.y = self.mouse_y - self.rect.height/2

    def draw(self, display):

        if self.mouse_x <= 6 or self.mouse_x >= 954 or self.mouse_y <= 6 or self.mouse_y >= 714:
            display.blit(self.image, (-24, -24))
        else:
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

        self.end_point = None

    def update(self):

        # Draw the line that the camera sees
        # Using the camera angle, follow it's line of perspective until you hit a platform
        # Then draw a line connecting the two points

        at_platform = False
        dist = 0
        self.end_point = None

        while not at_platform:

            dist += 2
            x, y = dist*math.degrees(math.cos(26)), dist*math.degrees(math.sin(26))

            at_platform = True if [platform.rect.collidepoint(x, y)
                                   for platform in self.level.platform_list.sprites()] else False

            self.end_point = (x, y) if at_platform else None

    def draw_lines(self, display):

        start_point = (self.rect.centerx, self.rect.centery)

        pygame.draw.line(display, constants.RED, start_point, self.end_point, width=2)
