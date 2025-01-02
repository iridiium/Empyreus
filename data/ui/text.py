import pygame.freetype

from ..game.board import Board
from ..game.player import Player, PlayerList


class UIText:
    def __init__(
        self,
        board: Board,
        font: pygame.freetype.Font,
        font_bold: pygame.freetype.Font,
        font_size: int,
        font_bold_size: int,
        players: PlayerList,
        text_colour: tuple[int, int, int],
    ):
        self.board = board
        self.font = font
        self.font_bold = font_bold
        self.font_size = font_size
        self.font_bold_size = font_bold_size
        self.players = players
        self.text_colour = text_colour

        self.board_pos = self.board.get_pos()
        self.board_pos_end = self.board.get_pos_end()
        self.tile_border_size = self.board.get_tile_border_size()
        self.tile_size = self.board.get_tile_size()
        self.window_size = self.board.get_window_size()

    def render_to(
        self,
        window: pygame.display,
        total_turns: int,
        curr_player: Player,
        mouse_pos: bool,
    ) -> None:
        self.render_title_text_to(window)

        self.render_player_list_text_to(window)

        self.render_player_resource_text_to(window, curr_player, mouse_pos)

        self.render_player_turn_text_to(window, total_turns, curr_player)

    def render_player_list_text_to(self, window: pygame.display) -> None:
        for player_num, player in enumerate(self.players.get_list()):
            player_hud_text_left = (
                self.board.get_pos_end()[0] + 0.4 * self.tile_size[0]
            )
            player_hud_text_top = self.board_pos[1] + (
                player_num * (self.tile_border_size[1] + self.font_size)
            )
            self.font.render_to(
                window,
                (player_hud_text_left, player_hud_text_top),
                f"Player {player_num + 1} ({player.get_name()}):",
                player.get_colour(),
            )

            player_image = player.get_image()
            player_image_rect = player_image.get_rect()

            player_image_rect.topleft = (
                player_hud_text_left + 9 * self.font_size,
                player_hud_text_top,
            )
            player_image_rect.size = (self.font_size, self.font_size)
            window.blit(player_image, player_image_rect)

    def render_player_resource_text_to(
        self,
        window: pygame.display,
        curr_player: Player,
        mouse_pos: tuple[int, int],
    ) -> None:
        curr_player_resources = curr_player.get_resources()

        resource_text_rect = pygame.Rect(
            20,
            0.75 * self.board_pos_end[1],
            self.board.get_pos()[0],
            (len(curr_player_resources) + 0.5) * 1.5 * self.font_size,
        )

        self.font.render_to(
            window,
            (
                resource_text_rect.left,
                resource_text_rect.top - self.font_size,
            ),
            f"Resources (hover to show):",
            self.text_colour,
        )

        if resource_text_rect.collidepoint(mouse_pos):
            for resource_index, (resource_name, resource_attrs) in enumerate(
                curr_player_resources.items()
            ):
                resource_icon_image = resource_attrs["icon_image"]

                resource_icon_image_rect = pygame.Rect(
                    resource_text_rect.left,
                    resource_text_rect.top
                    + (resource_index + 0.5) * 1.5 * self.font_size,
                    self.font_size,
                    self.font_size,
                )
                window.blit(resource_icon_image, resource_icon_image_rect)

                self.font.render_to(
                    window,
                    (
                        20 + 2 * self.font_size,
                        0.75 * self.board_pos_end[1]
                        + (resource_index + 0.5) * 1.5 * self.font_size,
                    ),
                    f"{resource_name}: {curr_player_resources[resource_name]["amount"]}",
                    self.text_colour,
                )

    def render_player_turn_text_to(
        self, window: pygame.display, total_turns: int, curr_player: Player
    ) -> None:
        self.font.render_to(
            window,
            (20, self.board_pos[1]),
            f"Turns elapsed: {total_turns}",
            self.text_colour,
        )

        self.font.render_to(
            window,
            (
                20,
                self.board_pos[1] + self.font_size + self.tile_border_size[1],
            ),
            f"Player {curr_player.get_num() + 1}'s turn.",
            self.text_colour,
        )

    def render_title_text_to(self, window: pygame.display) -> None:
        title_text = self.font_bold.render(
            "Empyreus", self.text_colour, size=self.font_bold_size
        )
        title_text_rect = title_text[0].get_rect(
            center=(self.window_size[0] / 2, (self.board_pos[1] / 2))
        )
        window.blit(title_text[0], title_text_rect)
