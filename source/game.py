import pygame
from pygame.locals import *

import constants
import controls
import player as p
import level
import guards
import torches
import covers
import entities
import text
import hud
import spritesheet
import funcs
import sys


class Game:

    def __init__(self, parent):

        self.parent = parent

        self.display = self.parent.display
        self.clock = self.parent.clock

        self.fast = self.parent.parent.fast

        # Show the loading screen
        self.loading_screen = covers.LoadingScreen()
        if self.parent.parent.small:
            self.loading_screen.image = self.loading_screen.image_small
            loading_label_x = 360
            loading_label_y = 400
        else:
            loading_label_x = 480
            loading_label_y = 500

        for n in range(63):
            spritesheet.blit_alpha(self.display, self.loading_screen.image, (0, 0), n * 4)
            pygame.display.flip()

        # Create the loading label
        label = text.LoadingLabel("", 300, 500)

        # Create the player
        self.player = p.Player()

        self.active_sprite_list = pygame.sprite.Group()
        self.active_sprite_list.add(self.player)

        # Create the levels
        self.level_list = list()

        label.update_text("Loading Level 1...", loading_label_x, loading_label_y)
        label.draw(self.display)
        pygame.display.flip()
        # self.level_list.append(level.Level01(self.player, True, self.fast))

        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 2...", loading_label_x, loading_label_y)
        label.draw(self.display)
        pygame.display.flip()
        # self.level_list.append(level.Level02(self.player, True, self.fast))

        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 3...", loading_label_x, loading_label_y)
        label.draw(self.display)
        pygame.display.flip()
        # self.level_list.append(level.Level03(self.player, True, self.fast))

        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 4...", loading_label_x, loading_label_y)
        label.draw(self.display)
        pygame.display.flip()
        # self.level_list.append(level.Level04(self.player, True, self.fast))

        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 5...", loading_label_x, loading_label_y)
        label.draw(self.display)
        pygame.display.flip()
        # self.level_list.append(level.Level05(self.player, True, self.fast))

        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 6...", loading_label_x, loading_label_y)
        label.draw(self.display)
        pygame.display.flip()
        self.level_list.append(level.Level06(self.player, True, self.fast))

        # Set the current level
        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]

        self.player.level = self.current_level
        self.current_level.player = self.player

        # Create the blackout
        self.blackout = covers.Blackout()
        self.blackout.player = self.player

        # Create the game over screen
        self.game_over = covers.GameOverScreen()

        self.crosshair = entities.Crosshair()

        self.hud = hud.HUD(self.player, self.parent.parent.small)

        self.light_sound = pygame.mixer.Sound("resources/lights.wav")
        self.light_sound.set_volume(0.15)

        self.dissolve_sound = pygame.mixer.Sound("resources/dissolve.wav")
        self.dissolve_sound.set_volume(0.2)

    def run(self):
        # Game loop

        # A performance enhancement
        player = self.player

        # Load the music
        pygame.mixer.music.load("resources/music.mp3")
        pygame.mixer.music.set_volume(0.25)

        # Hide mouse pointer
        pygame.mouse.set_visible(False)

        # Reset scrolling
        self.current_level.reset_world()
        self.current_level.set_scrolling()

        # Set the players position
        player.rect.x = 48
        player.rect.y = 384

        # Variables to control the player
        run = 0
        jump = False
        crouch = False

        pause = 0
        reset = False
        progress = False
        do_reset = False

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
                    if event.key == controls.controls["WALK_LEFT"]:
                        run = -1
                    if event.key == controls.controls["WALK_RIGHT"]:
                        run = 1

                    if event.key == controls.controls["JUMP"]:
                        jump = True

                    # Use keypads
                    if event.key == controls.controls["ACTION"]:
                        player.use_keypad()

                    # Crouching
                    if event.key == controls.controls["CROUCH"]:
                        crouch = True

                elif event.type == KEYUP:

                    if event.key == controls.controls["WALK_LEFT"] and not run == 1:
                        run = 0

                    if event.key == controls.controls["WALK_RIGHT"] and not run == -1:
                        run = 0

                    if event.key == controls.controls["JUMP"]:
                        jump = False
                        player.climbing = False

                    if event.key == controls.controls["CROUCH"]:
                        crouch = False

            if pause > 0:
                pause -= 1

            # Level progression
            if player.rect.x + player.rect.width/2 >= constants.SCREEN_WIDTH and not progress:
                pause = 60
                progress = True

            if progress and not pause:

                # Reset the player and move on the level
                self.current_level.reset_world()
                player.reset()

                self.light_sound.stop()

                self.current_level_no += 1
                if self.current_level_no >= len(self.level_list):
                    break
                else:
                    self.current_level = self.level_list[self.current_level_no]

                player.level = self.current_level
                self.current_level.player = player

                has_guard = False
                for guard in self.current_level.guards.sprites():
                    if isinstance(guard, guards.Guard):
                        has_guard = True
                if has_guard:
                    self.light_sound.play(-1)

                progress = False

            # Check if player has hit obstacles
            obstacle_hits = pygame.sprite.spritecollide(player, self.current_level.obstacle_list, False)
            if len(obstacle_hits) and not player.dying:
                player.dying = True
                player.health = 0
                self.dissolve_sound.play()

            if pause == 0 and reset:
                do_reset = True

            elif not pause:
                # Check if the guards got the player
                hit_list = pygame.sprite.spritecollide(player, self.current_level.entities, False)
                for hit in hit_list:
                    if isinstance(hit, torches.Torch):
                        if funcs.pixel_perfect_collision(player.rect, player.hitmask, hit.rect, hit.hitmask):
                            pause = 180
                            reset = True

                            # Create an exclamation mark
                            self.current_level.entities.add(entities.ExclamationMark(hit.guard))

                hit_laser = []
                for laser in self.current_level.lasers:
                    hit_laser += [laser.test_collision()]

                if True in hit_laser:
                    pause = 180
                    reset = True

                # Playing running and jumping
                if abs(run) > 0:
                    if run == 1:
                        player.walk_right()
                    elif run == -1:
                        player.walk_left()

                if crouch:
                    player.do_crouch()
                else:
                    player.stop_crouching()

                if jump and not crouch:
                    player.jump()

            # Update entities
            self.active_sprite_list.update()
            if not pause:
                self.current_level.update()
            else:
                self.current_level.lasers.update()
            self.blackout.update()
            self.crosshair.update()
            self.hud.update()

            # Scrolling
            if player.rect.x >= constants.SCREEN_WIDTH - 288:
                diff = player.rect.x - (constants.SCREEN_WIDTH - 288)
                if not self.current_level.at_edge_x:
                    player.rect.x = constants.SCREEN_WIDTH - 288
                self.current_level.shift_world(-diff, 0)

            if player.rect.x <= 288:
                diff = player.rect.x - 288
                if not self.current_level.at_edge_x:
                    player.rect.x = 288
                self.current_level.shift_world(-diff, 0)

            if player.rect.y >= constants.SCREEN_HEIGHT - 240:
                diff = player.rect.y - (constants.SCREEN_HEIGHT - 240)
                if not self.current_level.at_edge_y:
                    player.rect.y = constants.SCREEN_HEIGHT - 240
                self.current_level.shift_world(0, diff)

            if player.rect.y <= 288:
                diff = player.rect.y - 288
                if not self.current_level.at_edge_y:
                    player.rect.y = 288
                self.current_level.shift_world(0, diff)

            if do_reset:
                self.current_level.reset_world()
                self.current_level.set_scrolling()
                player.reset()
                if player.crouching:
                    player.stop_crouching()
                    player.crouching = False
                reset = False
                do_reset = False

            if player.dying and player.death_progress >= 75:
                player.health = 100
                player.stamina = 100
                player.reset()
                self.current_level.reset_world()
                self.current_level.set_scrolling()

            # All drawing goes here
            self.current_level.draw(self.display)
            self.active_sprite_list.draw(self.display)
            self.blackout.draw(self.display)
            self.crosshair.draw(self.display)
            self.hud.draw(self.display)
            if reset and 0 < pause < 100:
                spritesheet.blit_alpha(self.display, self.game_over.image, (0, 0), abs(pause-100)*8)

            # Limit to 60 fps
            self.clock.tick(60)
            # Update the display
            pygame.display.flip()

        self.light_sound.stop()

        pygame.mixer.music.load("resources/menu_music.mp3")
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(-1)

        pygame.mouse.set_visible(True)
