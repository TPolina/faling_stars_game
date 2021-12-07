import pygame.font
from pygame.sprite import Group
from monster import Monster


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, fs_game):
        """Initialize scorekeeping attributes."""
        self.fs_game = fs_game
        self.screen = fs_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = fs_game.settings
        self.stats = fs_game.stats

        # Font settings for scoring information.
        self.text_color = (255, 218, 130)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_game_time()
        self.prep_longest_time()
        self.prep_level()
        self.prep_monsters()

    def prep_game_time(self):
        """Turn the time into a rendered image."""
        round_game_time = self.stats.game_time // 1000
        min = round_game_time // 60
        sec = round_game_time % 60
        game_time_str = f"{min:02}:{sec:02}"
        self.game_time_image = self.font.render(game_time_str, True, self.text_color, self.settings.bg_color)

        # Display the time at the top right of the screen.
        self.game_time_rect = self.game_time_image.get_rect()
        self.game_time_rect.right = self.screen_rect.right - 20
        self.game_time_rect.top = 20

    def prep_longest_time(self):
        """Turn the longest time into a rendered image."""
        round_longest_time = self.stats.longest_time // 1000
        min = round_longest_time // 60
        sec = round_longest_time % 60
        longest_time_str = f"{min:02}:{sec:02}"
        self.longest_time_image = self.font.render(longest_time_str, True, self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.longest_time_rect = self.longest_time_image.get_rect()
        self.longest_time_rect.centerx = self.screen_rect.centerx
        self.longest_time_rect.top = self.screen_rect.top

    def check_longest_time(self):
        """Check to see if there's a new longest time."""
        if self.stats.game_time > self.stats.longest_time:
            self.stats.longest_time = self.stats.game_time
        self.prep_longest_time()

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.game_time_rect.right
        self.level_rect.top = self.game_time_rect.bottom + 10

    def prep_monsters(self):
        """Show how many monsters are left."""
        self.monsters = Group()
        for monster_number in range(self.stats.monsters_left):
            monster = Monster(self.fs_game)
            monster.image = pygame.transform.scale(monster.original_image, (50, 50))
            monster.rect.x = 5 + monster_number * monster.rect.width
            monster.rect.y = 10
            self.monsters.add(monster)

    def show_time(self):
        """Draw time, level, and monsters to the screen."""
        self.screen.blit(self.game_time_image, self.game_time_rect)
        self.screen.blit(self.longest_time_image, self.longest_time_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.monsters.draw(self.screen)
