class BitLogicScoreboard:
    def __init__(self, line_cleaner_logic, combo_duration: float = 1.0):
        self.line_cleaner_logic = line_cleaner_logic

        self.current_score = 0

        self.current_level = 1

        self.lines_cleared = 0

        self.combo_duration = combo_duration

        self.domino_combo = 0
        self.combo_timer = 0


        self.points_per_line = {
            1: 100,
            2: 300,
            3: 500,
            4: 800  # * Tetris! 🎉✨
        }


    def update(self) -> None:
        """Update scoreboard based on lines cleared."""
        self.apply_scoring()
        
        
    def apply_scoring(self) -> None:
        """ Observe's player gameplay for scoring """
        lines = self.line_cleaner_logic.num_cleared_rows

        if lines > 0:
            self.apply_domino_scoring(self.combo_duration)

            # * Reset cleared_rows
            self.line_cleaner_logic.num_cleared_rows = 0
        else:
            if self.combo_timer > 0:
                self.combo_timer -= self.combo_duration
            else:
                self.domino_combo = 0


    def apply_domino_scoring(self, combo_duration: float) -> None:
        """ For domino effect row clearing """
        self.domino_combo += 1

        lines = self.line_cleaner_logic.num_cleared_rows
        base_points = self.points_per_line.get(lines, lines * 100)

        multiplier = 1 + (self.domino_combo - 1) * 0.5
        self.current_score += int(base_points * multiplier)

        self.lines_cleared += lines
        self.current_level = 1 + self.lines_cleared // 10

        self.combo_timer = combo_duration


if __name__ == "__main__":
      pass