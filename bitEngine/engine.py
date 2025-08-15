from .core import * 
from .ui import *
from .utils import *

from typing import Type

class BruhTheresNoWindows(Exception):
    """ Raised when the window object is missing. """
    def __init__(self, message = "Bruh... there's literally no window to work with!"):
        super().__init__(message)

class Bit:
    """ The Bit's mighty Assembler """
    def __init__(self, tick_speed: int = 5):
        self.window = None
        
        self.tick_speed = tick_speed * 100


    def create_window(self) -> None:
         """ Creates a tetris window """
         self.window = BitInterfaceWindow(height = 740, width = 1200)


    def create_grid(self, rows: int = 20, columns: int = 30, display_grid: bool = True) -> None:
        """ Creates a tetris board or grid """
        if not self.window:
             raise BruhTheresNoWindows()
        
        grid_logic = self.window.add_object(BitLogicGrid(rows, columns))
        self.window.add_object(BitLogicTetrominoGridSpawner(self.window, grid_logic, self.tick_speed)) 

        self.window.add_object(BitInterfaceGrid(grid_logic, display_grid = display_grid))


    def play(self) -> None:
         self.window.render()


if __name__ == "__main__":
        engine = Bit(tick_speed = -5)
        engine.create_window()
        engine.create_grid(
             rows = 25,
             columns = 40,
             display_grid = False
        )
        engine.play()