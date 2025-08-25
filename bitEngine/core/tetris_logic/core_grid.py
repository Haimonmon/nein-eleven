import os
import copy
import json
import random

from typing import Literal, List

from .core_tetromino import BitLogicTetromino
from .core_next_piece_view import BitLogicNextPiece
from ..ngrams import PatternNGrams

from bitEngine.ui.tetris_ui import BitInterfaceTetromino


class BitLogicGrid:
    """ Collision logics """
    def __init__(self, window, rows: int = 20, columns: int = 30) -> None:
        self.window = window

        self.rows = rows
        self.columns = columns

        self.cell_coordinates = [[0 for _ in range(columns)] for _ in range(rows)]
        
        self.offset_x = 0
        self.offset_y = 0

    
    def get_board_state(self) -> List:
        """ Returns the whole board state """
        return self.cell_coordinates
    

    def update(self) -> None:
        pass


class BitLogicTetrominoGridSpawner:
    """ Basically just a spawner 🤓☝️"""
    def __init__(self, engine, grid_logic: BitLogicGrid, next_piece_logic: BitLogicNextPiece, tick_speed: int = 500):
        self.engine = engine 

        self.tick_speed = tick_speed

        self.grid_logic = grid_logic
        
        self.next_piece_logic: BitLogicNextPiece = next_piece_logic

        self.tetromino_logic = BitLogicTetromino

        self.tetromino_interface = BitInterfaceTetromino
        self.tetromino_colors = "green"
        self.tetromino_border_color = None
        self.tetromino_indicator_color = "white"

        # * predictor handles write_pattern and predict
        self.predictor = PatternNGrams()

        self.spawn_test = True
        self.spawn_num = 0

        self.spawned_tetromino = None

        self.controller = None

        
    def change_tetromino_appearance(self, fill_colors: str | List[str], border_color: str | set = (0, 0, 0), indicator_color: str | set = "white") -> None:
        """ Change tetromino colors """
        self.tetromino_colors = fill_colors
        self.tetromino_border_color = border_color
        self.tetromino_indicator_color = indicator_color
        return


    def update(self) -> None:
        # * Spawn once only for testing
        if not self.spawned_tetromino or self.spawned_tetromino.landed:
            if self.spawned_tetromino:
                # * Use PatternNGrams' write_pattern instead of local one
                landed_coords = self.spawned_tetromino.coordinates
                piece = self.spawned_tetromino.piece_shape
                rotation = self.controller.rotation_index

                
                # * count cleared lines
                lines_cleared = 0
                for y in range(self.grid_logic.rows):
                    if all(self.grid_logic.cell_coordinates[y][x] != 0
                           for x in range(self.grid_logic.columns)):
                        lines_cleared += 1

                # * get the next queue from next_piece_logic
                next_queue = self.next_piece_logic.peek_next()

                self.predictor.write_pattern(
                    piece=piece,
                    landed_coords=landed_coords,
                    rotation=rotation,
                    lines_cleared=lines_cleared,
                    next_queue=next_queue,
                    reason="auto"
                )

            self.spawn(self.next_piece_logic.get_piece())
            self.spawned_tetromino.indicator = True


    def spawn(self, piece_shape: Literal["O", "I", "T", "L", "J", "S", "Z"] = "O", x: int = None, y: int = None) -> None:
        """ spawns tetromino pieces on the grid """
            
        piece_shape = piece_shape.upper()
        predictor = getattr(self, "predictor", None)
        print(f"[spawn] piece={piece_shape} | predictor attached? {'yes' if predictor else 'no'}")

        created_tetromino: BitLogicTetromino = self.create(piece_shape)

        # Ask predictor where it *should* go
        if self.predictor is not None:
            try:
                board_state = self.grid_logic.get_board_state()
                suggestion = self.predictor.predict(
                    board_state,
                    piece_shape,
                    columns=self.grid_logic.columns,
                    rows=self.grid_logic.rows
                )
                print(f"[spawn] predictor suggestion={suggestion}")

                if suggestion:
                    created_tetromino.suggested_position = suggestion
            except Exception as e:
                print(f"[spawn] predictor error: {e}")
                
        # * I make this because, Iwant the tetromino to spawn within in any area of the spawn 🫡
        if x is None:
            start_x = random.randint(0, self.grid_logic.columns)
        else:
            start_x = x
        
        if y is None:
            start_y = 0
        else:
            start_y = y

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


    def format_board(self, board):
        return ["[" + ",".join(str(c) for c in row) + "]" for row in board]


    def write_pattern(self, board, pieces, save_path="pattern.json"):
        board_copy = copy.deepcopy(board)

        for tetro in pieces:
            if tetro.landed:
                for x, y in tetro.coordinates:
                    board_copy[y][x] = tetro.piece_shape

        pattern_data = []
        for tetro in pieces:
            entry = {
                "piece": tetro.piece_shape,
                "landed_coordinates": tetro.coordinates,
                "board": self.format_board(board_copy),   # <── formatted
                "chosen_position": [tetro.coordinates[0][0], "default"]
            }
            pattern_data.append(entry)

        if os.path.exists(save_path):
            with open(save_path, "r") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = []
        else:
            existing = []

        existing.extend(pattern_data)

        with open(save_path, "w") as f:
            json.dump(existing, f, indent=2)

        return pattern_data


    def create(self, piece_shape: Literal["0", "I"]) -> BitLogicTetromino:
        """ Creates the tetromino peice coordinates or its piece shape """

        coordinates = self.next_piece_logic.piece.get(piece_shape)

        created_logic_tetromino: BitLogicTetromino = self.tetromino_logic(self.grid_logic, piece_shape, coordinates, self.tick_speed)

        # * ADDS TO THE WINDOW SURFACE
        self.engine.add_object(created_logic_tetromino)
        tetromino_interface = self.tetromino_interface(created_logic_tetromino, self.tetromino_colors)

        tetromino_interface.border_color = self.tetromino_border_color
        tetromino_interface.indicator_color = self.tetromino_indicator_color

        self.engine.add_object(tetromino_interface)

        return created_logic_tetromino


class BitLogicLineCleaner:
    def __init__(self, engine, grid_logic, num_clearing):
        self.engine = engine

        self.grid_logic = grid_logic

        self.num_clearing = num_clearing

        self.num_cleared_rows = 0

        self.tetrominoes = []


    def update(self) -> None:
        self.tetrominoes = self.engine.get_objects("BitLogicTetromino")
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
            self.num_cleared_rows = len(rows_to_clear)
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
