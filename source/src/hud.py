import pygame

from src import spritesheet, text, constants, saves


class Label(text.Text):

    def __init__(self, texts, size, x, y):

        # Generic text class to be displayed,
        # but it can be updated

        text.Text.__init__(self, texts, size, x, y)

        self.start_x = self.rect.centerx
        self.start_y = self.rect.centery

    def update_text(self, texts):

        # Change the image to the new text
        # and move to the position
        self.image = self.font.render(texts, True, constants.WHITE)

        self.rect = self.image.get_rect()

        self.rect.centerx = self.start_x
        self.rect.centery = self.start_y

    def draw(self, display):

        # Draw to the display
        display.blit(self.image, (self.rect.x, self.rect.y))


class HUD(pygame.sprite.Sprite):

    def __init__(self, player, small):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.middle = 360 if small else 480

        # Load all of the components
        sprite_sheet = spritesheet.SpriteSheet("src/resources/hud_bar.png")
        self.image = sprite_sheet.get_image(0, 0, 480, 48)

        self.rect = self.image.get_rect()
        self.rect.centerx = self.middle
        self.rect.y = 672

        self.health_label = Label("Health:", 28, self.middle - 232, 680)
        self.stamina_label = Label("Stamina:", 28, self.middle + 8, 680)

        self.health_num = Label("100%", 28, self.middle - 112, 680)
        self.stamina_num = Label("100%", 28, self.middle + 128, 680)

        self.player = player

        self.y_pos = 492 if small else 672

    def update(self):

        # Update the labels with new values
        if self.player.health <= 0:
            self.health_num.update_text("0.0")
        else:
            self.health_num.update_text("{0:.1f}%".format(round(self.player.health, 1)))

        if self.player.stamina <= 0:
            self.stamina_num.update_text("0.0")
        else:
            self.stamina_num.update_text("{0:.1f}%".format(round(self.player.stamina -
                                                                 self.player.stamina*(1-(self.player.stamina/100)), 1)))

        # If the player has got high enough move the hud to the bottom of the screen
        if self.player.rect.y > 200:
            self.rect.y = 0
            self.health_label.rect.centery = 24
            self.stamina_label.rect.centery = 24
            self.health_num.rect.centery = 24
            self.stamina_num.rect.centery = 24
        else:
            self.rect.y = self.y_pos
            self.health_label.rect.centery = self.y_pos + 24
            self.stamina_label.rect.centery = self.y_pos + 24
            self.health_num.rect.centery = self.y_pos + 24
            self.stamina_num.rect.centery = self.y_pos + 24

    def draw(self, display):

        # Draw everything to the display
        display.blit(self.image, (self.rect.x, self.rect.y))
        self.health_label.draw(display)
        self.stamina_label.draw(display)
        self.health_num.draw(display)
        self.stamina_num.draw(display)


class Timer(Label):

    def __init__(self, num):

        # Call the parents constructor
        Label.__init__(self, str(num), 66, 10, 10)

        self.start_value = num
        self.value = num
        self.can_update = False

    def update(self):

        # Update its value and text
        self.value -= 1
        self.update_text(str(self.value))
        saves.save_data["time_left"] = self.value
        saves.save()

    def reset(self):

        # Reset to original value
        self.value = self.start_value
        self.update_text(str(self.value))

    def set(self, val):

        # Set to a specific value
        self.value = val
        self.update_text(str(self.value))
