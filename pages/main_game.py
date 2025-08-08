class MainGame:
    """ Here lies the fun and gameplay """
    def __init__(self, main):
        self.window = main.window

    def render(self) -> None:
        self.window.render()

if __name__ == "__main__":
      MainGame.render()