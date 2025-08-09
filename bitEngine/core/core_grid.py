from typing import Literal, Dict, List, Tuple, Type

from .core_tetromino import BitLogicTetromino
from BitEngine.ui import BitInterfaceTetromino

class BitLogicGrid:
    """ Collision logics """
    def __init__(self, rows: int = 20, columns: int = 30):
        self.rows = rows
        self.columns = columns

        self.cell_coordinates = [[0 for _ in range(columns)] for _ in range(rows)]


    def update(self) -> None:
        pass


class BitLogicTetrominoGridSpawner:
    def __init__(self, window, grid_logic: BitLogicGrid):
         self.window = window 

         self.grid_logic = grid_logic
         self.tetromino_logic = BitLogicTetromino
         self.tetromino_interface = BitInterfaceTetromino

         self.spawn_test = True


    def update(self) -> None:
        # * Spawn once only for testing
        if self.spawn_test:
            self.spawn(piece_shape = "O")
            self.spawn_test = False


    def spawn(self, piece_shape: Literal["O", "I"] = "O") -> None:
        """ spawns tetromino pieces on the grid """
        # * Pick starting location
        start_x = (self.grid_logic.columns // 2) - 2
        start_y = 0

        shape_coords = self.create(piece_shape)

        positioned_shape = [(x + start_x, y + start_y)
                            for x, y in shape_coords]

        self.tetromino_logic.shape = positioned_shape

        for x, y in positioned_shape:
            self.grid_logic.cell_coordinates[y][x] = 1


    def create(self, piece_shape: Literal["0", "I"]) -> None:
        """ Creates the tetromino peice coordinates or its piece shape """

        piece: Dict[str, List[Tuple[int, int]]] = {
            "O": [(5, 0), (6, 0), (5, 1), (6, 1)],
            "I": [(3, 0), (4, 0), (5, 0), (6, 0)]
        }

        created_logic_tetromino: BitLogicTetromino = self.tetromino_logic(self.grid_logic)

        # * SET STATES 🟢🍏
        created_logic_tetromino.word = "TESTING"
        created_logic_tetromino.coordinates = piece.get(piece_shape)
        created_logic_tetromino.piece_word = piece_shape

        # * ADDS TO THE WINDOW SURFACE
        self.window.add_object(created_logic_tetromino)
        self.window.add_object(self.tetromino_interface(created_logic_tetromino))

        return created_logic_tetromino.coordinates