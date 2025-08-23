import pygame
import random

from typing import List, Tuple
class BitInterfaceTetromino:
    """ Renders a tetromino interface """
    def __init__(self, tetromino_logic, color) -> None:
        self.tetromino_grid = tetromino_logic.grid_logic
        self.tetromino_logic = tetromino_logic
        self.cell_size = 30

        self.color = color
        
        if isinstance(self.color, list):
            self.chosen_color = random.choice(self.color)
        
        if isinstance(self.color, str) or isinstance(self.color, set):
            self.chosen_color = self.color

        self.border_color = (0, 0, 0)
        self.indicator_color = "white"

    
    def render(self, screen: pygame.Surface) -> None:
        """ Renders tetromino """
        if self.tetromino_logic.indicator and not self.tetromino_logic.landed:
            self.draw_ghost_indicator(screen)

        self.draw_tetromino(self.tetromino_logic.coordinates, self.chosen_color, self.border_color, screen)


    def draw_tetromino(self, coordinates: List[Tuple[int, int]], color: str, border_color: str | Tuple,  screen: pygame.Surface) -> None:
        """ Draws tetromino """
        if not coordinates:
            return
        
        xs = [x for x, _ in coordinates]
        ys = [y for _, y in coordinates]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        width = (max_x - min_x + 1) * self.cell_size
        height = (max_y - min_y + 1) * self.cell_size

        temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        for x, y in coordinates:
            rect = pygame.Rect(
                (x - min_x) * self.cell_size,
                (y - min_y) * self.cell_size,
                self.cell_size,
                self.cell_size
            )

            pygame.draw.rect(temp_surface, color, rect)

            screen.blit(temp_surface, (
                self.tetromino_grid.offset_x + min_x * self.cell_size,
                self.tetromino_grid.offset_y + min_y * self.cell_size
            ))
            
            # # * piece border
            if border_color:
                mask = pygame.mask.from_surface(temp_surface)
                outline = mask.outline()
                outline = [(px + self.tetromino_grid.offset_x + min_x * self.cell_size,
                            py + self.tetromino_grid.offset_y + min_y * self.cell_size)
                        for px, py in outline]
                pygame.draw.polygon(screen, border_color, outline, width=2)
    

    def draw_ghost_indicator(self, screen: pygame.Surface) -> None:
        ghost_coords = self.tetromino_logic.get_ghost_coords()
        self.draw_tetromino(ghost_coords, self.tetromino_grid.window.background_color, self.indicator_color, screen)
    


if __name__ == "__main__":
      pass