import pygame

class BitInterfaceNextPieceView:
    def __init__(self, next_piece_logic, width: int, height: int , cell_size: int = 30, position_x: int = 0, position_y: int = 0, border_color: str = "blue", border_thickness: int = 1,  num_piece_display: int = 1, background_color: str | set = None):
        self.next_piece_logic = next_piece_logic

        self.width = width
        self.height = height

        self.cell_size = cell_size

        self.position_x = position_x
        self.position_y = position_y

        self.border_color = border_color
        self.border_thickness = border_thickness
        self.background_color = background_color

        self.num_piece_display = num_piece_display


    def render(self, screen: pygame.Surface) -> None:
        """ Render piece Preview """
        self.draw_next_piece_board(screen)
        self.draw_dummy_tetromino(screen)


    def draw_next_piece_board(self, screen: pygame.surface) -> None:
        """ Draws next piece board """
        if not self.next_piece_logic:
            return

        # * Draw board
        pygame.draw.rect(
            screen, self.background_color,
            (self.position_x, self.position_y, self.width, self.height)
        )

        pygame.draw.rect(
            screen,
            self.border_color,  
            (self.position_x, self.position_y, self.width, self.height),
            width = self.border_thickness
        )


    def draw_dummy_tetromino(self, screen: pygame.Surface) -> None:
        """ Draws dummy tetrominoes, not fully controllable but for display """
        next_pieces = self.next_piece_logic.peek_next(self.num_piece_display)

        n = len(next_pieces)

        vertical_space = self.height // n

        for i, piece_key in enumerate(next_pieces):
            piece_coords = self.next_piece_logic.piece[piece_key]
            color = getattr(self.next_piece_logic, 'color', (255, 255, 255))
            border_color = (0, 0, 0)

            # Bounding box of the piece
            xs = [x for x, _ in piece_coords]
            ys = [y for _, y in piece_coords]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            piece_width = max_x - min_x + 1
            piece_height = max_y - min_y + 1

            # Center offsets
            offset_x = (self.width - piece_width * self.cell_size) // 2
            offset_y = (vertical_space - piece_height * self.cell_size) // 2 + i * vertical_space

            # * Draw blocks
            for x, y in piece_coords:
                rect = pygame.Rect(
                    self.position_x + offset_x + (x - min_x) * self.cell_size,
                    self.position_y + offset_y + (y - min_y) * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, border_color, rect, 1)


if __name__ == "__main__":
      pass