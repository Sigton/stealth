import pygame

import spritesheet


class Door(pygame.sprite.Sprite):

    keypad = None
    level = None
    door_no = 0

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/terrain.png")

        self.image = self.sprite_sheet.get_image(96, 48, 24, 24)
        self.rect = self.image.get_rect()

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


class Keypad(pygame.sprite.Sprite):

    progress_bar = None

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/keypad.png")

        self.image_off = self.sprite_sheet.get_image(0, 0, 12, 14)
        self.image_on = self.sprite_sheet.get_image(12, 0, 12, 14)

        self.image = self.image_off

        self.rect = self.image.get_rect()

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

    def __init__(self):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/bomb.png")

        self.image_off = self.sprite_sheet.get_image(0, 0, 24, 24)
        self.image_on = self.sprite_sheet.get_image(24, 0, 24, 24)

        self.image = self.image_off

        self.rect = self.image.get_rect()

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

    def update(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.rect.x = mouse_x - self.rect.width/2
        self.rect.y = mouse_y - self.rect.height/2
