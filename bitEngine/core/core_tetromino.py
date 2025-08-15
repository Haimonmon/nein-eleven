from typing import List, Tuple, Dict, Literal


class BitLogicTetromino:
    """ Tetromino functionalities """
    def __init__(self, grid_logic, width, height, piece_shape, coordinates) -> None:
        self.grid_logic = grid_logic

        # * For n grams
        self.word = None

        # * By Blocks
        self.width = width
        self.height = height

        # * Piece Name
        self.piece_shape = piece_shape

        self.coordinates: List[Tuple[int, int]] = coordinates

        self.landed = False
     
     
    def update(self) -> None:
        """ Update tetromino state """
        # print(self.word)
        pass
   

if __name__ == "__main__":
      pass