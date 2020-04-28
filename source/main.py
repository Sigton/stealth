import pygame
from pygame.locals import *

# tkinter is used for the launcher GUI
import tkinter as tk

from src import menu as m
from src import constants, saves


# Initiate pygame
# Initiating the mixer first stops a glitch where audio is out of sync
pygame.mixer.pre_init(22050, -16, 1, 512)
pygame.mixer.init()
pygame.init()

# We need more channels than the default
# so set up some more
pygame.mixer.set_num_channels(16)


class LauncherApp(tk.Tk):

    # The launcher is used to allow users to select options for their game
    # It's a simple GUI created using the tkinter library

    # LauncherApp is a subclass of tk.Tk, a tkinter window

    def __init__(self, *args, **kwargs):

        # Call the parents constructor
        tk.Tk.__init__(self, *args, **kwargs)

        # Set the title and window size
        tk.Tk.wm_title(self, "Stealth Launcher")
        self.geometry("480x480")
        # Also disallow useres to resize the window
        self.resizable(0, 0)

        # Create a container frame to hold any content placed inside the window
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # Configure the containers grid
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Define an instance of the Launcher class to insert into the container frame
        frame = Launcher(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        # Raise this frame
        frame.tkraise()


class Launcher(tk.Frame):

    # Launcher is the actual content of the launcher
    # It is a subclass of tk.Frame, allowing it to be inserted into the window

    def __init__(self, parent, controller):

        # Call the parents constructor
        tk.Frame.__init__(self, parent)

        # Assign attributes from the input
        self.parent = parent
        self.controller = controller

        # These variables control launch settings
        # They are IntVar's so that they can be controlled by tk.Checkbutton
        self.fast = tk.IntVar()
        self.small = tk.IntVar()

        # This is the instance of the Main class
        # An instance is not created because we don't want the constructor to be ran yet
        self.game = None

        # Here the controls are loaded from the save file
        self.controls = saves.load("controls")

        # Create a nice big title to be placed at the top of the window
        self.title = tk.Label(self, text="Stealth", font=("Verdana", 20))
        self.title.place(x=240, y=20, anchor="center")

        # A sub-heading, telling users this section is about game config
        self.config_heading = tk.Label(self, text="Game Configuration", font=("Verdana", 12))
        self.config_heading.place(x=240, y=65, anchor="center")

        # A bit more in-depth explanation
        self.desc = tk.Label(self, text="Select the launch options you want.")
        self.desc.place(x=240, y=90, anchor="center")

        # This checkbutton controls whether the user wants to run the game in fast mode
        # A description of 'fast mode' is also created as a label
        self.button1 = tk.Checkbutton(self, text="Fast Mode", variable=self.fast)
        self.button1.place(x=50, y=120, anchor="w")
        self.label1 = tk.Label(self, text="Removes decorations for better performance.",
                               font="Helvetica 9 italic")
        self.label1.place(x=160, y=120, anchor="w")

        # Same thing again, but this time about small screen mode
        self.button2 = tk.Checkbutton(self, text="Small Screen", variable=self.small)
        self.button2.place(x=50, y=150, anchor="w")
        self.label2 = tk.Label(self, text="Smaller window for smaller or lower resolution monitors.",
                               font="Helvetica 9 italic")
        self.label2.place(x=160, y=150, anchor="w")

        # Another sub-heading for control config
        self.controls_heading = tk.Label(self, text="Control Configuration", font=("Verdana", 12))
        self.controls_heading.place(x=240, y=200, anchor="center")

        # Here are quite a few similar blocks of code
        # Each one shows what key each control is set to,
        # with a button allowing users to change what key they want to use.

        self.control1_label = tk.Label(self, text="Walk Left Button:")
        self.control1_label.place(x=50, y=240, anchor="w")
        self.control1 = tk.Label(self, text=pygame.key.name(self.controls["WALK_LEFT"]))
        self.control1.place(x=160, y=240, anchor="w")
        self.control1_button = tk.Button(self, text="Change",
                                         command=lambda: self.set_control("WALK_LEFT"))
        self.control1_button.place(x=230, y=240, anchor="w")

        self.control2_label = tk.Label(self, text="Walk Right Button:")
        self.control2_label.place(x=50, y=270, anchor="w")
        self.control2 = tk.Label(self, text=pygame.key.name(self.controls["WALK_RIGHT"]))
        self.control2.place(x=160, y=270, anchor="w")
        self.control2_button = tk.Button(self, text="Change",
                                         command=lambda: self.set_control("WALK_RIGHT"))
        self.control2_button.place(x=230, y=270, anchor="w")

        self.control3_label = tk.Label(self, text="Jump Button:")
        self.control3_label.place(x=50, y=300, anchor="w")
        self.control3 = tk.Label(self, text=pygame.key.name(self.controls["JUMP"]))
        self.control3.place(x=160, y=300, anchor="w")
        self.control3_button = tk.Button(self, text="Change",
                                         command=lambda: self.set_control("JUMP"))
        self.control3_button.place(x=230, y=300, anchor="w")

        self.control4_label = tk.Label(self, text="Action Button:")
        self.control4_label.place(x=50, y=330, anchor="w")
        self.control4 = tk.Label(self, text=pygame.key.name(self.controls["ACTION"]))
        self.control4.place(x=160, y=330, anchor="w")
        self.control4_button = tk.Button(self, text="Change",
                                         command=lambda: self.set_control("ACTION"))
        self.control4_button.place(x=230, y=330, anchor="w")

        self.control5_label = tk.Label(self, text="Crouch Button:")
        self.control5_label.place(x=50, y=360, anchor="w")
        self.control5 = tk.Label(self, text=pygame.key.name(self.controls["CROUCH"]))
        self.control5.place(x=160, y=360, anchor="w")
        self.control5_button = tk.Button(self, text="Change",
                                         command=lambda: self.set_control("CROUCH"))
        self.control5_button.place(x=230, y=360, anchor="w")

        self.control6_label = tk.Label(self, text="Restart Button:")
        self.control6_label.place(x=50, y=390, anchor="w")
        self.control6 = tk.Label(self, text=pygame.key.name(self.controls["RESTART"]))
        self.control6.place(x=160, y=390, anchor="w")
        self.control6_button = tk.Button(self, text="Change",
                                         command=lambda: self.set_control("RESTART"))
        self.control6_button.place(x=230, y=390, anchor="w")

        # The save controls button writes the controls currently selected to the save file,
        # if the user wants to use the same control setup the next time they play
        self.save_controls_button = tk.Button(self, text="Set as default", command=self.save_controls, width="11")
        self.save_controls_button.place(x=350, y=300, anchor="w")

        # The reset controls button sets all the controls back to the very original control layout
        self.reset_controls_button = tk.Button(self, text="Reset controls", command=self.reset_controls, width="11")
        self.reset_controls_button.place(x=350, y=330, anchor="w")

        # The launch button starts the game with the users selected configuration
        self.launch_button = tk.Button(self, text="Launch", width="20", height="2",
                                       bg="#bbb", activebackground="#ccc", command=self.launch)
        self.launch_button.place(x=240, y=440, anchor="center")

        # Call the update controls to make sure everything is definitely up-to-date
        self.update_controls()

    def launch(self):

        # Runs the game

        # Make sure no keys are assigned to more than one control
        # First create a list off each key
        # Then another list of booleans of whether each key appears more than once
        controls = [self.controls[n] for n in self.controls]
        duplicates = [bool(controls.count(self.controls[n])-1) for n in self.controls]

        # If a key occurred more than once
        if True in duplicates:
            # then create a popup
            Popup("You have multiple controls\nassigned to the same key!")
        else:
            # Otherwise start the game

            # Create in instance of main, using the launch parameters chosen by the user
            self.game = Main(bool(self.fast.get()), bool(self.small.get()), self.controls)
            # Close the launcher, then run the game
            self.controller.destroy()
            self.game.run()

    def set_control(self, control):

        # Allows user to assign their chosen key to a control

        # Remove any existing binding, then bind the get_key function to any key press
        self.controller.unbind("<KeyPress>")
        self.controller.bind("<KeyPress>", lambda event, c=control: self.get_key(event, c))

    def get_key(self, event, control):

        # Gets the key code of the key the user just pressed

        # As tkinter uses different keycodes than pygame, they have to be translated.
        # trans_dict solves any discrepancies between the two modules' keycodes
        if event.keycode in saves.trans_dict:
            code = saves.trans_dict[event.keycode]
        else:
            code = event.keycode
        # Assign the control to the new keycode,
        # then update the labels and unbind the function

        if code == 271:
            Popup("Controls cannot be\nassigned to enter!")
            self.controller.unbind("<KeyPress>")
            return

        self.controls[control] = code
        self.update_controls()
        self.controller.unbind("<KeyPress>")

    def update_controls(self):
        # Updates the name of the key shown after a control has been updated
        self.control1.configure(text=(pygame.key.name(self.controls["WALK_LEFT"])).upper())
        self.control2.configure(text=(pygame.key.name(self.controls["WALK_RIGHT"])).upper())
        self.control3.configure(text=(pygame.key.name(self.controls["JUMP"])).upper())
        self.control4.configure(text=(pygame.key.name(self.controls["ACTION"])).upper())
        self.control5.configure(text=(pygame.key.name(self.controls["CROUCH"])).upper())
        self.control6.configure(text=(pygame.key.name(self.controls["RESTART"])).upper())

        # Any controls that are bound to the same key show in red

        # Get a list of all the key bindings
        controls = [self.controls[n] for n in self.controls]

        # Then for each control if the same key occurs more than once,
        # color the label red
        if controls.count(self.controls["WALK_LEFT"]) > 1:
            self.control1.configure(fg="red")
        else:
            self.control1.configure(fg="black")
        if controls.count(self.controls["WALK_RIGHT"]) > 1:
            self.control2.configure(fg="red")
        else:
            self.control2.configure(fg="black")
        if controls.count(self.controls["JUMP"]) > 1:
            self.control3.configure(fg="red")
        else:
            self.control3.configure(fg="black")
        if controls.count(self.controls["ACTION"]) > 1:
            self.control4.configure(fg="red")
        else:
            self.control4.configure(fg="black")
        if controls.count(self.controls["CROUCH"]) > 1:
            self.control5.configure(fg="red")
        else:
            self.control5.configure(fg="black")
        if controls.count(self.controls["RESTART"]) > 1:
            self.control6.configure(fg="red")
        else:
            self.control6.configure(fg="black")

    def save_controls(self):

        # Writes the controls to the save file
        saves.save_data["controls"] = self.controls
        saves.save()

    def reset_controls(self):

        # Loads the default controls
        self.controls = saves.default_controls
        self.update_controls()


class Popup(tk.Toplevel):

    # A simple subclass of tk.TopLevel
    # that serves as a popup message
    # to tell users not to have more than one control assigned to the same key

    def __init__(self, message):

        # Call the parents constructor
        tk.Toplevel.__init__(self)

        # Set the size of the popup
        self.geometry("200x150")

        # Create the text and add it to the TopLevel
        self.text = tk.Label(self, text=message)
        self.text.place(x=100, y=50, anchor="center")

        # Then a button to close the widget
        self.close_button = tk.Button(self, text="Dismiss", command=self.destroy, width=12, height=2)
        self.close_button.place(x=100, y=110, anchor="center")


class Main:

    # This class simply starts the game from running
    # It does tasks such as creating the window

    def __init__(self, fast_mode, small_mode, controls):
        # Main Program

        # There seemed to be a problem where the font module would fail to initialize when pygame.init was called
        if not pygame.font.get_init():
            pygame.font.init()

        # Create the display
        self.game_display = pygame.display.set_mode(constants.SIZE)

        # Set the window caption and icon
        pygame.display.set_caption("Stealth")

        icon_img = pygame.image.load("src/resources/icon.ico")

        icon = pygame.Surface([32, 32], flags=SRCALPHA)
        icon = icon.convert_alpha()
        icon.blit(icon_img, (0, 0))
        pygame.display.set_icon(icon)

        # Used to manage update frequency
        self.clock = pygame.time.Clock()

        # Set attributes of the input given
        self.fast = fast_mode
        self.small = small_mode
        self.controls = controls

    def run(self):

        # Runs the menu
        # Creates an instance of menu, then runs it

        # Start the menu
        menu = m.Menu(self)
        menu.run()

        # Once the game has finished running
        # Quit the game
        pygame.quit()

    def set_screen_size(self, new_width, new_height):

        # Sets the screen size of the display to the new width and height given
        self.game_display = pygame.display.set_mode(constants.set_screen_size(new_width, new_height))

        # It then returns a reference to the re-sized surface
        return self.game_display


if __name__ == "__main__":
    # Open the launcher
    launcher = LauncherApp()
    launcher.mainloop()
