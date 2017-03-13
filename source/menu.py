import pygame
from pygame.locals import *

import game as g
import spritesheet
import text
import constants


class Button(pygame.sprite.Sprite):

    # Generic button class

    def __init__(self, sprite_sheet, sprite_sheet_data, x, y, command):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the sprites images
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

        # Correct the sprites position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set the command
        self.command = command

    def update(self):

        # Get the mouse pointer position
        mouse_pos = pygame.mouse.get_pos()

        # Check if the mouse is touching the button
        touching_pointer = self.rect.collidepoint(mouse_pos)
        if touching_pointer:  # If it is then switch the image
            if self.image != self.image_active:
                self.image = self.image_active
        else:
            if self.image != self.image_inactive:
                self.image = self.image_inactive


class Menu:

    # This is the games menu

    def __init__(self, parent):

        self.parent = parent

        # Set the display to draw to and the clock for timing
        self.display = parent.game_display
        self.clock = parent.clock

        # Create an instance of the game class
        self.game = g.Game(self)

        # Set the background
        self.background = pygame.image.load("resources/menubackground.png").convert()

        # Fill the group with everything on that screen of the menu
        self.main_menu = pygame.sprite.Group()
        self.main_menu.add(Button("resources/menubuttons.png", ((0, 0, 360, 80), (360, 0, 360, 80)),
                                  320, 350, lambda: self.game.run()))
        self.main_menu.add(Button("resources/menubuttons.png", ((0, 80, 360, 80), (360, 80, 360, 80)),
                                  282, 426, "quit"))

        self.main_menu.add(text.Text("Stealth", 200, 165, 100))

        # The screen that is currently displayed
        self.current_screen = None

        # Lag mode
        self.lagging = False

    def run(self):

        # Load the music
        pygame.mixer.music.load("resources/menu_music.mp3")
        pygame.mixer.music.set_volume(0.75)

        # Set the current screen
        self.current_screen = self.main_menu

        # Play the music
        pygame.mixer.music.play(-1)

        game_exit = False

        while not game_exit:

            # Event loop
            for event in pygame.event.get():
                if event.type == QUIT:  # Quit closes the application
                    game_exit = True

                if event.type == MOUSEBUTTONUP:

                    # Check if any buttons were clicked
                    mouse_pos = pygame.mouse.get_pos()

                    buttons_clicked = [x for x in self.current_screen if x.rect.collidepoint(mouse_pos)
                                       and isinstance(x, Button)]

                    for button in buttons_clicked:
                        if button.command is not None:

                            # Execute the buttons command

                            if button.command == "quit":  # Special case for quitting game
                                game_exit = True

                            else:
                                button.command()

                if event.type == KEYUP:

                    if event.key == K_F8:
                        self.toggle_lag()

            # Update the sprites
            self.current_screen.update()

            # Draw to the display
            self.display.fill(constants.BLACK)
            self.display.blit(self.background, (0, 0))

            self.current_screen.draw(self.display)

            # Update and limit to 60fps
            pygame.display.update()
            self.clock.tick(60)

        pygame.mouse.set_visible(False)

    def toggle_lag(self):

        if not self.lagging:
            self.lagging = True
            self.display = self.parent.set_screen_size(720, 540)

        else:
            self.lagging = False
            self.display = self.parent.set_screen_size(960, 720)
