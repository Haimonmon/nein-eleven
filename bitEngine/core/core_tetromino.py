from typing import List, Tuple
import pygame

class BitLogicTetromino:
    """ Tetromino functionalities """
    def __init__(self, grid_logic, piece_shape: str, coordinates: List[Tuple[int, int]], tick_speed: int = 500) -> None:
        self.grid_logic = grid_logic

        # * For n grams
        self.word = None

        self.width = 0
        self.height = 0

        # * Highest X and Y values default
        self.max_x = 0
        self.min_x = 0

        self.max_y = 0
        self.min_y = 0

        # * Piece Name
        self.piece_shape = piece_shape

        self.coordinates: List[Tuple[int, int]] = coordinates

        self.landed = False

        # * Gravity timing
        self.gravity_delay = tick_speed  # * milliseconds on falling
        self.last_gravity_time = pygame.time.get_ticks()

        self.falling_skip = 3

        self.counter = 0

        self.pivot = self._get_block_pivot()

        self._get_width()
        self._get_height()
    

    def _get_height(self) -> None:
        """ gets latest tetromino height """
        ys = [y for _, y in self.coordinates]
        self.height = max(ys) - min(ys) + 1


    def _get_width(self) -> None:
        """ gets latest tetromino width """
        xs = [x for x, _ in self.coordinates]
        self.width = max(xs) - min(xs) + 1
    

    def _get_block_pivot(self) -> Tuple[int, int]:
        """ Return a piece center pivot """
        xs = [x for x, _ in self.coordinates]
        ys = [y for _, y in self.coordinates]

        self.min_x, self.max_x = min(xs), max(xs)
        self.min_y, self.max_y = min(ys), max(ys)

        center_x = (self.min_x + self.max_x) / 2
        center_y = (self.min_y + self.max_y) / 2

        # * snap to nearest block, decimals are not allowed because of block or grid
        pivot_x = round(center_x)
        pivot_y = round(center_y)

        return (pivot_x, pivot_y)


    def change_coordinates(self, new_coordinates: List[Tuple[int, int]], falling_skip: int = 1) -> None:
        """ Change tetromino coordinates state """
        for x, y in self.coordinates:
            self.grid_logic.cell_coordinates[y][x] = 0

        if not self.check_collision(dy = falling_skip):
            self.coordinates = new_coordinates
        else:
            self.landed = True

        for x, y in self.coordinates:
            self.grid_logic.cell_coordinates[y][x] = 1


    def update(self) -> None:
        """ Update tetromino state """
        self.apply_gravity()
        self._get_width()


    def apply_gravity(self, falling_skip: int = 1) -> None:
        """ falling state of the tetromino """
        if not self.coordinates:
            return 
        
        now = pygame.time.get_ticks()

        if now - self.last_gravity_time >= self.gravity_delay:

            self.change_coordinates([(x, y + falling_skip) for (x, y) in self.coordinates], falling_skip)
            
            self.last_gravity_time = now


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
    

    def rotate(self, direction: str = "cw") -> None:
        """ Rotates tetromino counter or in clockwise turn """
        if not self.coordinates:
            return
        
        # ! STILL FIXING
        # * find's pivot or center point
        px = sum(x for x, _ in self.coordinates) / len(self.coordinates)
        py = sum(y for _, y in self.coordinates) / len(self.coordinates)

        new_coords = []

        for (x, y) in self.coordinates:
            x -= px
            y -= py

            # * Rotatation
            if direction == "cw":
                x, y = y, -x
            elif direction == "ccw":
                x, y = -y, x

            new_coords.append((round(x + px), round(y + py)))

        self.change_coordinates(new_coords)
    

if __name__ == "__main__":
      pass