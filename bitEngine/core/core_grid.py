import random

from typing import Literal, Dict, List, Tuple, Type

from .core_tetromino import BitLogicTetromino
from .core_controller import BitLogicController

from bitEngine.ui import BitInterfaceTetromino

class BitLogicGrid:
    """ Collision logics """
    def __init__(self, window, rows: int = 20, columns: int = 30) -> None:
        self.window = window

        self.rows = rows
        self.columns = columns

        self.cell_coordinates = [[0 for _ in range(columns)] for _ in range(rows)]


    def update(self) -> None:
        pass
        # for row in self.cell_coordinates:
        #     print(row)


class BitLogicTetrominoGridSpawner:
    """ Basically just a spawner 🤓☝️"""
    def __init__(self, window, grid_logic: BitLogicGrid, tick_speed: int = 500):
        self.window = window 

        self.tick_speed = tick_speed

        self.grid_logic = grid_logic
        self.tetromino_logic = BitLogicTetromino
        self.tetromino_interface = BitInterfaceTetromino

        self.spawn_test = True
        self.spawn_num = 0

        self.piece: Dict[str, List[Tuple[int, int]]] = {
            "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
            "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
            "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
            "L": [(0, 0), (0, 1), (0, 2), (1, 2)],
            "J": [(1, 0), (1, 1), (1, 2), (0, 2)],
            "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
            "Z": [(0, 0), (1, 0), (1, 1), (2, 1)]
        }

        self.spawned_tetromino = None

        self.controller = None


    def update(self) -> None:
        # * Spawn once only for testing
        if self.spawn_test and self.spawn_num < 1:

            self.spawn("I", x = 0, y = 19)
            self.spawn("I", x = 4, y = 19)
            self.spawn("I", x = 0, y = 18)
            self.spawn("I", x = 4, y = 18)
            self.spawn("I", x = 0, y = 17)
            self.spawn("I", x = 4, y = 17)
            self.spawn("I", x = 0, y = 16)
            self.spawn("I", x = 4, y = 16)
            self.spawn("I", x = 0, y = 15)
            self.spawn("I", x = 4, y = 15)
            
            self.spawn("z", x = 8, y = 10)
            self.spawned_tetromino.rotate("clock_wise")


            self.spawn_num += 1


        if not self.spawned_tetromino or self.spawned_tetromino.landed:
            self.spawn(piece_shape = random.choice(list(self.piece.keys())))

        
        

    def spawn(self, piece_shape: Literal["O", "I", "T", "L", "J", "S", "Z"] = "O", x: int = None, y: int = None) -> None:
        """ spawns tetromino pieces on the grid """
            
        piece_shape = piece_shape.upper()
        # * I want the tetromino to spawn within in any area of the spawn 🫡
        if x is None:
            start_x = random.randint(0, self.grid_logic.columns)
        else:
            start_x = x
        
        if y is None:
            start_y = 0
        else:
            start_y = y

        created_tetromino: BitLogicTetromino = self.create(piece_shape)

        # * Solution for over exceeding of tetromino because of randint     
        if start_x + created_tetromino.max_x >= self.grid_logic.columns:
            start_x = self.grid_logic.columns - created_tetromino.max_x - 1

        
        # * Change tetromino coordinates base on grid
        tetromino_coordinates = [(x + start_x, y + start_y) for x, y in created_tetromino.coordinates]
       
        
        # * Position Tetromino on the grid
        for x, y in tetromino_coordinates:
            self.grid_logic.cell_coordinates[y][x] = 1

        created_tetromino.coordinates = tetromino_coordinates

        self.spawned_tetromino = created_tetromino
        

    def create(self, piece_shape: Literal["0", "I"]) -> BitLogicTetromino:
        """ Creates the tetromino peice coordinates or its piece shape """

        coordinates = self.piece.get(piece_shape)

        created_logic_tetromino: BitLogicTetromino = self.tetromino_logic(self.grid_logic, piece_shape, coordinates, self.tick_speed)

        # * ADDS TO THE WINDOW SURFACE
        self.window.add_object(created_logic_tetromino)
        self.window.add_object(self.tetromino_interface(created_logic_tetromino))

        return created_logic_tetromino


class BitLogicLineCleaner:
    def __init__(self, window, grid_logic, num_clearing):
        self.window = window

        self.grid_logic = grid_logic

        self.num_clearing = num_clearing

        self.tetrominoes = []


    def update(self) -> None:
        self.tetrominoes = self.window.get_objects("BitLogicTetromino")

        self.check_clearing()


    def check_clearing(self) -> None:
        """ Checks for possible row clearing """
        landed_coords = set()
        for tet in self.tetrominoes:
            if tet.landed:
                landed_coords.update(tet.coordinates)

        rows_to_clear = []

        for y in range(self.grid_logic.rows):
            if all((x, y) in landed_coords for x in range(self.grid_logic.columns)):
                rows_to_clear.append(y)
            
        if rows_to_clear:
            self.clear_rows(rows_to_clear)
    

    def clear_rows(self, rows_to_clear: List[int]) -> None:
        """ Clears a set of line of rows """
        rows_to_clear = set(rows_to_clear)

        for tetro in self.tetrominoes:
            tetro.remove_rows(rows_to_clear)
            
        for tetro in self.tetrominoes:
            tetro.shift_down(rows_to_clear)

        for tetro in self.tetrominoes:
            for (x, y) in tetro.coordinates:
                self.grid_logic.cell_coordinates[y][x] = 1
    
    
