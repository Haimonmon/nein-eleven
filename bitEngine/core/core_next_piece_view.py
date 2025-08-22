import random 

from typing import Dict, List, Tuple

class BitLogicNextPiece:
    def __init__(self, max_piece_queue: int = 3):
        self.max_piece_queue = max_piece_queue

        self.piece: Dict[str, List[Tuple[int, int]]] = {
            "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
            "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
            "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
            "L": [(0, 0), (0, 1), (0, 2), (1, 2)],
            "J": [(1, 0), (1, 1), (1, 2), (0, 2)],
            "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
            "Z": [(0, 0), (1, 0), (1, 1), (2, 1)]
        }

        self.piece_queue = []

        for _ in range(self.max_piece_queue):
            self.insert_piece()

        
    def get_piece(self) -> None:
        """ get first piece """
        return self.piece_queue.pop(0)
    

    def update(self) -> None:
        """ keeps the queue filled """
        while len(self.piece_queue) < self.max_piece_queue:
            self.insert_piece()


    def insert_piece(self) -> None:
        """ insert on the last piece """
        new_piece = random.choice(list(self.piece.keys()))
        self.piece_queue.append(new_piece)

        if len(self.piece_queue) > self.max_piece_queue:
            self.piece_queue.pop(0)


    def peek_next(self, n: int = 1):
        """ Look at the next n pieces without removing """
        return self.piece_queue[:n]


if __name__ == "__main__":
      piece_view = BitLogicNextPiece(5)
      piece_view.update()
      print(piece_view.get_piece())
      piece_view.update()
   