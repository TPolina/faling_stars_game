class Settings:
    """A class to store all settings for Falling Stars."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1100
        self.screen_height = 750
        self.bg_color = (0, 0, 50)

        # Monster settings
        self.monster_limit = 3

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        # Monster settings
        self.monster_speed = 1.5

        # Star settings
        self.star_speed = 1
        self.chance_to_appear = 0.005

    def increase_speed(self):
        """Increase speed settings."""
        self.monster_speed *= self.speedup_scale
        self.star_speed *= self.speedup_scale
        self.chance_to_appear *= self.speedup_scale
