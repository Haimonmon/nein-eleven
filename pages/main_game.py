import BitEngine

class MainGame:
    """ Here lies the fun and gameplay """
    def __init__(self, main):
        self.window: BitEngine.BitWindow = main.window
        self.grid: BitEngine.BitGrid = BitEngine.BitGrid(columns = 25, cell_size = 30, display_grid = True, border_width = 3) 
        

    def render(self) -> None:
        # self.window.background_color =  "#DFA05D"
        self.window.add_object(self.grid)
     


if __name__ == "__main__":
      MainGame.render()