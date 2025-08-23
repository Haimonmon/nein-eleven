import sys
import pygame
import random

from typing import Set, List, Callable

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

        self.page_manager = BitPageManager(self)

       
    def get_window_events(self) -> pygame.event:
        """ Get's window events """
        return self.events
    

    def add_object(self, object: object) -> object:
        """ Make the object be part of the loop  """
        self.game_objects.append(object)
        return object
    

    def clear_objects(self) -> None:
        """ Clears the entire game objects """
        self.game_objects = []
    

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
                target_surface = self.game_surface
            else:
                target_surface = self.screen

            target_surface.fill(self.background_color)

            for game_object in self.game_objects:
                # * For logic updates objects
                if hasattr(game_object, "update"):
                    game_object.update()

                # * For logic controller game_objects
                if hasattr(game_object, "control"):
                    game_object.control(self.events)
                    
                # * For interface renderings game_objects
                if hasattr(game_object, "render"):
                    if self.crt_effect:
                        game_object.render(self.game_surface)
                    else:
                        game_object.render(self.screen)


            # * FOR THE PAGE MANAGER
            if self.page_manager.current_page:
                self.page_manager.update()
                self.page_manager.control(self.events)
                self.page_manager.render(target_surface)

             # * FOR THE CRT EFFECT
            if self.crt_effect:
                crt_surface = self.apply_scanlines(self.game_surface.copy())
                bent_surface = self.crt_bend_exaggerated(crt_surface)
                final_surface = self.apply_flicker(bent_surface)

                self.screen.blit(final_surface, (0, 0))
            
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


# * ============ DECORATORS ============

def validate_page(func: Callable):
    """ Decorator for window validation """

    def wrapper(self, name: str, page: object, *args, **kwargs):
        required_methods = ["render", "update", "control"]

        for method in required_methods:
            if not hasattr(page, method):
                raise AttributeError(f"The page '{name}' must have a callable '{method}' method.")
            
        return func(self, name, page, *args, **kwargs)
    return wrapper

# * ====================================


class BitPageManager:
    """ Handles windows single page application """
    def __init__(self, window):
        self.window = window

        # * PAGE HANDLING
        self.pages = {}

        self.current_page = None
    

    @validate_page
    def add_page(self, name: str, page_class: object, *args, **kwargs) -> object:
        """ Sotres the page on the app window """
        self.pages[name] = (page_class, args, kwargs)
        return name
    

    def set_page(self, name: str, *args, **kwargs) -> object:
        """ Switch to a page, allowing extra params """
        if name not in self.pages:
            raise ValueError(f"Page '{name}' does not exist.")

        self.window.clear_objects()

        page_class, default_args, default_kwargs = self.pages[name]

        # Merge defaults + new args
        final_args = args if args else default_args
        final_kwargs = {**default_kwargs, **kwargs}

        # Create new page instance
        self.current_page = page_class(*final_args, **final_kwargs)

        return self.current_page


    def update(self):
        if self.current_page and hasattr(self.current_page, "update"):
            self.current_page.update()


    def render(self, surface: pygame.Surface, *args):
        if self.current_page and hasattr(self.current_page, "render"):
            self.current_page.render(surface, *args)


    def control(self, events):
        if self.current_page and hasattr(self.current_page, "control"):
            self.current_page.control(events)


if __name__ == "__main__":
      window = BitInterfaceWindow()
      window.render()
      window.exit()