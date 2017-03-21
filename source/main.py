import pygame
from pygame.locals import *

# tkinter is used for the launcher GUI
import tkinter as tk
from tkinter import ttk

import menu as m
import constants
import os


class LauncherApp(tk.Tk):

    # The launcher to select game options

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Stealth Launcher")
        self.geometry("480x360")
        self.resizable(0, 0)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        frame = Launcher(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


class Launcher(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        self.fast = tk.IntVar()
        self.small = tk.IntVar()

        self.game = None

        self.background_image = tk.PhotoImage(file="resources/launcher_background.gif")
        self.background_label = ttk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0)

        self.title = ttk.Label(self, text="Stealth", font=("Verdana", 16), background="#0b2837")
        self.title.place(x=240, y=20, anchor="center")

        self.desc = ttk.Label(self, text="Select the launch options you want for your game.", background="#0b2837")
        self.desc.place(x=240, y=60, anchor="center")

        self.button1 = ttk.Checkbutton(self, text="Fast Mode", variable=self.fast)#, background="#0b2837")
        self.button1.place(x=50, y=100, anchor="w")
        self.label1 = ttk.Label(self, text="Removes decorations for better performance.",
                                font="Helvetica 9 italic", background="#0b2837")
        self.label1.place(x=160, y=100, anchor="w")

        self.button2 = ttk.Checkbutton(self, text="Small Screen", variable=self.small)#, background="#0b2837")
        self.button2.place(x=50, y=130, anchor="w")
        self.label2 = ttk.Label(self, text="Smaller window for smaller or lower resolution monitors.",
                                font="Helvetica 9 italic", background="#0b2837")
        self.label2.place(x=160, y=130, anchor="w")

        self.launch_button = tk.Button(self, text="Launch", width="20", height="2", bg="#566b75",
                                       activebackground="#93a6af", command=self.launch)
        self.launch_button.place(x=240, y=320, anchor="center")

    def launch(self):

        self.game = Main(bool(self.fast.get()), bool(self.small.get()))
        self.controller.withdraw()
        self.game.run()
        self.controller.deiconify()


class Main:

    def __init__(self, fast_mode, small_mode):
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

        self.fast = fast_mode
        self.small = small_mode

    def run(self):

        # Start the menu
        menu = m.Menu(self)
        menu.run()

        # Quit the game
        pygame.quit()

    def set_screen_size(self, new_width, new_height):

        self.game_display = pygame.display.set_mode(constants.set_screen_size(new_width, new_height))

        return self.game_display

if __name__ == "__main__":
    # Open the launcher
    launcher = LauncherApp()
    launcher.mainloop()
