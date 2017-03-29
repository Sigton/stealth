import pygame
from pygame.locals import *

# tkinter is used for the launcher GUI
import tkinter as tk

import menu as m
import constants
import saves


# Initiate pygame
pygame.mixer.pre_init(22050, -16, 1, 512)
pygame.mixer.init()
pygame.init()


class LauncherApp(tk.Tk):

    # The launcher to select game options

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Stealth Launcher")
        self.geometry("480x480")
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

        saves.controls = saves.load_controls()

        self.title = tk.Label(self, text="Stealth", font=("Verdana", 20))
        self.title.place(x=240, y=20, anchor="center")

        self.config_heading = tk.Label(self, text="Game Configuration", font=("Verdana", 12))
        self.config_heading.place(x=240, y=65, anchor="center")

        self.desc = tk.Label(self, text="Select the launch options you want for your game.")
        self.desc.place(x=240, y=90, anchor="center")

        self.button1 = tk.Checkbutton(self, text="Fast Mode", variable=self.fast)
        self.button1.place(x=50, y=120, anchor="w")
        self.label1 = tk.Label(self, text="Removes decorations for better performance.",
                               font="Helvetica 9 italic")
        self.label1.place(x=160, y=120, anchor="w")

        self.button2 = tk.Checkbutton(self, text="Small Screen", variable=self.small)
        self.button2.place(x=50, y=150, anchor="w")
        self.label2 = tk.Label(self, text="Smaller window for smaller or lower resolution monitors.",
                               font="Helvetica 9 italic")
        self.label2.place(x=160, y=150, anchor="w")

        self.controls_heading = tk.Label(self, text="Control Configuration", font=("Verdana", 12))
        self.controls_heading.place(x=240, y=200, anchor="center")

        self.control1_label = tk.Label(self, text="Walk Left Button:")
        self.control1_label.place(x=50, y=240, anchor="w")
        self.control1 = tk.Label(self, text=pygame.key.name(saves.controls["WALK_LEFT"]))
        self.control1.place(x=160, y=240, anchor="w")
        self.control1_button = tk.Button(self, text="Change",
                                         command=lambda: self.set_control("WALK_LEFT"))
        self.control1_button.place(x=230, y=240, anchor="w")

        self.control2_label = tk.Label(self, text="Walk Right Button:")
        self.control2_label.place(x=50, y=270, anchor="w")
        self.control2 = tk.Label(self, text=pygame.key.name(saves.controls["WALK_RIGHT"]))
        self.control2.place(x=160, y=270, anchor="w")
        self.control2_button = tk.Button(self, text="Change",
                                         command=lambda: self.set_control("WALK_RIGHT"))
        self.control2_button.place(x=230, y=270, anchor="w")

        self.control3_label = tk.Label(self, text="Jump Button:")
        self.control3_label.place(x=50, y=300, anchor="w")
        self.control3 = tk.Label(self, text=pygame.key.name(saves.controls["JUMP"]))
        self.control3.place(x=160, y=300, anchor="w")
        self.control3_button = tk.Button(self, text="Change",
                                         command=lambda: self.set_control("JUMP"))
        self.control3_button.place(x=230, y=300, anchor="w")

        self.control4_label = tk.Label(self, text="Action Button:")
        self.control4_label.place(x=50, y=330, anchor="w")
        self.control4 = tk.Label(self, text=pygame.key.name(saves.controls["ACTION"]))
        self.control4.place(x=160, y=330, anchor="w")
        self.control4_button = tk.Button(self, text="Change",
                                         command=lambda: self.set_control("ACTION"))
        self.control4_button.place(x=230, y=330, anchor="w")

        self.control5_label = tk.Label(self, text="Crouch Button:")
        self.control5_label.place(x=50, y=360, anchor="w")
        self.control5 = tk.Label(self, text=pygame.key.name(saves.controls["CROUCH"]))
        self.control5.place(x=160, y=360, anchor="w")
        self.control5_button = tk.Button(self, text="Change",
                                         command=lambda: self.set_control("CROUCH"))
        self.control5_button.place(x=230, y=360, anchor="w")

        self.save_controls_button = tk.Button(self, text="Set as default", command=saves.save_controls)
        self.save_controls_button.place(x=350, y=300, anchor="w")

        self.launch_button = tk.Button(self, text="Launch", width="20", height="2",
                                       bg="#bbb", activebackground="#ccc", command=self.launch)
        self.launch_button.place(x=240, y=440, anchor="center")

    def launch(self):

        self.game = Main(bool(self.fast.get()), bool(self.small.get()))
        self.controller.destroy()
        self.game.run()

    def set_control(self, control):

        self.controller.unbind("<KeyPress>")
        self.controller.bind("<KeyPress>", lambda event, c=control: self.get_key(event, c))

    def get_key(self, event, control):

        if event.keycode in saves.trans_dict:
            code = saves.trans_dict[event.keycode]
        else:
            code = event.keycode
        saves.controls[control] = code
        self.update_controls()
        self.controller.unbind("<KeyPress>")

    def update_controls(self):
        self.control1.configure(text=pygame.key.name(saves.controls["WALK_LEFT"]))
        self.control2.configure(text=pygame.key.name(saves.controls["WALK_RIGHT"]))
        self.control3.configure(text=pygame.key.name(saves.controls["JUMP"]))
        self.control4.configure(text=pygame.key.name(saves.controls["ACTION"]))
        self.control5.configure(text=pygame.key.name(saves.controls["CROUCH"]))


class Main:

    def __init__(self, fast_mode, small_mode):
        # Main Program

        if not pygame.font.get_init():
            pygame.font.init()

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
