import pygame

class BitInterfaceScoreBoard:
    """ Renders a grid scoreboard interface """
    def __init__(self, engine, scoreboard_logic, width: int, height: int, position_x: int = 0, position_y: int = 0, border_color: str | set = "blue", border_thickness: int = 1, font_color: str = "white", font_size: int = 30, background_color: str | set = "black") -> None:
        """ Tetris board scoreboard """
        self.engine = engine

        self.scoreboard_logic = scoreboard_logic

        self.height = height
        self.width = width

        self.position_x = position_x
        self.position_y = position_y

        self.border_color = border_color
        self.border_thickness = border_thickness
        self.background_color = background_color

        self.font_color = font_color
        self.font_size = font_size


    def render(self, screen: pygame.Surface) -> None:
        self.draw_board(screen)
    

    def draw_board(self, screen: pygame.Surface) -> None:
        """ Draw the literal Scoreboard 🤓☝️ """
        if not self.scoreboard_logic:
            return

        # * Draw board
        pygame.draw.rect(
            screen, 
            self.background_color, 
            (self.position_x, self.position_y, self.width, self.height)
        )

        pygame.draw.rect(
            screen,
            self.border_color,
            (self.position_x, self.position_y, self.width, self.height),
            width=self.border_thickness
        )

        self.display_details(screen)


    def display_details(self, screen: pygame.Surface) -> None:
        """ Display's scoreboard information """
        font = pygame.font.Font(None, self.font_size)

        score_text = f"Score: {self.scoreboard_logic.current_score}"
        level_text = f"Level: {self.scoreboard_logic.current_level}"

        score_surface = font.render(score_text, True, self.font_color)  
        level_surface = font.render(level_text, True, self.font_color)

        total_height = score_surface.get_height() + level_surface.get_height() + 2 * 5  
        start_y = self.position_y + (self.height - total_height) // 2 

        # Center horizontally and blit
        for i, surface in enumerate([score_surface, level_surface]):
            rect = surface.get_rect(center=(self.position_x + self.width // 2, start_y + surface.get_height() // 2))
            screen.blit(surface, rect)
            start_y += surface.get_height() + 5
        
