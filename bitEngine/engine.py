"""
Basically the heart of the engine
"""

import sys
import pygame

from .ui import *
from .core import *
from .utils import *

from typing import Callable, List

from .interface import BitInterfaceMaker
from .tetris_maker import BitTetrisMaker

class BruhTheresNoWindows(Exception):
    """ Raised when the window object is missing. """
    def __init__(self, message = "Bruh... there's literally no window to work with!"):
        super().__init__(message)


# * ============ DECORATORS ============

def require_window(func: Callable):
    """ Decorator for window validation """
    def wrapper(self, *args, **kwargs):
        if not self.window:
            raise BruhTheresNoWindows()
        return func(self, *args, **kwargs)
    return wrapper


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
    def __init__(self, engine):
        self.engine = engine

        # * PAGE HANDLING
        self.pages = {}

        self.current_page = None


    @validate_page
    def add_page(self, name: str, page_class: object, *args, **kwargs) -> object:
        """ Adds the page on the app window """
        self.pages[name] = (page_class, args, kwargs)
        return name


    def set_page(self, name: str, *args, **kwargs) -> object:
        """ Switch to a page, allowing extra params """
        if name not in self.pages:
            raise ValueError(f"Page '{name}' does not exist.")

        self.engine.clear_objects()

        page_class, default_args, default_kwargs = self.pages[name]

        # * Merge defaults + new args
        final_args = args if args else default_args
        final_kwargs = {**default_kwargs, **kwargs}

        # * Create new page instance
        self.current_page = page_class(*final_args, **final_kwargs)

        return self.current_page


    def update(self):
        if self.current_page and hasattr(self.current_page, "update"):
            self.current_page.update()


    def render(self, surface, *args):
        if self.current_page and hasattr(self.current_page, "render"):
            self.current_page.render(surface, *args)


    def control(self, events):
        if self.current_page and hasattr(self.current_page, "control"):
            self.current_page.control(events)


class Bit:
    """ The Bit's mighty Assembler """
    def __init__(self):
        self.window = None

        self.__running = False
        self.paused = False

        self.events = None

        self.game_objects = []

        # * BIT PAGE MANAGING ENGINE
        self.__page_manager = BitPageManager(self)

        # * BIT USER INTERFACE ENGINE
        self.__ui_maker = BitInterfaceMaker(self)

        # * BIT TETRIS LEVEL ENGINE
        self.__tetris_maker = BitTetrisMaker(self)


    def ui_maker(self) -> BitInterfaceMaker:
        """
        Helps you to make user interface of the game application.

        Returns: 
            BitInterfaceWindow: A Class whos responsible for making user interfaces of the application.

        Example Usage:
            ui_maker
        """
        return self.__ui_maker


    @require_window
    def page_manager(self) -> BitPageManager:
        """
        Helps you to manage single page application
        
        Returns:
            BitPageManager: A Class whos responsible for managing application pages.
        """
        return self.__page_manager


    @require_window
    def tetris_maker(self, tick_speed: int = 7) -> BitTetrisMaker:
        """
        Helps you to create the tetris level round easily.

        Parameters:
            tick_speed (int, optional): How fast the game round clocks ticks in seconds.
        
        Returns:
            BitTetrisMaker: A Class whos responsible for making tetris rounds or levels.
       
        Example Usage:
            ```python
            level_maker = tetris_maker()

            level_maker.create_grid()
            ```
        """
        self.__tetris_maker.tick_speed = tick_speed * 100
        return self.__tetris_maker


    def add_object(self, object: object) -> object:
        """ Make the object be part of the gameloop  """
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


    @require_window
    def _gameloop(self) -> None:
        """ Performs the whole gameloop of the game """
        pygame.font.init()
        clock = pygame.time.Clock()
        self.__running = True
        self.paused = False

        while self.__running:
            self.events = pygame.event.get()

            for event in self.events:
                if event.type == pygame.QUIT:
                    self.__running = False

            if self.window.crt_effect:
                target_surface = self.window.game_surface
            else:
                target_surface = self.window.screen

            target_surface.fill(self.window.background_color)
            
            # * UPDATES ONLY WHEN NOT PAUSED 🤓☝️
            if not self.paused:
                for game_object in self.game_objects:
                    # * For logic updates objects
                    if hasattr(game_object, "update"):
                        game_object.update()

                    # * For logic controller game_objects
                    if hasattr(game_object, "control"):
                        game_object.control(self.events)
                        
                    # * For interface renderings game_objects
                    if hasattr(game_object, "render"):
                        game_object.render(target_surface)
                     

            # * FOR THE PAGE MANAGER
            if self.__page_manager and self.__page_manager.current_page:
                self.__page_manager.update()
                self.__page_manager.control(self.events)
                self.__page_manager.render(target_surface)


            # * FOR THE CRT EFFECT
            if self.window.crt_effect:
                crt_surface = self.window.apply_scanlines(self.window.game_surface.copy())
                bent_surface = self.window.crt_bend_exaggerated(crt_surface)
                final_surface = self.window.apply_flicker(bent_surface)

                self.window.screen.blit(final_surface, (0, 0))
            
            pygame.display.flip()
            # * Frame per Seconds
            clock.tick(120)

    
    def play(self) -> None:
        """ Renders bit engine windows """
        self.window = self.__ui_maker.create_window()
        self.window.render()
        self._gameloop()

    
    def exit(self) -> None:
        """ exit bit engine windows """
        self.__running = False
        print("Goodbye and Thanks!, much love from BitEngine <3")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
        engine = Bit(tick_speed=-2)
        window = engine.create_window()
        grid = engine.create_grid()
        controller = engine.add_controller(grid)
        engine.play()