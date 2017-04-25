import pygame

# This deals with the loading and playing of sounds
# Each sound has it's own channel so that we don't
# any problems where there isn't a channel available
# for the sound to play on.


class SoundEngine:

    def __init__(self):

        # Create a channel for each sound
        self.light_sound_channel = pygame.mixer.Channel(0)
        self.dissolve_sound_channel = pygame.mixer.Channel(1)
        self.siren_sound_channel = pygame.mixer.Channel(2)
        self.footstep_sound_channel = pygame.mixer.Channel(3)
        self.fall_sound_channel = pygame.mixer.Channel(4)
        self.beep_sound_channel = pygame.mixer.Channel(5)
        self.gunshot_sound_channel = pygame.mixer.Channel(6)
        self.hiss_sound_channel = pygame.mixer.Channel(7)
        self.shell_sound_channel = pygame.mixer.Channel(8)
        self.click_sound_channel = pygame.mixer.Channel(9)
        self.keypress_sound_channel = pygame.mixer.Channel(10)
        self.explosion_sound_channel = pygame.mixer.Channel(11)
        self.jump_sound_channel = pygame.mixer.Channel(12)

        # Load all the sounds
        self.light_sound = pygame.mixer.Sound("resources/lights.wav")
        self.dissolve_sound = pygame.mixer.Sound("resources/dissolve.wav")
        self.siren_sound = pygame.mixer.Sound("resources/siren.wav")
        self.footstep_sound = pygame.mixer.Sound("resources/step.wav")
        self.fall_sound = pygame.mixer.Sound("resources/fall.wav")
        self.beep_sound = pygame.mixer.Sound("resources/beep.wav")
        self.gunshot_sound = pygame.mixer.Sound("resources/gunshot.wav")
        self.hiss_sound = pygame.mixer.Sound("resources/hiss.wav")
        self.shell_sound = pygame.mixer.Sound("resources/shelldrop.wav")
        self.click_sound = pygame.mixer.Sound("resources/click.wav")
        self.keypress_sound = pygame.mixer.Sound("resources/click.wav")
        self.explosion_sound = pygame.mixer.Sound("resources/explosion.wav")
        self.jump_sound = pygame.mixer.Sound("resources/jump.wav")

        # Link the sounds to the channels they should play in
        self.channel_linkup = {self.light_sound: self.light_sound_channel,
                               self.dissolve_sound: self.dissolve_sound_channel,
                               self.siren_sound: self.siren_sound_channel,
                               self.footstep_sound: self.footstep_sound_channel,
                               self.fall_sound: self.fall_sound_channel,
                               self.beep_sound: self.beep_sound_channel,
                               self.gunshot_sound: self.gunshot_sound_channel,
                               self.hiss_sound: self.hiss_sound_channel,
                               self.shell_sound: self.shell_sound_channel,
                               self.click_sound: self.click_sound_channel,
                               self.keypress_sound: self.keypress_sound_channel,
                               self.explosion_sound: self.explosion_sound_channel,
                               self.jump_sound: self.jump_sound_channel}

        # This is all the sounds that need to be played
        self.queued_sounds = []

    def play_sounds(self):

        # Plays all the queued sounds
        [self.channel_linkup[sound[0]].play(sound[0], sound[1]) for sound in self.queued_sounds]
        # And empty the que
        self.queued_sounds = []

    def que_sound(self, sound):
        # Add a sound to the que
        self.queued_sounds += [sound]
