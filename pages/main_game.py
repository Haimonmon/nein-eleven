import pygame
import bitEngine

from typing import Literal

class MainGame:
    """ Here lies the fun and gameplay """
    def __init__(self, main, picked_gamemode: Literal["SinglePlayer", "PlayerVsPlayer", "PlayerVsAi"] = None):
        self.main = main
        self.engine: bitEngine.Bit = main.engine

        self.window = main.window

        self.window_page_manager = self.main.window_page_manager

        self.tetromino_colors = [
            "#FF0000",  # Neon Red
            "#FF7F00",  # Orange
            "#FFFF00",  # Bright Yellow
            "#00FF00",  # Neon Green
            "#00FFFF",  # Cyan / Aqua
            "#0000FF",  # Electric Blue
            "#FF00FF",  # Magenta / Hot Pink
            "#FF1493",  # Deep Pink
            "#7CFC00",  # Lawn Green
            "#1E90FF",  # Dodger Blue
            "#FFD700",  # Gold (classic arcade shine)
            "#FF69B4"   # Hot Pink (extra pop)
        ]
        
        self.picked_gamemode = picked_gamemode

        self.gamemodes = {
            "SinglePlayer": self.create_single_player_match,
            "PlayerVsPlayer": self.create_single_player_match,
            "PlayerVsAi": self.create_single_player_match
        }

        self.paused = False
        self.pause_options = ["CONTINUE", "QUIT"]
        self.pause_selected = 0
        self.font = pygame.font.SysFont("SF Pixelate", 40)

        if self.picked_gamemode in self.gamemodes:
            self.gamemodes.get(self.picked_gamemode)()



    def render(self, surface) -> None:
        """ Display's the main game """
        if self.window.paused:
            self.display_pause_menu(surface)

        
    def update(self) -> None:
        pass


    def control(self, events) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.window.paused = not self.window.paused

                if self.window.paused:
                    if event.key == pygame.K_LEFT:
                        self.pause_selected = (self.pause_selected - 1) % len(self.pause_options)

                    elif event.key == pygame.K_RIGHT:
                        self.pause_selected = (self.pause_selected + 1) % len(self.pause_options)

                    elif event.key == pygame.K_RETURN:
                        self.handle_pause_selection()


    def display_pause_menu(self, surface: pygame.Surface) -> None:
        """ Display's pause menu with options """

        overlay = pygame.Surface(surface.get_size()) 
        overlay.set_alpha(180) 
        overlay.fill((0, 0, 0)) 
        surface.blit(overlay, (0, 0))

        # * PAUSED TEXT
        pause_font = pygame.font.SysFont("SF Pixelate", 100, bold=True)
        pause_text = pause_font.render("PAUSED", True, (255, 255, 0))
        pause_rect = pause_text.get_rect(
            center=(surface.get_width() // 2, surface.get_height() // 2 - 100))
        surface.blit(pause_text, pause_rect)


        option_font = pygame.font.SysFont("SF Pixelate", 40, bold=True)
        rendered_options = []
        total_width = 0
        spacing = 80  


        for i, option in enumerate(self.pause_options):
            is_selected = (i == self.pause_selected)

            if is_selected:
                color = (255, 215, 0)
            else: 
                color = (255, 255, 255) 

            text = option_font.render(option, True, color)

            rendered_options.append((text, color, is_selected))

            total_width += text.get_width() + 40  

            if i < len(self.pause_options) - 1:
                total_width += spacing


        start_x = pause_rect.centerx - total_width // 2
        y = pause_rect.bottom + 80


        for i, (text_surface, color, is_selected) in enumerate(rendered_options):
            text_rect = text_surface.get_rect(
                midleft=(start_x + 20, y))  # leave padding
            button_rect = pygame.Rect(
                text_rect.left - 20,
                text_rect.top - 10,
                text_rect.width + 40,
                text_rect.height + 20
            )

            border_color = (255, 215, 0) if is_selected else (255, 255, 255)
            pygame.draw.rect(surface, border_color, button_rect, 3)

            surface.blit(text_surface, text_rect)

            start_x += button_rect.width + spacing


    def handle_pause_selection(self) -> None:
        """ Entery key bindings """
        option = self.pause_options[self.pause_selected]
        if option == "CONTINUE":
            self.window.paused = False
        elif option == "QUIT":
            self.window.paused = False
            self.window_page_manager.set_page(self.main.main_menu, self.main)


    def create_single_player_match(self) -> None:
        """ Creates the single player match """
        print("Creating .. ")

        self.piece_viewer = self.engine.create_piece_viewer(width = 170, height = 300, position_x = 670, position_y = 370, num_piece_display = 2, border_color = "gold")
        self.grid = self.engine.create_grid(piece_view = self.piece_viewer["piece_view_logic"], columns=10, rows=20, position_y = 70, position_x = 300, display_grid = False, border_color = "blue")
        self.scoreboard = self.engine.create_scoreboard(self.grid["grid_line_cleaner"], width = 170, height = 150, position_x = 670, position_y = 70, border_color = "gold")
        self.controller = self.engine.add_controller(self.grid)

        self.window.background_color =  "black"
        self.grid["grid_spawner"].change_tetromino_appearance(self.tetromino_colors, (0,0,0), "blue")

    
  
        
     

if __name__ == "__main__":
      MainGame.render()

      # * X = 300, Y = 70 for centering 🤓☝️
