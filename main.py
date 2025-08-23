import pages
import bitEngine

class Tetra:
    """ Welcome to Tetra game """
    def __init__(self):
        self.engine = bitEngine.Bit()

        self.created_window = self.engine.create_window(crt_effect = True)
        self.window = self.created_window["window"]
        self.window_page_manager = self.created_window["window_page_manager"]

        self.main_menu = self.window_page_manager.add_page("main_menu", pages.MainMeny)
        self.main_game = self.window_page_manager.add_page("main_game", pages.MainGame)


    def start(self) -> None:
        self.window_page_manager.set_page(self.main_menu, self)
        self.engine.play()


if __name__ == "__main__":
    tetris = Tetra()
    tetris.start()

""" 
TODO:
? 1. Fix Shift Down

"""
