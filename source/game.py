import pygame
from pygame.locals import *

# Import all of the different components of the game
import constants
import saves
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
import math
import sys


class Game:

    # This is the game class
    # This actually executes everything in the game

    def __init__(self, parent):

        # Assign some constant attributes

        self.parent = parent

        self.display = self.parent.display
        self.clock = self.parent.clock

        self.fast = self.parent.parent.fast
        self.controls = self.parent.parent.controls

        # Show the loading screen
        self.loading_screen = covers.LoadingScreen()
        if self.parent.parent.small:
            # Adjust the loading screen for the small display
            self.loading_screen.image = self.loading_screen.image_small
            loading_label_x = 360
            loading_label_y = 400
        else:
            loading_label_x = 480
            loading_label_y = 500

        # Fade in the loading screen
        for n in range(63):
            spritesheet.blit_alpha(self.display, self.loading_screen.image, (0, 0), n * 4)
            pygame.display.flip()

        # Create the loading label
        label = text.LoadingLabel("", 300, 500)

        # Create the player
        self.player = p.Player()

        # Create a group that contains only the player
        # This is so I can call .draw() on the group
        # and pygame will draw the sprite for me
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player)

        # Create the levels
        self.level_list = list()

        # For each level, update the text on the level
        # then draw the loading screen and text to the display
        # Then load the level into the level list
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
        self.level_list.append(level.Level03(self.player, True, self.fast))

        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 4...", loading_label_x, loading_label_y)
        label.draw(self.display)
        pygame.display.flip()
        self.level_list.append(level.Level04(self.player, True, self.fast))

        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 5...", loading_label_x, loading_label_y)
        label.draw(self.display)
        pygame.display.flip()
        self.level_list.append(level.Level05(self.player, True, self.fast))

        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 6...", loading_label_x, loading_label_y)
        label.draw(self.display)
        pygame.display.flip()
        self.level_list.append(level.Level06(self.player, True, self.fast))

        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 7...", loading_label_x, loading_label_y)
        label.draw(self.display)
        pygame.display.flip()
        self.level_list.append(level.Level07(self.player, True, self.fast))

        self.loading_screen.draw(self.display)
        label.update_text("Loading Level 8...", loading_label_x, loading_label_y)
        label.draw(self.display)
        pygame.display.flip()
        self.level_list.append(level.Level08(self.player, True, self.fast))

        # Set the current level
        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]

        # Assign references between objects
        self.player.level = self.current_level
        self.current_level.player = self.player

        # Create the blackout
        self.blackout = covers.Blackout()
        self.blackout.player = self.player

        # Create the game over screens
        # Again, if it's set to the small display
        # then use the small image
        self.game_over = covers.GameOverScreen()
        if self.parent.parent.small:
            self.game_over.image = self.game_over.image_small
        self.black_screen = covers.DarkScreen()

        # Using a custom image as the pointer
        # suits the theme a bit better than the mouse pointer
        self.crosshair = entities.Crosshair()

        # Instantiate the HUD
        self.hud = hud.HUD(self.player, self.parent.parent.small)

        # Load the sounds and mix the volumes
        self.light_sound = pygame.mixer.Sound("resources/lights.wav")
        self.light_sound.set_volume(0)

        self.dissolve_sound = pygame.mixer.Sound("resources/dissolve.wav")
        self.dissolve_sound.set_volume(0.2)

    def run(self, from_start=False):
        # Game loop

        # Load the players progress,
        # if they clicked continue.
        # Otherwise then start from the start
        if not from_start:
            self.current_level_no = saves.load("current_level")
        else:
            self.current_level_no = 0
        # Save the current level
        saves.save_data["current_level"] = self.current_level_no
        saves.save()

        # Load the current level
        self.current_level = self.level_list[self.current_level_no]
        self.player.level = self.current_level
        self.current_level.player = self.player

        # A performance enhancement
        # The more dots the longer it takes
        player = self.player

        # Load the music
        # Then mix the volumes
        pygame.mixer.music.load("resources/music.mp3")
        pygame.mixer.music.set_volume(0.75)

        # Hide mouse pointer
        pygame.mouse.set_visible(False)

        # Reset level by undo-ing all scrolling
        # Then scroll back to the start position
        # Finally reset any changes made to sprites in the level
        self.current_level.reset_objects()
        self.current_level.reset_world()
        self.current_level.set_scrolling()

        # Set the players position
        player.rect.x = 48
        player.rect.y = 384

        # Variables to control the player
        run = 0
        jump = False
        crouch = False

        # A variety of variables that are controlling whats going on
        pause = 0
        reset = False
        progress = False
        do_reset = False
        show_caught = False

        # If there are guards in the level then play the light sound
        if len([guard for guard in self.current_level.guards.sprites() if isinstance(guard, guards.Guard)]):
            self.light_sound.play(-1)

        # Play the music
        pygame.mixer.music.play(-1)

        # Loop until the window is closed
        game_exit = False

        # And here begins out game loop
        while not game_exit:

            # A generic style events loop
            for event in pygame.event.get():

                # If player closes window
                if event.type == QUIT:

                    # Show the mouse before quitting
                    pygame.mouse.set_visible(True)

                    # Exit pygame then quit the program
                    pygame.quit()
                    sys.exit(0)

                # If a key was pressed...
                elif event.type == KEYDOWN:

                    # Escape returns to menu by breaking the game loop
                    if event.key == K_ESCAPE:
                        game_exit = True

                    # Player controls

                    # Running left/right
                    if event.key == self.controls["WALK_LEFT"]:
                        run = -1
                    if event.key == self.controls["WALK_RIGHT"]:
                        run = 1

                    # Jumping
                    if event.key == self.controls["JUMP"]:
                        jump = True

                    # Use keypads
                    if event.key == self.controls["ACTION"]:
                        player.use_keypad()

                    # Crouching
                    if event.key == self.controls["CROUCH"]:
                        crouch = True

                # If a key was released...
                elif event.type == KEYUP:

                    # Stopping the player from running left
                    if event.key == self.controls["WALK_LEFT"] and not run == 1:
                        run = 0

                    # Stopping the player from running right
                    if event.key == self.controls["WALK_RIGHT"] and not run == -1:
                        run = 0

                    # Stops the player from jumping and climbing
                    if event.key == self.controls["JUMP"]:
                        jump = False
                        player.climbing = False

                    # And then stopping the playing from crouching
                    if event.key == self.controls["CROUCH"]:
                        crouch = False

            # Pause is a counter variable that stops the game
            # The higher pause is set to the longer the game will pause
            # Pause is often used when transitions are being made
            if pause > 0:
                pause -= 1

            # Level progression
            # If the player has reached the right side of the screen
            # Then pause the game, and say the game should progress onto the next level
            if player.rect.centerx - player.rect.width/4 >= constants.SCREEN_WIDTH and not progress:
                pause = 60
                progress = True

            if progress and pause == 30:

                # Reset the player and level
                self.current_level.reset_world()
                player.reset()

                # Stop any sounds that are playing
                self.light_sound.stop()

                # Save the progress to the save file
                # and set the new level, if the player hasn't finished the game
                # Otherwise return to the menu
                self.current_level_no += 1
                if self.current_level_no >= len(self.level_list):
                    self.current_level_no = 0
                    saves.save_data["current_level"] = 0
                    saves.save()
                    break
                else:
                    self.current_level = self.level_list[self.current_level_no]
                saves.save_data["current_level"] = self.current_level_no
                saves.save()

                # Assign references between objects
                player.level = self.current_level
                self.current_level.player = player

                # If there are guards in the level then play the light sound
                if len([guard for guard in self.current_level.guards.sprites() if isinstance(guard, guards.Guard)]):
                    self.light_sound.play(-1)

            # Once the progression has complete, set the progress var accordingly
            if progress and not pause:
                progress = False

            # Check if player has hit obstacles
            obstacle_hits = pygame.sprite.spritecollide(player, self.current_level.obstacle_list, False)
            if len(obstacle_hits) and not player.dying:
                # If the player has, then say the player is dying
                player.dying = True
                player.health = 0
                self.dissolve_sound.play()

            # This tells the game that it needs to reset the level
            if pause < 50 and reset:
                do_reset = True

            # These are things that should only happen when the game is not paused
            elif not pause:

                # Check if the guards got the player
                hit_list = pygame.sprite.spritecollide(player, self.current_level.entities, False)
                for hit in hit_list:
                    if isinstance(hit, torches.Torch):

                        # Due to the conical shape of the torchlight, we need to do pixel perfect collision here
                        # otherwise it would be really easy to 'hit' a torch when you haven't really

                        if funcs.pixel_perfect_collision(player.rect, player.hitmask, hit.rect, hit.hitmask):
                            pause = 180
                            reset = True

                            # Create an exclamation mark
                            # Nice addition that easily lets the player know which guard caught them
                            self.current_level.entities.add(entities.ExclamationMark(hit.guard))

                # Using a generator, create a list of booleans reporting if the laser is touching the player
                hit_laser = [laser.test_collision() for laser in self.current_level.lasers]
                if True in hit_laser:
                    # If the player did get caught,
                    # then pause the game and tell the level it needs to reset
                    pause = 180
                    reset = True

                # Player movement

                # First check if the player should actually move
                if run != 0 and not player.dying:
                    # Then check which direction the player needs to run in
                    # and move the player in that direction
                    if run == 1:
                        player.walk_right()
                    elif run == -1:
                        player.walk_left()

                # If the should crouch, then make the player crouch
                # otherwise stop the player from crouching
                if crouch:
                    player.do_crouch()
                else:
                    player.stop_crouching()

                # Don't allow the player to jump when crouching
                if jump:
                    player.jump()

            # Update entities

            # Don't update the player when the games progressing
            if not progress:
                self.player_group.update()
            else:
                # Sometimes the player can get stuck in running pose
                # after it hits the right side of the screen
                # so here's a quick fix to that
                player.image = player.stand_image_r
            if not pause:
                # Don't update the level when the games paused
                self.current_level.update()
            else:
                # Lasers still need updated however to correct their position
                self.current_level.lasers.update()
            # There's no special cases for the rest of the sprites
            self.blackout.update()
            self.crosshair.update()
            self.hud.update()

            # Volume controls for the guards' light
            if self.light_sound.get_num_channels():
                # Find nearest guard
                # This is done by generating a list of the distances to each guard
                # calculated using Pythagoras' theorem.
                # This list is then sorted, so the zeroth item of the list would
                # be the distance to the nearest guard.
                nearest_guard = [int(math.pow((math.pow(x.rect.x - player.rect.x, 2)) +
                                              (math.pow(x.rect.y - player.rect.y, 2)), 0.5))
                                 for x in self.current_level.guards.sprites()]
                nearest_guard.sort()

                # Stops a special case where being very far away from all
                # guards means that the sound can still be loud
                if nearest_guard[0]-250 < 0:
                    # And then set the volume relative to the distance to the nearest guard
                    self.light_sound.set_volume(abs(nearest_guard[0]-250)/400)
                else:
                    self.light_sound.set_volume(0)

            # Scrolling in all 4 directions

            # Only scroll when the player is nearing the edge of the screen
            if player.rect.x >= constants.SCREEN_WIDTH - 288:
                # Calculate how far past the point of scrolling the player is
                diff = player.rect.x - (constants.SCREEN_WIDTH - 288)

                # If the level has reached its limit of scrolling then allow the player to move
                # otherwise the player wouldn't be able to get right up to the edges of the level
                if not self.current_level.at_edge_x:
                    player.rect.x = constants.SCREEN_WIDTH - 288

                # Then finally shift the level in the opposite direction of where the player moved
                self.current_level.shift_world(-diff, 0)

            # Repeat this again for the other direction
            if player.rect.x <= 288:
                diff = player.rect.x - 288
                if not self.current_level.at_edge_x:
                    player.rect.x = 288
                self.current_level.shift_world(-diff, 0)

            # Again it's a similar thing on the y axis,
            # but it's inverted since the y axis is flipped
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

            # If the game is paused, and the level is resetting,
            # then show the 'game over' screen
            if reset and pause > 0:
                show_caught = True

            # And once the level has reset, hide the game over screen
            if show_caught and pause == 0:
                show_caught = False

            # Resetting the level
            if do_reset:
                # Start by resetting the objects in the level,
                # such as keypads and doors.
                # Then reset the scrolling back to the start position of the level.
                self.current_level.reset_objects()
                self.current_level.reset_world()
                self.current_level.set_scrolling()

                # Reset the player
                # If the player is crouching, then stop the player from crouching
                player.reset()
                if player.crouching:
                    player.stop_crouching()
                    player.crouching = False

                # And tell the game that the level has reset
                reset = False
                do_reset = False

            # And now a similar procedure when the player dies
            if (player.dying and player.death_progress == 40) != player.health <= 0:
                # Reset the players health and stamina
                player.health = 100
                player.stamina = 100

                # Then again reset the level and player
                self.current_level.reset_objects()
                self.current_level.reset_world()
                self.current_level.set_scrolling()
                player.reset()

            # Stop the player from dying once it's dead
            if player.dying and player.death_progress >= 75:
                player.dying = False
                player.death_progress = 0

            # All drawing goes here
            # Start by drawing the level, then on top of that the player
            # then the various other things on top of that
            self.current_level.draw(self.display)
            self.player_group.draw(self.display)
            self.blackout.draw(self.display)
            self.crosshair.draw(self.display)
            self.hud.draw(self.display)

            # Draw covers when player is caught/dies
            # there are certain periods where these covers fade in/out
            # Which makes the transition look a lot smoother than
            # simply appearing then disappearing.
            # During these periods the transparency needs to increase/decrease

            # First of all the 'player was caught' screen
            if show_caught and 67 < pause < 100:
                spritesheet.blit_alpha(self.display, self.game_over.image, (0, 0), abs(pause-100)*8)
            elif show_caught and 0 < pause < 17:
                spritesheet.blit_alpha(self.display, self.game_over.image, (0, 0), pause*16)
            elif show_caught and 16 < pause < 68:
                self.display.blit(self.game_over.image, (0, 0))

            # Then just a dark screen when the player dies
            if player.dying and 16 < player.death_progress < 33:
                spritesheet.blit_alpha(self.display, self.black_screen.image, (0, 0), (player.death_progress-16)*16)
            elif player.dying and 32 < player.death_progress < 60:
                self.display.blit(self.black_screen.image, (0, 0))
            elif player.dying and 59 < player.death_progress < 76:
                spritesheet.blit_alpha(self.display, self.black_screen.image, (0, 0), abs(player.death_progress-75)*16)

            # And again a dark screen when the level is changing
            if progress and 43 < pause < 61:
                spritesheet.blit_alpha(self.display, self.black_screen.image, (0, 0), abs(pause-60)*16)
            elif progress and 16 < pause < 54:
                self.display.blit(self.black_screen.image, (0, 0))
            elif progress and 0 < pause < 17:
                spritesheet.blit_alpha(self.display, self.black_screen.image, (0, 0), pause*16)

            # Limit to 60 fps
            self.clock.tick(45)
            # Update the display
            pygame.display.flip()

        # Stop the light sound from playing once the game has finished
        self.light_sound.stop()

        # Start the menu music
        # before returning to the menu
        pygame.mixer.music.load("resources/menu_music.mp3")
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(-1)

        # Then show the mouse pointer
        pygame.mouse.set_visible(True)
