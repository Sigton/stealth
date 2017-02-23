import pygame

import spritesheet
import text as t
import constants


class Label(t.Text):

    def __init__(self, text, size, x, y):

        t.Text.__init__(self, text, size, x, y)

        self.start_x = self.rect.centerx
        self.start_y = self.rect.centery

    def update_text(self, text):

        self.image = self.font.render(text, True, constants.WHTIE)

        self.rect = self.image.get_rect()

        self.rect.centerx = self.start_x
        self.rect.centery = self.start_y

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))


class HUD(pygame.sprite.Sprite):

    def __init__(self, player):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = spritesheet.SpriteSheet("resources/hud_bar.png")
        self.image = sprite_sheet.get_image(0, 0, 480, 48)

        self.rect = self.image.get_rect()
        self.rect.centerx = 480
        self.rect.y = 672

        self.health_label = Label("Health:", 28, 248, 680)
        self.stamina_label = Label("Stamina:", 28, 488, 680)

        self.health_num = Label("10", 28, 368, 680)
        self.stamina_num = Label("10", 28, 608, 680)

        self.player = player

    def update(self):

        if self.player.rect.y > 200:
            self.rect.y = 0
            self.health_label.rect.centery = 24
            self.stamina_label.rect.centery = 24
            self.health_num.rect.centery = 24
            self.stamina_num.rect.centery = 24
        else:
            self.rect.y = 672
            self.health_label.rect.centery = 696
            self.stamina_label.rect.centery = 696
            self.health_num.rect.centery = 696
            self.stamina_num.rect.centery = 696

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))
        self.health_label.draw(display)
        self.stamina_label.draw(display)
        self.health_num.draw(display)
        self.stamina_num.draw(display)
