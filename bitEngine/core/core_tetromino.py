from typing import List, Tuple, Dict, Literal


class BitLogicTetromino:
    def __init__(self, grid_logic) -> None:
        self.grid_logic = grid_logic

        # * For n grams
        self.word = None
        self.piece_shape = None
        self.coordinates: List[Tuple[int, int]] = []

        self.landed = False
     
     
    def update(self) -> None:
        """ Update tetromino state """
        # print(self.word)
        pass
   

if __name__ == "__main__":
      pass