class GameStats:
    """Track statistics for Falling Stars."""

    def __init__(self, fs_game):
        """Initialize statistics."""
        self.settings = fs_game.settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.longest_time = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.monsters_left = self.settings.monster_limit
        self.level = 1
        self.last_time = 0
        self.game_time = 0
