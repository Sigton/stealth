import pygame
from pygame.locals import *

import constants
import player as p
import level
import torches
import covers


def main():
    # Main program

    # Initiate pygame
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.mixer.init()
    pygame.init()

    # Set the display size

    game_display = pygame.display.set_mode(constants.SIZE)

    # Used to manage update frequency
    clock = pygame.time.Clock()

    # Set the window caption
    pygame.display.set_caption("Stealth")

    # Create the player
    player = p.Player()

    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(player)

    # Create the levels
    level_list = list()
    #level_list.append(level.Level01(player))
    #level_list.append(level.Level02(player))
    #level_list.append(level.Level03(player))
    #level_list.append(level.Level04(player))
    level_list.append(level.Level05(player))
    level_list.append(level.Level06(player))
    level_list.append(level.Level07(player))
    level_list.append(level.Level08(player))
    level_list.append(level.Level09(player))
    level_list.append(level.Level10(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    player.level = current_level
    current_level.player = player

    # Create the blackout
    blackout = covers.Blackout()
    blackout.player = player

    # Set the players position
    player.rect.x = 48
    player.rect.y = 624

    # Variables to control the player
    run = 0
    jump = False

    pause = 0
    reset = False

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

            elif event.type == KEYUP:

                if (event.key == K_LEFT or event.key == K_a) and player.xv <= 0:
                    run = 0
                if (event.key == K_RIGHT or event.key == K_d) and player.xv >= 0:
                    run = 0

                if event.key == K_UP or event.key == K_w:
                    jump = False

        if pause > 0:
            pause -= 1

        if pause == 0 and reset:
            player.reset()
            reset = False

        # Level progression
        if player.rect.x + player.rect.width/2 >= constants.SCREEN_WIDTH:

            # Reset the player and move on the level
            player.reset()

            current_level_no += 1
            current_level = level_list[current_level_no]

            player.level = current_level
            current_level.player = player

        if not pause:
            # Check if the guards got the players
            hit_list = pygame.sprite.spritecollide(player, current_level.entities, False)
            for hit in hit_list:
                if isinstance(hit, torches.Torch):
                    pause = 120
                    reset = True

            # Playing running and jumping
            if abs(run) > 0:
                if run == 1:
                    player.walk_right()
                elif run == -1:
                    player.walk_left()

            if jump:
                player.jump()

            # Update entities
            active_sprite_list.update()
            current_level.update()
            blackout.update()

        # All drawing goes here
        current_level.draw(game_display)
        active_sprite_list.draw(game_display)
        blackout.draw(game_display)

        # Limit to 60 fps
        clock.tick(60)
        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
