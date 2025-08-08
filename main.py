import pages
import BitEngine

class Tetra:
    """ Welcome to Tetra game """
    def __init__(self):
        self.engine = BitEngine
        self.window = self.engine.BitWindow(740, width = 1200)
        self.main_game = pages.MainGame(self)

    def start(self) -> None:
        self.main_game.render()
        self.window.render()
       
        

if __name__ == "__main__":
    tetris = Tetra()
    tetris.start()
