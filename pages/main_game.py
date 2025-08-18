import bitEngine

class MainGame:
    """ Here lies the fun and gameplay """
    def __init__(self, main):
        self.main = main
        self.window: bitEngine.BitInterfaceWindow = main.window
        self.grid = self.main.engine.create_grid()
        # self.grid: bitEngine.BitInterfaceGrid = bitEngine.BitInterfaceGrid(columns = 25, cell_size = 30, display_grid = True, border_width = 3) 
        

    def render(self) -> None:
        # self.window.background_color =  "#DFA05D"
        self.main.engine.play()
     


if __name__ == "__main__":
      MainGame.render()