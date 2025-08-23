import bitEngine

from typing import Literal

class MainGame:
    """ Here lies the fun and gameplay """

    def __init__(self, main, picked_gamemode: Literal["SinglePlayer", "PlayerVsPlayer", "PlayerVsAi"] = None):
        self.main = main
        self.engine: bitEngine.Bit = main.engine

        self.window = main.window

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

        if self.picked_gamemode in self.gamemodes:
            self.gamemodes.get(self.picked_gamemode)()


    def render(self, surface) -> None:
        """ Display's the main game """
        print(f"Rendering {self.picked_gamemode} . . .")

        


    def update(self) -> None:
        pass


    def control(self, events) -> None:
        pass


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
