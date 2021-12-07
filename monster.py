import pygame
from pygame.sprite import Sprite


class Monster(Sprite):
    """A class to manage the monster."""

    def __init__(self, fs_game):
        """Initialize the monster and set its starting position."""
        super().__init__()
        self.screen = fs_game.screen
        self.settings = fs_game.settings
        self.screen_rect = fs_game.screen.get_rect()

        # load the image and get its rect.
        self.original_image = pygame.image.load('images/monster.bmp')
        self.image = pygame.transform.scale(self.original_image, (70, 70))
        self.rect = self.image.get_rect()

        # place the monster in the center of the screen.
        self.rect.center = self.screen_rect.center

        # store decimal value for the monster's position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the monster's position based on the movement flags."""
        # Update the monster's x and y value.
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.monster_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.monster_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.monster_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.monster_speed

        # Update rect object from self.x and self.y.
        self.rect.x = self.x
        self.rect.y = self.y

    def center_monster(self):
        """Center the monster on the screen."""
        self.rect.center = self.screen_rect.center
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the monster at its current location."""
        self.screen.blit(self.image, self.rect)
