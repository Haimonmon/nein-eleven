import bitEngine

class MainGame:
    """ Here lies the fun and gameplay """
    def __init__(self, main):
        self.main = main
        self.engine: bitEngine.Bit = main.engine

        self.window = main.window
        self.piece_viewer = self.engine.create_piece_viewer(width = 170, height = 300, position_x = 670, position_y = 370, num_piece_display = 2, border_color = "gold")
        self.grid = self.engine.create_grid(piece_view = self.piece_viewer["piece_view_logic"], columns=10, rows=20, position_y = 70, position_x = 300, display_grid = False, border_color = "blue")
        self.controller = self.engine.add_controller(self.grid)
        

    def render(self) -> None:
        tetromino_colors =  [
            "#FFD700",  # gold
            "#FFB700",  # rich gold
            "#FFA500",  # orange-gold
            "#FFF8DC",  # cornsilk (soft gold highlight)
            "#F5DEB3",  # wheat (warm golden tone)
            "#FFFACD",  # lemon chiffon (light reflection)
            "#FFDAB9",  # peach puff (soft highlight)
            "#FFF5E1",  # champagne glow
            "#E6BE8A",  # antique gold
            "#B8860B",  # dark goldenrod (deep gold shadow)
            "#DAA520",  # goldenrod
            "#FFFAF0"   # floral white (flash reflection)
        ]

        self.window.background_color =  "black"
        self.grid["grid_spawner"].change_tetromino_appearance(tetromino_colors, (0,0,0), "blue")
        self.engine.play()
        
     

if __name__ == "__main__":
      MainGame.render()

      # * X = 300, Y = 70 for centering 🤓☝️
