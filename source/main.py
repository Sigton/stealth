import pygame
from pygame.locals import *

import constants
import player as p
import level
import guards
import torches
import covers
import entities
from spritesheet import blit_alpha
from funcs import pixel_perfect_collision


def main():
    # Main program

    # Initiate pygame
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.mixer.init()
    pygame.init()

    # Set the display size
    game_display = pygame.display.set_mode(constants.SIZE)

    # Hide the mouse
    pygame.mouse.set_visible(False)

    # Set the window caption and icon
    pygame.display.set_caption("Stealth")

    icon_img = pygame.image.load("resources/icon.ico")

    icon = pygame.Surface([32, 32], flags=SRCALPHA)
    icon = icon.convert_alpha()
    icon.blit(icon_img, (0, 0))
    pygame.display.set_icon(icon)

    # Show the loading screen
    loading_screen = covers.LoadingScreen()

    for n in range(63):
        blit_alpha(game_display, loading_screen.image, (0, 0), n*4)
        pygame.display.flip()

    # Load the music
    pygame.mixer.music.load("resources/music.mp3")
    pygame.mixer.music.set_volume(0.25)

    # Used to manage update frequency
    clock = pygame.time.Clock()

    # Create the player
    player = p.Player()

    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(player)

    # Create the levels
    level_list = list()

    level_list.append(level.Level01(player))
    level_list.append(level.Level02(player))
    level_list.append(level.Level03(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    player.level = current_level
    current_level.player = player

    # Create the blackout
    blackout = covers.Blackout()
    blackout.player = player

    crosshair = entities.Crosshair()

    # Set the players position
    player.rect.x = 48
    player.rect.y = 384

    # Variables to control the player
    run = 0
    jump = False
    crouch = False

    pause = 0
    reset = False

    light_sound = pygame.mixer.Sound("resources/lights.wav")
    light_sound.set_volume(0.15)

    has_guard = False
    for guard in current_level.guards.sprites():
        if isinstance(guard, guards.Guard):
            has_guard = True
    if has_guard:
        light_sound.play(-1)

    # Play the music
    pygame.mixer.music.play(-1)

    # Loop until the window is closed
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():

            # If player closes window
            if event.type == QUIT:
                game_exit = True

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
                    player.use_keypad()

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
                    player.climbing = False

                if event.key == K_LCTRL:
                    crouch = False

        if pause > 0:
            pause -= 1

        if pause == 0 and reset:
            current_level.reset_world()
            current_level.set_scrolling()
            player.reset()
            reset = False

        # Level progression
        if player.rect.x + player.rect.width/2 >= constants.SCREEN_WIDTH:

            # Reset the player and move on the level
            current_level.reset_world()
            player.reset()

            light_sound.stop()

            current_level_no += 1
            if current_level_no >= len(level_list):
                break
            else:
                current_level = level_list[current_level_no]

            player.level = current_level
            current_level.player = player

            has_guard = False
            for guard in current_level.guards.sprites():
                if isinstance(guard, guards.Guard):
                    has_guard = True
            if has_guard:
                light_sound.play(-1)

        # Check if player has hit obstacles
        obstacle_hits = pygame.sprite.spritecollide(player, current_level.obstacle_list, False)
        if len(obstacle_hits):
            player.reset()
            current_level.reset_world()
            current_level.set_scrolling()

        if not pause:
            # Check if the guards got the players
            hit_list = pygame.sprite.spritecollide(player, current_level.entities, False)
            for hit in hit_list:
                if isinstance(hit, torches.Torch):
                    if pixel_perfect_collision(player, hit):
                        pause = 120
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
        active_sprite_list.update()
        if not pause:
            current_level.update()
        blackout.update()
        crosshair.update()

        # Scrolling
        if player.rect.x >= 624:
            diff = player.rect.x - 624
            if not current_level.at_edge_x:
                player.rect.x = 624
            current_level.shift_world(-diff, 0)

        if player.rect.x <= 288:
            diff = player.rect.x - 288
            if not current_level.at_edge_x:
                player.rect.x = 288
            current_level.shift_world(-diff, 0)

        if player.rect.y >= 454:
            diff = player.rect.y - 454
            if not current_level.at_edge_y:
                player.rect.y = 454
            current_level.shift_world(0, diff)

        if player.rect.y <= 288:
            diff = player.rect.y - 288
            if not current_level.at_edge_y:
                player.rect.y = 288
            current_level.shift_world(0, diff)

        # All drawing goes here
        current_level.draw(game_display)
        active_sprite_list.draw(game_display)
        blackout.draw(game_display)
        crosshair.draw(game_display)

        # Limit to 60 fps
        clock.tick(60)
        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.mouse.set_visible(True)
    pygame.quit()
    quit()
