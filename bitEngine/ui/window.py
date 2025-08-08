import sys
import pygame
from pathlib import Path

class BitWindow:
    """ Bit Engine's Window """
    def __init__(self, height: int = 300, width: int = 600, title: str = "The Bit Engine", icon: str = "favicon.png") -> None:
        self.__height = height
        self.__width = width
        self.__title = title
        self.__icon = f"./bitEngine/assets/{icon}"

        self.running = False
        self.screen = None
        self.game_objects = []


    def add_object(self, object: object) -> None:
        """ Make the object be part of the loop  """
        self.game_objects.append(object)


    def render(self) -> None:
        """ Renders bit engine windows """
        # * Window Screen
        self.screen = pygame.display.set_mode((self.__width, self.__height))

        # * Window Title
        pygame.display.set_caption(self.__title)

        # * Window Icon image
        icon = pygame.image.load(self.__icon)
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