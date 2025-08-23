import random
import os
import copy
import json

from typing import Literal, Dict, List, Tuple, Type

from .core_tetromino import BitLogicTetromino
from .core_next_piece_view import BitLogicNextPiece
from .ngrams import PatternNGrams
from .core_controller import BitLogicController

from bitEngine.ui import BitInterfaceTetromino


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
    def __init__(self, window, grid_logic: BitLogicGrid, next_piece_logic: BitLogicNextPiece, tick_speed: int = 500):
        self.window = window 
        self.tick_speed = tick_speed
        self.grid_logic = grid_logic
        self.next_piece_logic: BitLogicNextPiece = next_piece_logic

        self.tetromino_logic = BitLogicTetromino
        self.tetromino_interface = BitInterfaceTetromino
        self.tetromino_colors = "green"
        self.tetromino_border_color = None
        self.tetromino_indicator_color = "white"

        # predictor handles write_pattern and predict
        self.predictor = PatternNGrams()

        self.spawn_test = True
        self.spawn_num = 0
        self.spawned_tetromino = None
        self.controller = BitLogicController(object)


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
                # Use PatternNGrams' write_pattern instead of local one
                landed_coords = self.spawned_tetromino.coordinates
                piece = self.spawned_tetromino.piece_shape
                rotation = self.controller.rotation_index

                # count cleared lines
                lines_cleared = 0
                for y in range(self.grid_logic.rows):
                    if all(self.grid_logic.cell_coordinates[y][x] != 0 
                        for x in range(self.grid_logic.columns)):
                        lines_cleared += 1

                # get the next queue from next_piece_logic
                next_queue = self.next_piece_logic.peek_next()

                self.predictor.write_pattern(
                    piece=piece,
                    landed_coords=landed_coords,
                    board=self.grid_logic.cell_coordinates,
                    rotation=rotation,
                    lines_cleared=lines_cleared,
                    next_queue=next_queue,
                    reason="auto"
                )

            # Spawn the next piece
            self.spawn(self.next_piece_logic.get_piece())
            self.spawned_tetromino.indicator = True


    def spawn(self, piece_shape: Literal["O", "I", "T", "L", "J", "S", "Z"] = "O", x: int = None, y: int = None) -> None:
        """ spawns tetromino pieces on the grid """
            
        piece_shape = piece_shape.upper()
        predictor = getattr(self, "predictor", None)
        print(f"[spawn] piece={piece_shape} | predictor attached? {'yes' if predictor else 'no'}")

        # Create the tetromino normally
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

        # Normal spawn logic (random x, top y=0)
        if x is None:
            start_x = random.randint(0, self.grid_logic.columns - created_tetromino.max_x - 1)
        else:
            start_x = x

        if y is None:
            start_y = 0
        else:
            start_y = y

        tetromino_coordinates = [(cx + start_x, cy + start_y) for cx, cy in created_tetromino.coordinates]
        
        for gx, gy in tetromino_coordinates:
            self.grid_logic.cell_coordinates[gy][gx] = piece_shape

        created_tetromino.coordinates = tetromino_coordinates
        self.spawned_tetromino = created_tetromino


    def create(self, piece_shape: Literal["O", "I"]) -> BitLogicTetromino:
        """ Creates the tetromino piece coordinates or its piece shape """
        coordinates = self.next_piece_logic.piece.get(piece_shape)
        created_logic_tetromino: BitLogicTetromino = self.tetromino_logic(self.grid_logic, piece_shape, coordinates, self.tick_speed)

        # * ADDS TO THE WINDOW SURFACE
        self.window.add_object(created_logic_tetromino)
        tetromino_interface = self.tetromino_interface(created_logic_tetromino)

        tetromino_interface.color = self.tetromino_colors
        tetromino_interface.border_color = self.tetromino_border_color
        tetromino_interface.indicator_color = self.tetromino_indicator_color

        self.window.add_object(tetromino_interface)

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