import sys
import pygame
from typing import Set
from pathlib import Path
class BitWindow:
    """ Bit Engine's Window """

    def __init__(self, height: int = 300, width: int = 600, title: str = "The Bit Engine", icon: str = "favicon.png", background_color: str | Set[int] = "#1A1A1A") -> None:
        self.height = height
        self.width = width
        self.title = title
        self.background_color = background_color
        self.icon = f"./bitEngine/assets/{icon}"

        self.running = False
        self.screen = None
        self.game_objects = []


    def add_object(self, object: object) -> object:
        """ Make the object be part of the loop  """
        self.game_objects.append(object)
        return object

    def render(self) -> None:
        """ Renders bit engine windows """
        # * Window Screen
        self.screen = pygame.display.set_mode((self.width, self.height))

        # * Window Title
        pygame.display.set_caption(self.title)

        # * Window Icon image
        icon = pygame.image.load(self.icon)
        pygame.display.set_icon(icon)

        self.gameloop()


    def gameloop(self) -> None:
        """ Performs the whole gameloop of the game """
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    print("Goodbye and Thanks")

            self.screen.fill(self.background_color)

            for object in self.game_objects:
                if hasattr(object, "update"):
                    object.update()
                if hasattr(object, "render"):
                    object.render(self.screen)

            pygame.display.flip()
            # * Frame per Seconds
            clock.tick(60)


    def exit(self) -> None:
        """ exit bit engine windows """
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
      window = BitWindow()
      window.render()
      window.exit()