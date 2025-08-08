from core import * 
from ui import *
from utils import *

class BitEngine:
    """ The Bit's mighty Assembler """
    def __init__(self):
        self.window = None

    
    def create_window(self) -> None:
         """ """


    def create_grid(self) -> None:
        """ Creates a tetris board or grid """
        ui_grid = self.window.add_object(BitGrid())
        ui_grid_scoreboard = self.window.add_object(BitGridScoreBoard())
        grid_logic = self.window.add_object(BitGridLogics())


    def play(self) -> None:
         pass

if __name__ == "__main__":
        engine = BitEngine()