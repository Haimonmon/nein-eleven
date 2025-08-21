from .core import * 
from .ui import *
from .utils import *

from typing import Tuple, Callable

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


    def create_window(self, height: int = 740, width: int = 1200, title: str  = "The Bit Engine", icon: str = "favicon.png", background_color: str | Tuple[int] = "#1A1A1A") -> BitInterfaceWindow:
        """ Creates a tetris window """

        self.window = BitInterfaceWindow(height, width, title, icon, background_color)

        return self.window


    @require_window
    def create_grid(self, rows: int = 20, columns: int = 30, cell_size: int = 30, display_grid: bool = True, border_color: str | Tuple[int] = (100, 100, 100), border_width: int = 1) -> None:
        """ Creates a tetris board or grid """
      
        grid_logic = self.window.add_object(BitLogicGrid(rows, columns))
        grid_spawner = self.window.add_object(BitLogicTetrominoGridSpawner(self.window, grid_logic, self.tick_speed)) 

        self.window.add_object(BitInterfaceGrid(grid_logic, cell_size, display_grid, border_color, border_width))

        return grid_spawner
    

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