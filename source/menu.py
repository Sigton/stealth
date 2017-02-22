import pygame
from pygame.locals import *

import game as g
import spritesheet
import constants


class Button(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet, sprite_sheet_data, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet(sprite_sheet)

        self.image_inactive = self.sprite_sheet.get_image_srcalpha(sprite_sheet_data[0][0],
                                                                   sprite_sheet_data[0][1],
                                                                   sprite_sheet_data[0][2],
                                                                   sprite_sheet_data[0][3])

        self.image_active = self.sprite_sheet.get_image_srcalpha(sprite_sheet_data[1][0],
                                                                 sprite_sheet_data[1][1],
                                                                 sprite_sheet_data[1][2],
                                                                 sprite_sheet_data[1][3])

        self.image = self.image_inactive

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):

        mouse_pos = pygame.mouse.get_pos()

        touching_pointer = self.rect.collidepoint(mouse_pos)

        if touching_pointer:
            if self.image != self.image_active:
                self.image = self.image_active
        else:
            if self.image != self.image_inactive:
                self.image = self.image_inactive


class Text(pygame.sprite.Sprite):

    def __init__(self, text, size, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.font = pygame.font.Font("resources/alienleague.ttf", size)

        self.image = self.font.render(text, True, constants.WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Menu:

    def __init__(self, display, clock):

        self.display = display
        self.clock = clock

        self.game = g.Game(display, clock)

        self.background = pygame.image.load("resources/menubackground.png").convert()

        self.main_menu = pygame.sprite.Group()
        self.main_menu.add(Button("resources/menubuttons.png", ((0, 0, 360, 80), (360, 0, 360, 80)), 340, 350))
        self.main_menu.add(Button("resources/menubuttons.png", ((0, 80, 360, 80), (360, 80, 360, 80)), 300, 430))
        self.main_menu.add(Button("resources/menubuttons.png", ((0, 160, 360, 80), (360, 160, 360, 80)), 260, 510))

        self.main_menu.add(Text("STEALTH", 200, 165, 100))

    def run(self):

        game_exit = False

        while not game_exit:

            for event in pygame.event.get():
                if event.type == QUIT:
                    game_exit = True

            self.main_menu.update()

            self.display.fill(constants.BLACK)
            self.display.blit(self.background, (0, 0))

            self.main_menu.draw(self.display)

            pygame.display.update()
            self.clock.tick(60)

        pygame.mouse.set_visible(False)
