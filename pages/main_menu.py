import pygame


class MainMeny:
    def __init__(self, main):
        self.main = main

        self.window = self.main.window

        self.window_page_manager = self.main.window_page_manager

        self.options = ["START", "OPTIONS", "QUIT"]
        self.selected = 0

        self.title_font = pygame.font.SysFont("SF Pixelate", 120, bold=True)
        self.option_font = pygame.font.SysFont("SF Pixelate", 30, bold=True)

        self.text_color = (200, 200, 200)
        self.selected_color = (255, 215, 0)
        self.border_color = (200, 200, 200)
        self.selected_border_color = (255, 215, 0)

        self.fade_alpha = 10
        self.fade_speed = 2


    def render(self, surface) -> None:
        """ Display main menu options """
        self.render_main_menu(surface)

        if self.fade_alpha > 0:
            overlay = pygame.Surface(surface.get_size())
            overlay.fill((0, 0, 0))
            overlay.set_alpha(self.fade_alpha)
            surface.blit(overlay, (0, 0))


    def update(self) -> None:
        pass


    def control(self, events) -> None:
        for event in events:
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)

                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)

                elif event.key == pygame.K_RETURN:
                    option = self.options[self.selected]

                    if option == "QUIT":
                        self.main.engine.exit()

                    elif option == "START":
                        self.window_page_manager.set_page(self.main.main_game, self.main, "SinglePlayer")

                    elif option == "OPTIONS":
                        print("Options menu!")

    def render_main_menu(self, surface: pygame.Surface) -> None:
        """ Display main menu """
        surface.fill((0, 0, 0))

        screen_w, screen_h = surface.get_size()

        self.render_title(surface, "TETRIS", screen_w // 2, screen_h // 4)

        button_spacing = 80
        start_y = 300

        for i, option in enumerate(self.options):

            is_selected = i == self.selected
            color = self.selected_color if is_selected else self.text_color
            text_surface = self.option_font.render(option, True, color)

            text_rect = text_surface.get_rect(
                center=(screen_w // 2, start_y + i * button_spacing))
            button_rect = text_rect.inflate(40, 20)

            border_col = self.selected_border_color if is_selected else self.border_color
            pygame.draw.rect(surface, border_col, button_rect, 3)

            surface.blit(text_surface, text_rect)


    def render_title(self, surface, text, x, y) -> None:
        """ Display title with retro-colored letters 🍒✨ """
        retro_colors = [
            "#FF0000",  # Neon Red
            "#FF7F00",  # Orange
            "#FFFF00",  # Bright Yellow
            "#00FF00",  # Neon Green
            "#00FFFF",  # Cyan / Aqua
            "#FF00FF",  # Magenta / Hot Pink
        ]

        total_width = 0
        letters = []
        for i, char in enumerate(text):
            color = retro_colors[i % len(retro_colors)]
            letter_surface = self.title_font.render(char, True, color)
            letters.append(letter_surface)
            total_width += letter_surface.get_width()

        # Center align the whole word
        start_x = x - total_width // 2
        max_height = max(letter.get_height() for letter in letters)

        for i, letter_surface in enumerate(letters):
            surface.blit(letter_surface, (start_x, y - max_height // 2))
            start_x += letter_surface.get_width()
