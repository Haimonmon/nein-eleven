from typing import List, Tuple
import pygame

class BitLogicTetromino:
    """ Tetromino functionalities """
    def __init__(self, grid_logic, width: int, height: int, piece_shape: str, coordinates: List[Tuple[int, int]], tick_speed: int = 500) -> None:
        self.grid_logic = grid_logic

        # * For n grams
        self.word = None

        # * By Blocks
        self.width = width
        self.height = height

        # * Piece Name
        self.piece_shape = piece_shape

        self.coordinates: List[Tuple[int, int]] = coordinates

        self.landed = False

        # * Gravity timing
        self.gravity_delay = tick_speed  # * milliseconds on falling
        self.last_gravity_time = pygame.time.get_ticks()

        self.falling_skip = 3


    def update(self) -> None:
        """ Update tetromino state """
        self.apply_gravity()


    def apply_gravity(self, falling_skip: int = 1) -> None:
        """ Want to have gravity? """
        now = pygame.time.get_ticks()

        if now - self.last_gravity_time >= self.gravity_delay:
   
            for x, y in self.coordinates:
                self.grid_logic.cell_coordinates[y][x] = 0

            if not self.check_collision(dy = falling_skip):
                self.coordinates = [(x, y + falling_skip) for (x, y) in self.coordinates]
            else:
                self.landed = True

            for x, y in self.coordinates:
                self.grid_logic.cell_coordinates[y][x] = 1
            
            self.last_gravity_time = now
        # self.landed = True


    def check_collision(self, dx: int = 0, dy: int = 0) -> bool:
        """ collision logic """
        for x, y in self.coordinates:
            new_x = x + dx
            new_y = y + dy

            # * Check left or right edges
            # if new_x < 0 or new_x >= self.width:
            #     return True

            # * Check bottom edge
            if new_y >= self.grid_logic.rows:
                return True

            # * Check collision with other blocks (ignore current piece's own cells)
            if self.grid_logic.cell_coordinates[new_y][new_x] != 0 and (new_x, new_y) not in self.coordinates:
                return True

        return False

if __name__ == "__main__":
      pass