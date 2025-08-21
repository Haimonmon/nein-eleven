import bitEngine

class MainGame:
    """ Here lies the fun and gameplay """
    def __init__(self, main):
        self.main = main
        self.engine: bitEngine.Bit = main.engine

        self.window = main.window
        self.grid = self.engine.create_grid(columns=10)
        self.controller = self.engine.add_controller(self.grid)
        

    def render(self) -> None:
        # self.window.background_color =  "#DFA05D"
        self.engine.play()
     


if __name__ == "__main__":
      MainGame.render()