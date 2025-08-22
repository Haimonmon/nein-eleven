import sys
import pygame
import random

from typing import Set, List

class BitInterfaceWindow:
    """ Bit Engine's Window """

    def __init__(self, height: int = 300, width: int = 600, title: str = "The Bit Engine", icon: str = "favicon.png", background_color: str | Set[int] = "#1A1A1A", scanline_alpha: int = 70, bend_amount: float = 0.85, flicker_intensity: int = 20, crt_effect: bool = True) -> None:
        self.height = height
        self.width = width
        self.title = title
        self.background_color = background_color
        self.icon = f"./bitEngine/assets/{icon}"

        self.running = False

        self.screen = None

        self.events = None

        self.game_objects = []

        self.game_surface = pygame.Surface((self.width, self.height))

        # * CRT FILTER
        self.crt_effect = crt_effect

        self.scanline_alpha = scanline_alpha    
        self.bend_amount = bend_amount
        self.flicker_intensity = flicker_intensity


    def add_object(self, object: object) -> object:
        """ Make the object be part of the loop  """
        self.game_objects.append(object)
        return object
    

    def get_objects(self, name: str = None) -> List[object]:
        """ Returns objects you want to get """
        if name is None:
            return self.game_objects
        return [obj for obj in self.game_objects if obj.__class__.__name__ == name]


    def gameloop(self) -> None:
        """ Performs the whole gameloop of the game """
        pygame.font.init()
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self.events = pygame.event.get()

            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False
                    print("Goodbye and Thanks")

            if self.crt_effect:
                self.game_surface.fill(self.background_color)
            else:
                self.screen.fill(self.background_color)

            for object in self.game_objects:
                # * For logic updates objects
                if hasattr(object, "update"):
                    object.update()

                # * For logic controller objects
                if hasattr(object, "control"):
                    object.control(self.events)
                    
                # * For interface renderings objects
                if hasattr(object, "render"):
                    if self.crt_effect:
                        object.render(self.game_surface)
                    else:
                        object.render(self.screen)

            if self.crt_effect:
                crt_surface = self.apply_scanlines(self.game_surface.copy())
                bent_surface = self.crt_bend_exaggerated(crt_surface)
                final_surface = self.apply_flicker(bent_surface)

                self.screen.blit(final_surface, (0, 0))
            else:
                self.screen.blit(self.screen, (0,0))

            pygame.display.flip()
            # * Frame per Seconds
            clock.tick(120)


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


    def apply_scanlines(self, surface: pygame.Surface) -> pygame.Surface:
        """ Draw scanlines over the surface """
        line_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        width, height = surface.get_size()

        for y in range(0, height, 2):
            alpha = self.scanline_alpha
            pygame.draw.line(line_surface, (0, 0, 0, alpha), (0, y), (width, y))
            
        surface.blit(line_surface, (0, 0))

        return surface


    def crt_bend_fast(self, surface: pygame.Surface) -> pygame.Surface:
        """Fake CRT screen curvature using scaling"""
        width, height = surface.get_size()

        small = pygame.transform.smoothscale(surface, (width, int(height * self.bend_amount)))

        bent = pygame.transform.smoothscale(small, (width, height))

        return bent
    

    def crt_bend_exaggerated(self, surface):
        width, height = surface.get_size()
        bent = pygame.Surface((width, height), pygame.SRCALPHA)

        for y in range(height):
            # factor: more bending near top/bottom
            factor = 1.2 - 0.40 * ((y / height - 0.5)**2)
            
            line = pygame.transform.smoothscale(surface.subsurface((0, y, width, 1)), (int(width * factor), 1))

            x_offset = (width - line.get_width()) // 2

            bent.blit(line, (x_offset, y))
            
        return bent


    def apply_flicker(self, surface: pygame.Surface) -> pygame.Surface:
        """Add slight flicker to simulate CRT"""
        flicker_surface = surface.copy()

        flicker_alpha = random.randint(-self.flicker_intensity, self.flicker_intensity)

        flicker_overlay = pygame.Surface(flicker_surface.get_size(), pygame.SRCALPHA)

        flicker_overlay.fill((0, 0, 0, max(0, flicker_alpha)))

        flicker_surface.blit(flicker_overlay, (0, 0))

        return flicker_surface


    def exit(self) -> None:
        """ exit bit engine windows """
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
      window = BitInterfaceWindow()
      window.render()
      window.exit()