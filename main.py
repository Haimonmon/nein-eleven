import pages
import bitEngine as bit

class Tetra:
    """ Welcome to Tetra game """
    def __init__(self):
        self.window = bit.BitWindow()
        self.main_game = pages.MainGame(self)

    def start(self) -> None:
        self.window.render()


if __name__ == "__main__":
    tetris = Tetra()
    tetris.start()
