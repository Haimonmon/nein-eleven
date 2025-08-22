import pygame

class BitInterfaceNextPieceView:
    def __init__(self, next_piece_logic):
        self.next_piece_logic = next_piece_logic
    

    def render(self, screen: pygame.Surface) -> None:
        """ Render piece Preview """
        pass

    def draw_next_piece_board(self) -> None:
        """ Draws next piece board """