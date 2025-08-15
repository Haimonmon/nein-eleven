import pygame

class BitInterfaceTetromino:
    """ Renders a tetromino interface """
    def __init__(self, tetromino_logic) -> None:
        self.tetromino_grid = tetromino_logic.grid_logic
        self.tetromino_logic = tetromino_logic
        self.cell_size = 30
        self.color = "yellow"


    def render(self, screen: pygame.Surface) -> None:
        """ Renders tetromino """
        
        windows_width, windows_height = screen.get_size()

        board_width: int = self.tetromino_grid.columns * self.cell_size
        board_height: int = self.tetromino_grid.rows * self.cell_size

        offset_x: int = (windows_width - board_width) // 2
        offset_y: int = (windows_height - board_height) // 2

        for x, y in self.tetromino_logic.coordinates:
            rectangle = pygame.Rect(
                offset_x + x * self.cell_size,
                offset_y + y * self.cell_size,
                self.cell_size, self.cell_size
            )

            pygame.draw.rect(screen, (255, 255, 0), rectangle)
            
            # * piece border
            pygame.draw.rect(screen, (0, 0, 0), rectangle, 1)


if __name__ == "__main__":
      pass