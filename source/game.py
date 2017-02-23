import pygame
from pygame.locals import *

import constants
import player as p
import level
import guards
import torches
import covers
import entities
import leveltext
from spritesheet import blit_alpha
from funcs import pixel_perfect_collision
import sys


class Game:

    def __init__(self, display, clock):

        self.display = display
        self.clock = clock

        # Show the loading screen
        self.loading_screen = covers.LoadingScreen()

        for n in range(63):
            blit_alpha(self.display, self.loading_screen.image, (0, 0), n * 4)
            pygame.display.flip()

        # Create the loading label
        label = leveltext.LoadingLabel("", 300, 500)

        # Create the player
        self.player = p.Player()

        self.active_sprite_list = pygame.sprite.Group()
        self.active_sprite_list.add(self.player)

        # Create the levels
        self.level_list = list()

        label.update_text("Loading Level 1...", 480, 500)
        label.draw(self.display)
        pygame.display.flip()
        self.level_list.append(level.Level01(self.player, True))
        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 2...", 480, 500)
        label.draw(self.display)
        pygame.display.flip()
        self.level_list.append(level.Level02(self.player, True))
        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 3...", 480, 500)
        label.draw(self.display)
        pygame.display.flip()
        self.level_list.append(level.Level03(self.player, True))
        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 4...", 480, 500)
        label.draw(self.display)
        pygame.display.flip()
        self.level_list.append(level.Level04(self.player, True))

        # Set the current level
        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]

        self.player.level = self.current_level
        self.current_level.player = self.player

        # Create the blackout
        self.blackout = covers.Blackout()
        self.blackout.player = self.player

        self.crosshair = entities.Crosshair()

        self.light_sound = pygame.mixer.Sound("resources/lights.wav")
        self.light_sound.set_volume(0.15)

    def run(self):
        # Game loop

        # Load the music
        pygame.mixer.music.load("resources/music.mp3")
        pygame.mixer.music.set_volume(0.25)

        # Hide mouse pointer
        pygame.mouse.set_visible(False)

        # Reset scrolling
        self.current_level.reset_world()
        self.current_level.shift_world(self.current_level.start_x, self.current_level.start_y)

        # Set the players position
        self.player.rect.x = 48
        self.player.rect.y = 384

        # Variables to control the player
        run = 0
        jump = False
        crouch = False

        pause = 0
        reset = False

        has_guard = False
        for guard in self.current_level.guards.sprites():
            if isinstance(guard, guards.Guard):
                has_guard = True
        if has_guard:
            self.light_sound.play(-1)

        # Play the music
        pygame.mixer.music.play(-1)

        # Loop until the window is closed
        game_exit = False

        while not game_exit:
            for event in pygame.event.get():

                # If player closes window
                if event.type == QUIT:

                    pygame.mouse.set_visible(True)

                    pygame.quit()
                    sys.exit(0)

                elif event.type == KEYDOWN:

                    if event.key == K_ESCAPE:
                        game_exit = True

                    # Player controls
                    if event.key == K_LEFT or event.key == K_a:
                        run = -1
                    if event.key == K_RIGHT or event.key == K_d:
                        run = 1

                    if event.key == K_UP or event.key == K_w:
                        jump = True

                    # Use keypads
                    if event.key == K_SPACE:
                        self.player.use_keypad()

                    # Crouching
                    if event.key == K_LCTRL:
                        crouch = True

                elif event.type == KEYUP:

                    if event.key == K_LEFT or event.key == K_RIGHT:
                        run = 0

                    if event.key == K_a or event.key == K_d:
                        run = 0

                    if event.key == K_UP or event.key == K_w:
                        jump = False
                        self.player.climbing = False

                    if event.key == K_LCTRL:
                        crouch = False

            if pause > 0:
                pause -= 1

            if pause == 0 and reset:
                self.current_level.reset_world()
                self.current_level.set_scrolling()
                self.player.reset()
                reset = False

            # Level progression
            if self.player.rect.x + self.player.rect.width/2 >= constants.SCREEN_WIDTH:

                # Reset the player and move on the level
                self.current_level.reset_world()
                self.player.reset()

                self.light_sound.stop()

                self.current_level_no += 1
                if self.current_level_no >= len(self.level_list):
                    break
                else:
                    self.current_level = self.level_list[self.current_level_no]

                self.player.level = self.current_level
                self.current_level.player = self.player

                has_guard = False
                for guard in self.current_level.guards.sprites():
                    if isinstance(guard, guards.Guard):
                        has_guard = True
                if has_guard:
                    self.light_sound.play(-1)

            # Check if player has hit obstacles
            obstacle_hits = pygame.sprite.spritecollide(self.player, self.current_level.obstacle_list, False)
            if len(obstacle_hits):
                self.player.reset()
                self.current_level.reset_world()
                self.current_level.set_scrolling()

            if not pause:
                # Check if the guards got the players
                hit_list = pygame.sprite.spritecollide(self.player, self.current_level.entities, False)
                for hit in hit_list:
                    if isinstance(hit, torches.Torch):
                        if pixel_perfect_collision(self.player, hit):
                            pause = 120
                            reset = True

                            # Create an exclamation mark
                            self.current_level.entities.add(entities.ExclamationMark(hit.guard))

                # Playing running and jumping
                if abs(run) > 0:
                    if run == 1:
                        self.player.walk_right()
                    elif run == -1:
                        self.player.walk_left()

                if crouch:
                    self.player.do_crouch()
                else:
                    self.player.stop_crouching()

                if jump and not crouch:
                    self.player.jump()

                # Update entities
            self.active_sprite_list.update()
            if not pause:
                self.current_level.update()
            self.blackout.update()
            self.crosshair.update()

            # Scrolling
            if self.player.rect.x >= 624:
                diff = self.player.rect.x - 624
                if not self.current_level.at_edge_x:
                    self.player.rect.x = 624
                self.current_level.shift_world(-diff, 0)

            if self.player.rect.x <= 288:
                diff = self.player.rect.x - 288
                if not self.current_level.at_edge_x:
                    self.player.rect.x = 288
                self.current_level.shift_world(-diff, 0)

            if self.player.rect.y >= 454:
                diff = self.player.rect.y - 454
                if not self.current_level.at_edge_y:
                    self.player.rect.y = 454
                self.current_level.shift_world(0, diff)

            if self.player.rect.y <= 288:
                diff = self.player.rect.y - 288
                if not self.current_level.at_edge_y:
                    self.player.rect.y = 288
                self.current_level.shift_world(0, diff)

            # All drawing goes here
            self.current_level.draw(self.display)
            self.active_sprite_list.draw(self.display)
            self.blackout.draw(self.display)
            self.crosshair.draw(self.display)

            # Limit to 60 fps
            self.clock.tick(60)
            # Update the display
            pygame.display.flip()

        pygame.mixer.music.load("resources/menu_music.mp3")
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(-1)

        self.light_sound.stop()

        pygame.mouse.set_visible(True)
