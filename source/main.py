import pygame
from pygame.locals import *

# tkinter is used for the launcher GUI
import tkinter as tk
from tkinter import ttk

import menu as m
import constants
import sys


class LauncherApp(tk.Tk):

    # The launcher to select game options

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Stealth Launcher")
        self.geometry("480x360")


class Main:

    def __init__(self):
        # Main Program

        # Initiate pygame
        pygame.mixer.pre_init(22050, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        # Set the display size
        self.game_display = pygame.display.set_mode(constants.SIZE)

        # Set the window caption and icon
        pygame.display.set_caption("Stealth")

        icon_img = pygame.image.load("resources/icon.ico")

        icon = pygame.Surface([32, 32], flags=SRCALPHA)
        icon = icon.convert_alpha()
        icon.blit(icon_img, (0, 0))
        pygame.display.set_icon(icon)

        # Used to manage update frequency
        self.clock = pygame.time.Clock()

    def run(self):

        # Start the menu
        menu = m.Menu(self)
        menu.run()

        # Quit the game
        pygame.quit()
        sys.exit(0)

    def set_screen_size(self, new_width, new_height):

        self.game_display = pygame.display.set_mode(constants.set_screen_size(new_width, new_height))

        return self.game_display

if __name__ == "__main__":
    # Begin everything
    game = Main()
    game.run()
