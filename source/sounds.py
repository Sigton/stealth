import pygame


class SoundEngine:

    def __init__(self):

        self.light_sound_channel = pygame.mixer.Channel(8)
        self.dissolve_sound_channel = pygame.mixer.Channel(9)
        self.siren_sound_channel = pygame.mixer.Channel(10)
