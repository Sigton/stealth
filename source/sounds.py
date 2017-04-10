import pygame


class SoundEngine:

    def __init__(self):

        self.light_sound_channel = pygame.mixer.Channel(8)
        self.dissolve_sound_channel = pygame.mixer.Channel(9)
        self.siren_sound_channel = pygame.mixer.Channel(10)

        self.light_sound = pygame.mixer.Sound("resources/lights.wav")
        self.dissolve_sound = pygame.mixer.Sound("resources/dissolve.wav")
        self.siren_sound = pygame.mixer.Sound("resources/siren.wav")

        self.light_sound.set_volume(0)
        self.dissolve_sound.set_volume(0.2)

        self.channel_linkup = {self.light_sound: self.light_sound_channel,
                               self.dissolve_sound: self.dissolve_sound_channel,
                               self.siren_sound: self.siren_sound_channel}

        self.queued_sounds = []

    def play_sounds(self):

        # Plays all the queued sounds
        for sound in self.queued_sounds:

            self.channel_linkup[sound].play(sound[0], sound[1])

        self.queued_sounds = []
