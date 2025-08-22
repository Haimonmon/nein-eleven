import pygame

from typing import List, Tuple, Literal

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

        self.shift_downed = False
        self.row_to_shift = set()
    

    def _get_height(self) -> None:
        """ gets latest tetromino height """
        if not self.coordinates:
            return
        
        ys = [y for _, y in self.coordinates]
        self.height = max(ys) - min(ys) + 1


    def _get_width(self) -> None:
        """ gets latest tetromino width """
        if not self.coordinates:
            return 
        
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


    def change_coordinates(self, new_coordinates: List[Tuple[int, int]],dx: int = 0, dy: int = 1) -> None:
        """ Change tetromino coordinates state """
        for x, y in self.coordinates:
            self.grid_logic.cell_coordinates[y][x] = 0

        if not self.check_collision(self.coordinates, dx = dx, dy = dy):
            self.coordinates = new_coordinates

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

            self.change_coordinates([(x, min(y + falling_skip, self.grid_logic.rows - 1)) for (x, y) in self.coordinates], dx = 0, dy = 1)
            
            self.last_gravity_time = now


    def check_collision(self, coordinates: List[Tuple[int, int]], dx: int = 0, dy: int = 0) -> bool:
        """ collision logic """
        for x, y in coordinates:
            new_x = x + dx
            new_y = y + dy

            # * Check left edges and right edges
            if new_x < 0 or new_x >= self.grid_logic.columns:
                return True
                          
            # * Check bottom edge
            if new_y >= self.grid_logic.rows:
                self.landed = True
                return True
            
            # * Check collision with other blocks (ignore current piece's own cells)
            if self.grid_logic.cell_coordinates[new_y][new_x] != 0 and (new_x, new_y) not in self.coordinates:
                if dy > 0:
                    self.landed = True
                return True
            
        return False
    

    def rotate(self, direction: Literal["clock_wise", "counter_clock_wise"] = "clock_wise") -> None:
        """ Rotates tetromino counter or in clockwise turn """
        if not self.coordinates:
            return
        
        # * find's pivot or center point
        px, py = self._get_block_pivot()

        new_coords = []

        for x, y in self.coordinates:
            dx = x - px
            dy = y - py
        
            if direction == "clock_wise":
                new_x = px + dy
                new_y = py - dx
            
            if direction == "counter_clock_wise":
                new_x = px - dy
                new_y = py + dx
        
            new_coords.append((new_x, new_y))

        if not self.check_collision(new_coords):
            self.change_coordinates(new_coords)

    
    def hard_drop(self) -> None:
        """ Rapid drop of the tetromino, kinda like slamdunk in tetris 🔥 """
        while not self.check_collision(self.coordinates, dy = 1):
            self.change_coordinates([(x, y + 1) for x, y in self.coordinates])
        
        self.landed = True


    def remove_rows(self, rows: set[int]) -> None:
            """ Removes specific rows in a tetrominoes coordinates """
            self.coordinates = [(x, y) for (x, y) in self.coordinates if y not in rows]

            for y in rows:
                for x in range(self.grid_logic.columns):
                    self.grid_logic.cell_coordinates[y][x] = 0

    
    def shift_down(self, rows: set[int]) -> None:
        """ Shifts down block """        
        new_coords = []

        for (x, y) in self.coordinates:
            shift = sum(1 for row in rows if row >= y)
            new_coords.append((x, y + shift))

        for x, y in self.coordinates:
            self.grid_logic.cell_coordinates[y][x] = 0

        self.coordinates = new_coords

        for x, y in self.coordinates:
            self.grid_logic.cell_coordinates[y][x] = 1


    def __debug(self, piece_name: str, string: str) -> None:
        piece_name = piece_name.upper()
        if self.piece_shape == piece_name:
            print(string)

if __name__ == "__main__":
      pass

