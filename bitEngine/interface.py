from .ui import *

class BitInterfaceMaker:
    def __init__(self, engine):
        self.__engine = engine

    def create_window(self, height: int = 740, width: int = 1200, title: str = "The Bit Engine", icon: str = "favicon.png", background_color: str | set[int] = "#1A1A1A", scanline_alpha: int = 70, bend_amount: float = 0.85, flicker_intensity: int = 20, crt_effect: bool = False) -> BitInterfaceWindow:
        """ Creates a window """

        window = BitInterfaceWindow(height, width, title, icon, background_color, scanline_alpha, bend_amount, flicker_intensity, crt_effect)

        self.__engine.window = window
        return window