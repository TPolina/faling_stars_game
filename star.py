import pygame
import random
from pygame.sprite import Sprite


class Star(Sprite):
    """A class to represent a single star."""

    def __init__(self, fs_game):
        """Initialize the star and set its starting position."""
        super().__init__()
        self.screen = fs_game.screen
        self.settings = fs_game.settings

        # load the image and get its rect
        self.original_image = pygame.image.load('images/star.bmp')
        self.image = pygame.transform.scale(self.original_image, (35, 35))
        self.rect = self.image.get_rect()

        # Start each new star somewhere at the top left of the screen.
        self.rect.x = random.randrange(self.settings.screen_width)
        self.rect.y = -self.rect.height

        # store decimal value for the star's vertical position.
        self.y = float(self.rect.y)

    def update(self):
        """Move the star up the screen."""
        # Update the decimal position of the bullet.
        self.y += self.settings.star_speed
        # Update the rect position.
        self.rect.y = self.y
