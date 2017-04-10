import pygame


class SoundEngine:

    def __init__(self):

        self.light_sound_channel = pygame.mixer.Channel(0)
        self.dissolve_sound_channel = pygame.mixer.Channel(1)
        self.siren_sound_channel = pygame.mixer.Channel(2)
        self.footstep_sound_channel = pygame.mixer.Channel(3)
        self.fall_sound_channel = pygame.mixer.Channel(4)

        self.light_sound = pygame.mixer.Sound("resources/lights.wav")
        self.dissolve_sound = pygame.mixer.Sound("resources/dissolve.wav")
        self.siren_sound = pygame.mixer.Sound("resources/siren.wav")
        self.footstep_sound = pygame.mixer.Sound("resources/step.wav")
        self.fall_sound = pygame.mixer.Sound("resources/fall.wav")

        self.light_sound.set_volume(0)
        self.dissolve_sound.set_volume(0.2)

        self.channel_linkup = {self.light_sound: self.light_sound_channel,
                               self.dissolve_sound: self.dissolve_sound_channel,
                               self.siren_sound: self.siren_sound_channel,
                               self.footstep_sound: self.footstep_sound_channel,
                               self.fall_sound: self.fall_sound_channel}

        self.queued_sounds = []

    def play_sounds(self):

        # Plays all the queued sounds
        for sound in self.queued_sounds:

            self.channel_linkup[sound].play(sound[0], sound[1])

        self.queued_sounds = []
