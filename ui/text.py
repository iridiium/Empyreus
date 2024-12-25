import pygame.freetype


class UIText:
    def __init__(
        self,
        board,
        font,
        font_bold,
        font_size,
        font_bold_size,
        players,
        text_colour,
    ):
        self.board = board
        self.font = font
        self.font_bold = font_bold
        self.font_size = font_size
        self.font_bold_size = font_bold_size
        self.players = players
        self.text_colour = text_colour

        self.board_pos = self.board.get_pos()
        self.tile_border_size = self.board.get_tile_border_size()
        self.tile_size = self.board.get_tile_size()
        self.window_size = self.board.get_window_size()

    def render_player_hud_text_on(self, window, total_turns) -> None:
        for player_num, player in enumerate(self.players.get_list()):
            player_hud_text_left = (
                10 + self.board.get_end_pos()[0] + 0.5 * self.tile_size[0]
            )
            player_hud_text_top = self.board_pos[1] + (
                player_num * (self.tile_border_size[1] + self.font_size)
            )
            self.font.render_to(
                window,
                (player_hud_text_left, player_hud_text_top),
                f"Player {player_num + 1}:",
                self.text_colour,
            )

            player_image = player.get_image()
            player_image_rect = player_image.get_rect()

            player_image_rect.topleft = (
                player_hud_text_left + 4 * self.font_size,
                player_hud_text_top,
            )
            player_image_rect.size = (self.font_size, self.font_size)
            window.blit(player.get_image(), player_image_rect)

    def render_on(self, window, total_turns, curr_player) -> None:
        self.render_player_hud_text_on(window, total_turns)

        title_text = self.font_bold.render(
            "Empyreus", self.text_colour, size=self.font_bold_size
        )
        title_text_rect = title_text[0].get_rect(
            center=(self.window_size[0] / 2, (self.board_pos[1] / 2))
        )
        window.blit(title_text[0], title_text_rect)

        self.font.render_to(
            window,
            (10, self.board_pos[1]),
            f"Turns elapsed: {total_turns}",
            self.text_colour,
        )

        self.font.render_to(
            window,
            (
                10,
                self.board_pos[1] + self.font_size + self.tile_border_size[1],
            ),
            f"Player {curr_player.get_num() + 1}'s turn.",
            self.text_colour,
        )
