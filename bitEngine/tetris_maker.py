from .core.tetris_logic import *
from .ui.tetris_ui import *
from .utils import *

from typing import Tuple, Dict


class BitTetrisMaker:
    """ Tetris Level Maker """
    def __init__(self,  engine) -> None:
        # * Main Window of the game application
        self.__engine = engine

        self.window = self.__engine.window

        self.tick_speed = 700

        self.num_controllers = 0


    def create_piece_queue(self, width: int = 150, height: int = 300,  max_piece_queue: int = 3, cell_size: int = 30, position_x: int = 0, position_y: int = 0, border_color: str | set = "blue", border_thickness: int = 1, num_piece_display: int = 1, background_color: str | set = None) -> Dict[str, object]:
        """ Creates a tetris piece queue viewer , it will enables you to see the next peices to be spawn along with the grid """
        if background_color is None:
            background_color = self.window.background_color
            
        piece_view_logic: BitLogicNextPiece = BitLogicNextPiece(max_piece_queue)
        piece_view_interface: BitInterfaceNextPieceView = BitInterfaceNextPieceView(piece_view_logic, width, height, cell_size, position_x, position_y, border_color, border_thickness, num_piece_display, background_color)

        self.__engine.add_object(piece_view_logic)
        self.__engine.add_object(piece_view_interface)

        return {
            "piece_view_logic": piece_view_logic,
            "piece_view_interface": piece_view_interface
        }


    def create_grid(self, piece_view, rows: int = 20, columns: int = 30, cell_size: int = 30, display_grid: bool = True, border_color: str | Tuple[int] = (100, 100, 100), border_thickness: int = 1, position_x: int = 0, position_y: int = 0) -> Dict[str, object]:
        """ Creates a tetris board or grid """

        grid_logic: BitLogicGrid = self.__engine.add_object(BitLogicGrid(self.window, rows, columns))
        grid_spawner: BitLogicTetrominoGridSpawner = self.__engine.add_object(BitLogicTetrominoGridSpawner(self.__engine, grid_logic, piece_view["piece_view_logic"], self.tick_speed)) 

        line_cleaner: BitLogicLineCleaner = self.__engine.add_object(BitLogicLineCleaner(self.__engine, grid_logic, grid_logic.rows))

        grid_interface: BitInterfaceGrid = self.__engine.add_object(BitInterfaceGrid(grid_logic, cell_size, display_grid, border_color, border_thickness, position_x, position_y))

        return {
            "grid_logic": grid_logic,
            "grid_spawner": grid_spawner,
            "grid_line_cleaner": line_cleaner,
            "grid_interface": grid_interface
        }
    

    def create_scoreboard(self, grid, width: int = 170, height: int = 150, position_x: int = 0, position_y: int = 0, border_color: str | Tuple[int] = "blue", border_thickness: int = 1) -> Dict[str, object]:
        """ Creates tetris scoreboard """

        scoreboard_logic: BitLogicScoreboard = BitLogicScoreboard(grid["grid_line_cleaner"])
        scoreboard_interface: BitInterfaceScoreBoard = BitInterfaceScoreBoard(self.__engine, scoreboard_logic ,width, height, position_x, position_y, border_color, border_thickness)

        self.__engine.add_object(scoreboard_logic)
        self.__engine.add_object(scoreboard_interface)

        return {
            "scoreboard_logic": scoreboard_logic,
            "scoreboard_interface": scoreboard_interface
        }


    def add_controller(self, grid) -> BitLogicController:
        """ Apply Controller of the tetromino """
    
        self.num_controllers += 1

        controller = self.__engine.add_object(BitLogicController(grid["grid_spawner"], f"player{self.num_controllers}"))

        return controller