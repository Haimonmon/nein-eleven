import pygame
from typing import Set, Any

class BitInterfaceGrid:
    """ Renders a grid or tetris board interface """
    def __init__(self, grid_logic, cell_size: int = 30, display_grid: bool = False, border_color: Set[int] = (100, 100, 100), border_width: int = 1, position_x: int = 0, position_y: int = 0) -> None:
        """ Tetris board """
        # * internal logics
        self.grid_logic = grid_logic

        self.cell_size = cell_size
        self.display_grid = display_grid

        self.border_color = border_color
        self.border_width = border_width

        self.cell_coordinates = []

        self.position_x = position_x
        self.position_y = position_y

        self.board_width = 0
        self.board_height = 0

        self.offset_x = 0
        self.offset_y = 0
    

    def render(self, screen: pygame.Surface) -> None:
        """ Renders a tetris board """
        self.draw_board(screen)
    

    def draw_board(self, screen: pygame.Surface) -> None:
        """ Draws tetromino board """

        self.board_width: int = self.grid_logic.columns * self.cell_size
        self.board_height: int = self.grid_logic.rows * self.cell_size
        
        self.offset_x: int = self.position_x
        self.offset_y: int = self.position_y

        # self.offset_x: int = (windows_width - self.board_width) // 2
        # self.offset_y: int = (windows_height - self.board_height) // 2

        self.grid_logic.offset_x = self.offset_x
        self.grid_logic.offset_y = self.offset_y

        self._get_cell_coordinates()

        # * For board row
        for row in range(self.grid_logic.rows + 1):
            if row in [0, self.grid_logic.rows] and not self.display_grid:
                self.draw_vertical_line(screen, self.offset_x, self.offset_y,
                                        row, self.board_width, self.border_color, self.border_width)

            if self.display_grid:
                self.draw_vertical_line(
                    screen, self.offset_x, self.offset_y, row, self.board_width, self.border_color)

        # * For board columns
        for column in range(self.grid_logic.columns + 1):
            if column in [0, self.grid_logic.columns] and not self.display_grid:
                self.draw_horizontal_line(screen, self.offset_x, self.offset_y,
                                          column, self.board_height, self.border_color, self.border_width)

            if self.display_grid:
                self.draw_horizontal_line(
                    screen, self.offset_x, self.offset_y, column, self.board_height, self.border_color)
                

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
    

    def _get_cell_coordinates(self) -> None: 
        """ Gets all cell coordinates storing set of x and y coordinates """
        self.cell_coordinates.clear()
        for row in range(self.grid_logic.rows):
            for column in range(self.grid_logic.columns):
                x = self.offset_x + column * self.cell_size
                y = self.offset_y + row * self.cell_size
                self.cell_coordinates.append((x, y))


if __name__ == "__main__":
      pass