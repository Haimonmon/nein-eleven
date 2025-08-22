from .core import * 
from .ui import *
from .utils import *

from typing import Tuple, Callable, Dict

class BruhTheresNoWindows(Exception):
    """ Raised when the window object is missing. """
    def __init__(self, message = "Bruh... there's literally no window to work with!"):
        super().__init__(message)


# * ============ DECORATORS ============

def require_window(func: Callable):
    """ Decorator for window validation """
    def wrapper(self, *args, **kwargs):
        if not self.window:
            raise BruhTheresNoWindows()
        return func(self, *args, **kwargs)
    return wrapper

# * ====================================


class Bit:
    """ The Bit's mighty Assembler """
    def __init__(self, tick_speed: int = 7):
        self.window = None
        
        self.tick_speed = tick_speed * 100

        self.num_controllers = 0

    def create_window(self, height: int = 740, width: int = 1200, title: str = "The Bit Engine", icon: str = "favicon.png", background_color: str | Tuple[int] = "#1A1A1A", scanline_alpha: int = 70, bend_amount: float = 0.85, flicker_intensity: int = 20, crt_effect: bool = False) -> BitInterfaceWindow:
        """ Creates a tetris window """

        self.window = BitInterfaceWindow(height, width, title, icon, background_color, scanline_alpha, bend_amount, flicker_intensity, crt_effect)

        return self.window


    @require_window
    def create_piece_viewer(self, width: int, height: int,  max_piece_queue: int = 3, cell_size: int = 30, position_x: int = 0, position_y: int = 0, border_color: str | set = "blue", border_thickness: int = 1, num_piece_display: int = 1) -> Dict[str, object]:
        """ Creates a tetris next piece viewer """
        piece_view_logic: BitLogicNextPiece = BitLogicNextPiece(max_piece_queue)
        piece_view_interface: BitInterfaceNextPieceView = BitInterfaceNextPieceView(self.window, piece_view_logic, width, height, cell_size, position_x, position_y, border_color, border_thickness, num_piece_display)

        self.window.add_object(piece_view_logic)
        self.window.add_object(piece_view_interface)

        return {
            "piece_view_logic": piece_view_logic,
            "piece_view_interface": piece_view_interface
        }


    @require_window
    def create_grid(self,piece_view: BitLogicNextPiece = None, rows: int = 20, columns: int = 30, cell_size: int = 30, display_grid: bool = True, border_color: str | Tuple[int] = (100, 100, 100), border_width: int = 1, position_x: int = 0, position_y: int = 0) -> Dict[str, object]:
        """ Creates a tetris board or grid """
      
        grid_logic: BitLogicGrid = self.window.add_object(BitLogicGrid(self.window, rows, columns))
        grid_spawner: BitLogicTetrominoGridSpawner = self.window.add_object(BitLogicTetrominoGridSpawner(self.window, grid_logic, piece_view, self.tick_speed)) 

        line_cleaner: BitLogicLineCleaner = self.window.add_object(BitLogicLineCleaner(self.window, grid_logic, grid_logic.rows))

        grid_interface: BitInterfaceGrid = self.window.add_object(BitInterfaceGrid(grid_logic, cell_size, display_grid, border_color, border_width, position_x, position_y))

        return {
            "grid_logic": grid_logic,
            "grid_spawner": grid_spawner,
            "grid_line_cleaner": line_cleaner,
            "grid_interface": grid_interface
        }
    

    @require_window
    def create_scoreboard(self, grid_line_cleaner: BitLogicLineCleaner, width: int, height: int, position_x: int = 0, position_y: int = 0, border_color: str | Tuple[int] = "blue", border_thickness: int = 1) -> Dict[str, object]:
        """ Creates tetris scoreboard """
        scoreboard_logic: BitLogicScoreboard = BitLogicScoreboard(grid_line_cleaner)
        scoreboard_interface: BitInterfaceScoreBoard = BitInterfaceScoreBoard(self.window, scoreboard_logic ,width, height, position_x, position_y, border_color, border_thickness)

        self.window.add_object(scoreboard_logic)
        self.window.add_object(scoreboard_interface)

        return {
            "scoreboard_logic": scoreboard_logic,
            "scoreboard_interface": scoreboard_interface
        }


    @require_window
    def add_controller(self, object: object) -> None:
        """ Apply Controller of the tetromino """
    
        self.num_controllers += 1

        controller = self.window.add_object(BitLogicController(object, f"player{self.num_controllers}"))

        return controller


    @require_window
    def play(self) -> None:
         self.window.render()
         self.window.exit()


if __name__ == "__main__":
        engine = Bit(tick_speed=-2)
        window = engine.create_window()
        grid = engine.create_grid()
        controller = engine.add_controller(grid)
        engine.play()