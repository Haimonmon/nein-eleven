from .core import * 
from .ui import *
from .utils import *

from typing import Type

class BruhTheresNoWindows(Exception):
    """Raised when the window object is missing."""
    def __init__(self, message="Bruh... there's literally no window to work with!"):
        super().__init__(message)


class BitEngine:
    """ The Bit's mighty Assembler """
    def __init__(self):
        self.window = None

    
    def create_window(self) -> None:
         """ Creates a tetris window """
         self.window = BitInterfaceWindow(height = 740, width = 1200)


    def create_grid(self) -> None:
        """ Creates a tetris board or grid """
        if not self.window:
             raise BruhTheresNoWindows()
        
        grid_logic = self.window.add_object(BitLogicGrid(columns = 25))
        grid_spawner_logic = self.window.add_object(BitLogicTetrominoGridSpawner(self.window, grid_logic)) 

        ui_grid = self.window.add_object(BitInterfaceGrid(grid_logic, display_grid = True))


    def play(self) -> None:
         self.window.render()


if __name__ == "__main__":
        engine = BitEngine()
        engine.create_window()
        engine.create_grid()
        engine.play()