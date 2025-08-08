import pygame
from typing import Set, Literal

class BitGrid:
    """ Renders a grid or tetris board interface """
    def __init__(self, row: int = 20, columns: int = 30, cell_size: int = 30, display_grid: bool = False, border_color: Set[int] = (100, 100, 100), border_width: int = 1) -> None:
        """ Tetris board """
        self.row = row
        self.columns = columns
        self.cell_size = cell_size
        self.display_grid = display_grid

        self.border_color = border_color
        self.border_width = border_width

        self.cell_coordinates = []

        self.board_width = 0
        self.board_height = 0

        self.offset_x = 0
        self.offset_y = 0
    

    def render(self, screen: pygame.Surface) -> None:
        """ Renders a tetris board """

        windows_width, windows_height = screen.get_size()

        self.board_width: int = self.columns * self.cell_size
        self.board_height: int = self.row * self.cell_size

        self.offset_x: int = (windows_width - self.board_width) // 2
        self.offset_y: int = (windows_height - self.board_height) // 2

        # * For board row
        for row in range(self.row + 1):
            if row in [0, self.row] and not self.display_grid:
                self.draw_vertical_line(screen, self.offset_x, self.offset_y, row, self.board_width, self.border_color, self.border_width)
            
            if self.display_grid:
                self.draw_vertical_line(screen, self.offset_x, self.offset_y, row, self.board_width, self.border_color)


        # * For board columns
        for column in range(self.columns + 1):
            if column in [0, self.columns] and not self.display_grid:
                self.draw_horizontal_line(screen, self.offset_x, self.offset_y, column, self.board_height, self.border_color, self.border_width)
            
            if self.display_grid:
                self.draw_horizontal_line(screen, self.offset_x, self.offset_y, column, self.board_height, self.border_color)


    def draw_vertical_line(self, screen: pygame.Surface, offset_x: float, offset_y: float, row: int, board_width: int, color: Set[int] = (100, 100, 100), width: int = 1) -> None:
        """ Draws a perfect line base within its coordinate """
        pygame.draw.line(
            screen, color,
            (offset_x, offset_y + row * self.cell_size),
            (offset_x + board_width, offset_y + row * self.cell_size),
            width = width
        )
    

    def draw_horizontal_line(self, screen: pygame.Surface, offset_x: float, offset_y: float, column: int, board_height: int, color: Set[int] = (100, 100, 100), width: int = 1) -> None:
        """ Draws a perfect line base within its coordinate """
        pygame.draw.line(
            screen, color,
            (offset_x + column * self.cell_size, offset_y),
            (offset_x + column * self.cell_size, offset_y + board_height),
            width = width
        )


   

        
class BitGridScoreBoard:
    def __init__(self, height: int, width: int) -> None:
        """ Tetris board scoreboard """
        self.__height = height
        self.__width = width
    
    def render() -> None:
        pass


if __name__ == "__main__":
      pass