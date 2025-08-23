import pygame


class MainMeny:
    def __init__(self, main):
        self.main = main

        self.window = self.main.window

        self.window_page_manager = self.main.window_page_manager

        self.options = ["START", "OPTIONS", "QUIT"]
        self.selected = 0

        self.window_page_manager.set_page("main_game", self.main, "SinglePlayer")


    def render(self, surface) -> None:
        """ Display main menu options """
        pass


    def update(self) -> None:
        pass


    def control(self, events) -> None:
        pass