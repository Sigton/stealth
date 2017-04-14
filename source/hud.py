import pygame

import spritesheet
import text
import constants


class Label(text.Text):

    def __init__(self, texts, size, x, y):

        text.Text.__init__(self, texts, size, x, y)

        self.start_x = self.rect.centerx
        self.start_y = self.rect.centery

    def update_text(self, texts):

        self.image = self.font.render(texts, True, constants.WHITE)

        self.rect = self.image.get_rect()

        self.rect.centerx = self.start_x
        self.rect.centery = self.start_y

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))


class HUD(pygame.sprite.Sprite):

    def __init__(self, player, small):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.middle = 360 if small else 480

        sprite_sheet = spritesheet.SpriteSheet("resources/hud_bar.png")
        self.image = sprite_sheet.get_image(0, 0, 480, 48)

        self.rect = self.image.get_rect()
        self.rect.centerx = self.middle
        self.rect.y = 672

        self.health_label = Label("Health:", 28, self.middle - 232, 680)
        self.stamina_label = Label("Stamina:", 28, self.middle + 8, 680)

        self.health_num = Label("100%", 28, self.middle - 112, 680)
        self.stamina_num = Label("100%", 28, self.middle + 128, 680)

        self.player = player

        self.y_pos = 492 if small else 672

    def update(self):

        self.health_num.update_text("{0:.1f}%".format(round(self.player.health, 1)))
        self.stamina_num.update_text("{0:.1f}%".format(round(self.player.stamina -
                                                             self.player.stamina*(1-(self.player.stamina/100)), 1)))

        if self.player.rect.y > 200:
            self.rect.y = 0
            self.health_label.rect.centery = 24
            self.stamina_label.rect.centery = 24
            self.health_num.rect.centery = 24
            self.stamina_num.rect.centery = 24
        else:
            self.rect.y = self.y_pos
            self.health_label.rect.centery = self.y_pos + 24
            self.stamina_label.rect.centery = self.y_pos + 24
            self.health_num.rect.centery = self.y_pos + 24
            self.stamina_num.rect.centery = self.y_pos + 24

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))
        self.health_label.draw(display)
        self.stamina_label.draw(display)
        self.health_num.draw(display)
        self.stamina_num.draw(display)


class Timer(Label):

    def __init__(self, num):

        Label.__init__(self, str(num), 32, 10, 10)

        self.value = num
        self.can_update = False

    def update(self):

        if self.can_update:
            self.value -= 1
            self.update_text(str(self.value))
