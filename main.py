import pages
import bitEngine

class Tetra:
    """ Welcome to Tetra game """
    def __init__(self):
        self.engine = bitEngine.Bit()
        self.window = self.engine.create_window()
        self.main_game = pages.MainGame(self)

    def start(self) -> None:
        self.main_game.render()
        
if __name__ == "__main__":
    tetris = Tetra()
    tetris.start()
