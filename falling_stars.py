import sys
import pygame
import random
from settings import Settings
from monster import Monster
from star import Star
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class FallingStars:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        # create screen of certain size
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # # A fullscreen variant of game
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Falling Stars")

        # Create an instance to store game statistics, and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.monster = Monster(self)
        self.stars = pygame.sprite.Group()

        # Make the Play button.
        self.play_button = Button(self, "Start")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self._create_star()
                self.monster.update()
                self._update_stars()
                self._check_timer()

            self._update_screen()

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings and get start_time.
            self.start_game_time = pygame.time.get_ticks()
            self.stats.last_time = self.start_game_time
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_game_time()
            self.sb.prep_level()
            self.sb.prep_monsters()

            # Get rid of any remaining stars.
            self.stars.empty()

            # Center the monster.
            self.monster.center_monster()

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_UP:
            self.monster.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.monster.moving_down = True
        elif event.key == pygame.K_RIGHT:
            self.monster.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.monster.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_UP:
            self.monster.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.monster.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.monster.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.monster.moving_left = False

    def _update_stars(self):
        """Update position of stars and get rid of fallen stars."""
        # Update stars` positions.
        self.stars.update()

        if pygame.sprite.spritecollideany(self.monster, self.stars):
            self._monster_hit()

        # Get rid of stars that have disappeared.
        for star in self.stars.copy():
            if star.rect.top >= self.settings.screen_height:
                self.stars.remove(star)

    def _check_timer(self):
        """Track game time and increase speed after each 10 sec"""
        ticks = pygame.time.get_ticks()
        self.stats.game_time = (ticks - self.start_game_time)

        # Increase speed and level.
        if self.stats.game_time - self.stats.last_time > 10000:
            self.stats.last_time = self.stats.game_time
            self.settings.increase_speed()
            self.stats.level += 1

        # Show time and level.
        self.sb.prep_game_time()
        self.sb.check_longest_time()
        self.sb.prep_level()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.monster.blitme()
        self.stars.draw(self.screen)

        # Draw the time information.
        self.sb.show_time()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _create_star(self):
        """Create a new star and add it to the bullets group."""
        if random.random() < self.settings.chance_to_appear:
            new_star = Star(self)
            self.stars.add(new_star)

    def _monster_hit(self):
        """Respond to the monster being hit by a star."""

        if self.stats.monsters_left > 0:
            # Decrease monster, and update scoreboard.
            self.stats.monsters_left -= 1
            self.sb.prep_monsters()

            # Remove stars and center the monster
            self.stars.empty()
            self.monster.center_monster()

        else:
            self.stats.game_active = False


if __name__ == '__main__':
    # Make a game instance, and run the game.
    fs = FallingStars()
    fs.run_game()
