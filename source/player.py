import pygame

# Import the required components of the game
import spritesheet
import constants
import funcs
import entities


class Player(pygame.sprite.Sprite):

    # The player class has all of the attributes and methods
    # that allow the player to act as the player

    # Attributes

    # Set the players movement vector
    xv = 0
    yv = 0

    # The direction the player is pointing in
    # Used for calculating which direction to move in collisions
    # And what image to show
    direction = "R"

    # All the constants of the player
    # defining how the player will move
    speed = constants.PLAYER_SPEED
    gravity = constants.PLAYER_GRAVITY
    friction = constants.PLAYER_FRICTION
    jump_height = constants.PLAYER_JUMP_HEIGHT
    climb_speed = constants.PLAYER_CLIMB_SPEED

    # A reference to the level the player is currently in
    level = None

    # Methods
    def __init__(self, sound_engine):

        # Constructor

        # Call parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sound_engine = sound_engine

        # Load the sprite sheet to take all the images from
        sprite_sheet = spritesheet.SpriteSheet("resources/player.png")

        # Get the standing image
        # for the left-facing image, simply flip the right-facing one
        self.stand_image_r = sprite_sheet.get_image(0, 0, 24, 48)
        self.stand_image_l = pygame.transform.flip(self.stand_image_r, True, False)

        # Get the crouching image
        self.crouch_image_r = sprite_sheet.get_image(96, 0, 48, 24)
        self.crouch_image_l = pygame.transform.flip(self.crouch_image_r, True, False)

        # Arrays for animation
        self.walking_frames_r = []
        self.walking_frames_l = []

        # Load the images
        image = sprite_sheet.get_image(0, 0, 24, 48)
        self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(24, 0, 24, 48)
        self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(48, 0, 24, 48)
        self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(72, 0, 24, 48)
        self.walking_frames_r.append(image)

        # Flip them to the left
        for frame in self.walking_frames_r:
            image = pygame.transform.flip(frame, True, False)
            self.walking_frames_l.append(image)

        # Get the crouching animation
        self.crouching_frames_r = []
        self.crouching_frames_l = []

        self.crouching_frames_r.append(self.crouch_image_r)
        image = sprite_sheet.get_image(96, 24, 48, 24)
        self.crouching_frames_r.append(image)

        # Flip them
        for frame in self.crouching_frames_r:
            image = pygame.transform.flip(frame, True, False)
            self.crouching_frames_l.append(image)

        # Get the dissolve animation
        self.dissolve_frames_r = []
        self.dissolve_frames_l = []

        image = sprite_sheet.get_image(0, 48, 22, 48)
        self.dissolve_frames_r.append(image)
        image = sprite_sheet.get_image(22, 48, 20, 46)
        self.dissolve_frames_r.append(image)
        image = sprite_sheet.get_image(42, 48, 16, 34)
        self.dissolve_frames_r.append(image)
        image = sprite_sheet.get_image(58, 48, 14, 24)
        self.dissolve_frames_r.append(image)
        image = sprite_sheet.get_image(72, 48, 10, 14)
        self.dissolve_frames_r.append(image)
        image = sprite_sheet.get_image(82, 48, 6, 10)
        self.dissolve_frames_r.append(image)

        # Flip them
        for frame in self.dissolve_frames_r:
            image = pygame.transform.flip(frame, True, False)
            self.dissolve_frames_l.append(image)

        # Create an empty image for when the player needs to be hidden
        # For example when the player dissolves
        # there is a period when the player is not displayed
        self.empty_image = sprite_sheet.get_image(88, 48, 4, 4)

        # Set the starting image
        self.image = self.stand_image_r

        # Set a reference to the image rectangle
        self.rect = self.image.get_rect()

        # Create a hitmask
        # The hitmask is used for pixel-perfect collisions
        # and consists of a 2D array of boolean values
        # where 1 means that a pixel exists there
        # and 0 is empty space
        self.hitmask_stand = funcs.create_mask(self.stand_image_r)
        self.hitmask_crouch = funcs.create_mask(self.crouch_image_r)

        self.hitmask = self.hitmask_stand

        # Load the players sounds and mix the volumes
        self.footstep_sound = sound_engine.footstep_sound
        self.fall_sound = sound_engine.fall_sound
        self.jump_sound = sound_engine.jump_sound

        self.jump_sound.set_volume(0.40)

        # How far the player has walked without stopping
        # This is used for calculating what frame in the
        # animation to show
        self.walk_dist = 0

        # The players stats
        self.health = 100
        self.stamina = 100

        # Vars for controlling what the player is doing

        self.climbing = False
        self.touching_ladder = False
        self.touching_ground = False
        self.crouching = False

        # This is used to work out how much damage to deal the player
        # from falling from heights
        self.in_air = False
        self.air_time = 0

        self.dying = False
        self.death_progress = 0

    def update(self):

        # This runs the player death animation
        if self.dying:

            # Increase the progress into the death
            self.death_progress += 1

            if self.death_progress % 5 == 0 and self.death_progress < 30:
                # Keep track of where the player was
                old_center = self.rect.center

                # Then switch the image
                if self.direction == "R":
                    self.image = self.dissolve_frames_r[int(self.death_progress/5)]
                else:
                    self.image = self.dissolve_frames_l[int(self.death_progress/5)]
                # Update the rect and re-center the player
                self.rect = self.image.get_rect()
                self.rect.center = old_center

            # If the player has finished the animation
            # then just show an empty image
            elif self.death_progress == 30:
                self.image = self.empty_image

            # The player doesn't do anything else when dead, so just return
            return

        # Find out if the player is currently on a ladder
        self.touching_ladder = self.on_ladder()

        # Show the crouching image when the player is crouching
        if self.crouching:

            if self.direction == "R":
                self.image = self.crouch_image_r
            else:
                self.image = self.crouch_image_l

        # Calculate gravity
        if self.yv == 0:
            self.yv = 1

        # Slide down the ladder when not climbing up it
        elif self.touching_ladder and not self.climbing:
            self.yv = self.climb_speed
        else:
            # Otherwise just fall at the normal rate of gravity
            self.yv += self.gravity

            # Cap the potential downwards velocity as
            # the scrolling can't keep up if the
            # player gets too fast
            if self.yv >= 15:
                self.yv = 15

        # Stop the player from falling off the bottom of the screen
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.yv >= 0:
            self.yv = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

        # Momentum

        # The player slows down at a rate
        # relative to it's friction
        self.xv *= self.friction

        # If the player isn't moving
        # then reset the walk_dist
        if abs(self.xv) <= 0.1:
            self.xv = 0
            self.walk_dist = 0
        # Otherwise increase the walk_dist
        # and decrease the stamina
        else:
            self.walk_dist += 1
            self.stamina -= 0.008

        # Move left/right
        self.rect.x += self.xv

        # Display the players running animation
        # Or crouching animation of the player is crouching
        if self.crouching:
            if self.xv != 0:
                if self.direction == "R":
                    frame = self.walk_dist // 7 % len(self.crouching_frames_r)
                    self.image = self.crouching_frames_r[frame]
                else:
                    frame = self.walk_dist // 7 % len(self.crouching_frames_l)
                    self.image = self.crouching_frames_l[frame]
        else:
            if self.direction == "R":
                frame = self.walk_dist // 7 % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            else:
                frame = self.walk_dist // 7 % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]

        # Play the footstep sound every so often
        # but make sure that the player is both walking and on the ground
        if int(self.walk_dist) % 15 == 0 and not self.walk_dist == 0 and self.on_ground():
            self.sound_engine.que_sound([self.footstep_sound, 0])

        # If not running or crouching then show the standing image
        if self.xv == 0 and not self.crouching:
            if self.direction == "R":
                self.image = self.stand_image_r
            else:
                self.image = self.stand_image_l

        # Check for collisions on the x axis
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If the player is moving right
            # then set the right of the player to the left of collision
            if self.xv > 0:
                self.rect.right = block.rect.left
            # and if the player is moving left
            # then set the left of the player to the right of the collision
            elif self.xv < 0:
                self.rect.left = block.rect.right

            # And then  the walking distance
            self.walk_dist = 0

        # So the player can't walk off the left side of the screen
        if self.rect.x <= 0:
            self.rect.x = 0
            self.xv = 0
            self.walk_dist = 0

        # Move up/down
        self.rect.y += self.yv

        # Check for collisions of the y axis
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If the player is moving down
            # then set the bottom of the player to the top of the collision
            if self.yv > 0:
                self.rect.bottom = block.rect.top
            # and if the player is moving up
            # then set the top of the player to the bottom of the collision
            elif self.yv < 0:
                self.rect.top = block.rect.bottom

            # Stop vertical movement
            self.yv = 0

        # So the player can't jump off the top of the screen
        if self.rect.y + self.rect.height <= 0:
            self.rect.y = 0 - self.rect.height
            self.yv = 0

        # Saves having to call the same functions twice
        self.touching_ladder = self.on_ladder()
        self.touching_ground = self.on_ground()

        # If the player is not on the ground, or on a ladder
        # then it must be in the air
        if not (self.touching_ground or self.touching_ladder):
            self.in_air = True

        # Then once the player hits the ground
        if (self.touching_ground or self.touching_ladder) and self.in_air:
            # If the player has been in the air for more than a certain threshold of time
            if self.air_time > 45:
                # Play the impact sound and deal the player damage
                self.sound_engine.que_sound([self.fall_sound, 0])
                self.health -= self.air_time / 7.5
            # Since the player is no longer on the ground, tell the game such
            self.in_air = False
            self.air_time = 0

        # Increase the counter for how long the player has been in the air
        if self.in_air:
            self.air_time += 1

        # Player slowly regains health and stamina
        if self.health < 100:
            self.health += 0.001

        if self.stamina < 100:
            self.stamina += 0.004

    def on_ground(self):

        # Helper function that returns whether the player is on the ground

        # It works by moving the player slightly down,
        # and checking if there is a platform there.
        # If there is, the player must be on the ground
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) or self.rect.bottom > constants.SCREEN_HEIGHT:
            return True
        else:
            return False

    def walk_right(self):

        # Moves the player right

        # Stamina has an effect on walking speed, as does crouching
        self.xv += (self.speed / 1.5) * ((self.stamina / 400) + 0.75) \
            if self.crouching or self.climbing else self.speed * ((self.stamina / 400) + 0.75)
        self.direction = "R"

    def walk_left(self):

        # Moves the player left

        # Stamina has an effect on walking speed, as does crouching
        self.xv -= (self.speed / 2) * ((self.stamina / 400) + 0.75) \
            if self.crouching or self.climbing else self.speed * ((self.stamina / 400) + 0.75)
        self.direction = "L"

    def jump(self):

        if self.touching_ladder:
            # If the player is on a ladder
            # then it will move upwards at its climbing speed
            self.yv = -self.climb_speed
            self.climbing = True

        elif self.on_ground():
            if not self.crouching:
                # otherwise move upwards at the players jump height
                self.yv = -self.jump_height
                self.sound_engine.que_sound([self.jump_sound, 0])

    def reset(self):

        if self.crouching:
            # If it can then reset the rect sizes
            self.crouching = False
            self.rect.width = 24
            self.rect.height = 48
            self.rect.y -= 24

            # Again the players position needs readjusted when facing left
            if self.direction == "L":
                self.rect.x += 24

            # And reset the hitmask to the standing one
            self.hitmask = self.hitmask_stand

        # Reset to the sprites original position and image
        self.image = self.stand_image_r
        self.hitmask = self.hitmask_stand
        self.rect = self.image.get_rect()
        self.rect.x = 48
        self.rect.y = 385
        self.xv = 0
        self.yv = 0
        self.direction = "R"
        self.in_air = False
        self.air_time = 0

    def use_keypad(self):

        # If the player is touching the keypad, increase the progress
        touching_keypads = pygame.sprite.spritecollide(self, self.level.keypads, False)
        for keypad in touching_keypads:
            if keypad.progress < 10:
                keypad.progress += 1

        # Bombs too
        touching_bombs = pygame.sprite.spritecollide(self, self.level.bombs, False)
        for bomb in touching_bombs:
            if bomb.progress < 10:
                bomb.progress += 1

        # Placing bombs

        # Here we first gather a list of all the bombs that haven't been placed
        # Then find those of which we are touching
        # And the ones that we are touching we set the placed variable to True
        non_placed_bombs = pygame.sprite.Group([n for n in self.level.non_draw if isinstance(n, entities.Bomb)])
        bombs_to_place = pygame.sprite.spritecollide(self, non_placed_bombs, False)
        for bomb in bombs_to_place:
            bomb.placed = True
        # We empty this group to stop a build-up of sprites
        non_placed_bombs.empty()

    def on_ladder(self):

        # Check if the player is touching a ladder
        # This is done simply by taking a collision test against the ladders group in the level
        ladder_hit_list = pygame.sprite.spritecollide(self, self.level.ladders, False)

        # Return true if at least one ladder was hit
        return True if len(ladder_hit_list) else False

    def at_wall(self, direction):

        # Checks if the player is at a wall
        # Direction is +1 for right, -1 for left

        # Moves the player horizontally by one tile and checks if there is a platform there
        self.rect.x += 24 * direction
        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.x -= 24 * direction

        # if there is then return true
        return True if len(hit_list) else False

    def do_crouch(self):

        # Bools holding whether the playing is at a wall in each direction
        at_wall_l = False
        at_wall_r = False

        # Checks to make sure that the player is on the ground and not on a ladder
        if self.on_ground() and not self.climbing:

            # Check the player isn't at a wall
            if self.direction == "R":
                at_wall_r = self.at_wall(1)
            else:
                at_wall_l = self.at_wall(-1)

            # Here we use an (<> xor <>) or not (<> or <>) gate
            # This means that one or the other returns true,
            # neither of them returns true,
            # but both of them returns false
            if (at_wall_r != at_wall_l) or not(at_wall_r or at_wall_l):
                self.crouching = True
                # Adjust the players rect
                # Since the crouching image is low and wide
                # Rather than tall and thin
                if self.rect.height == 48:
                    self.rect.height = 24
                    self.rect.width = 48
                    self.rect.y += 24

                    # If the player is next to one wall, but not two
                    # then it can still crouch.
                    # It just needs to adjust its position.
                    if at_wall_r:
                        self.rect.x -= 24
                    elif at_wall_l:
                        self.rect.x += 24

                    # When the player is facing left it has to be moved left one tile
                    # so the player stays in the same place
                    if self.direction == "L":
                        self.rect.x -= 24

                    # Use the new hitmask
                    # Since the images are so different a new hitmask has to be used here
                    self.hitmask = self.hitmask_crouch

    def stop_crouching(self):

        # Check first if the player can stand
        if self.can_stand():
            if self.rect.height == 24:
                # If it can then reset the rect sizes
                self.crouching = False
                self.rect.width = 24
                self.rect.height = 48
                self.rect.y -= 24

                # Again the players position needs readjusted when facing left
                if self.direction == "L":
                    self.rect.x += 24

                # And reset the hitmask to the standing one
                self.hitmask = self.hitmask_stand

    def can_stand(self):

        # This checks if there is a roof directly above the player
        self.rect.y -= 24
        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y += 24

        # Returns False if there is a platform, because that means the player CAN'T stand
        return False if len(hit_list) else True
