import pygame.freetype

from ..game.board import Board
from ..game.player import Player, PlayerList


class UIText:

    def __init__(
        self,
        board: Board,
        players: PlayerList,
        font: pygame.freetype.Font,
        font_bold: pygame.freetype.Font,
        font_size: int,
        font_bold_size: int,
        text_colour: tuple[int, int, int],
    ):
        self.board = board
        self.players = players
        self.font = font
        self.font_bold = font_bold
        self.font_size = font_size
        self.font_bold_size = font_bold_size
        self.text_colour = text_colour

        self.board_pos = self.board.get_pos()
        self.board_pos_end = self.board.get_pos_end()
        self.tile_border_size = self.board.get_tile_border_size()
        self.tile_size = self.board.get_tile_size()
        self.window_size = self.board.get_window_size()

    def render_to(
        self,
        window: pygame.Surface,
        mouse_pos: bool,
        curr_player: Player,
    ) -> None:
        self.curr_player = self.players.get_curr()

        self.render_player_list_text_to(window)
        self.render_player_resource_text_to(window, mouse_pos)
        self.render_player_turn_text_to(window)
        self.render_status_text_to(window)
        self.render_title_text_to(window)

    def render_player_list_text_to(self, window: pygame.display) -> None:
        for player_num, player in enumerate(self.players.get_list()):
            # Renders the individual player's line of text.
            player_list_text_pos = (
                self.board.get_pos_end()[0] + 0.3 * self.tile_size[0],
                self.board_pos[1]
                + (player_num * (self.tile_border_size[1] + self.font_size)),
            )

            # Renders player image.
            window.blit(
                pygame.transform.scale(
                    player.get_image(),
                    (
                        self.font_size,
                        self.font_size,
                    ),
                ),
                player_list_text_pos,
            )

            # Renders player index, name and score.
            self.font.render_to(
                window,
                (
                    player_list_text_pos[0] + 2 * self.font_size,
                    player_list_text_pos[1],
                ),
                f"P{player_num + 1} ({player.get_name()}): {player.get_score()}",
                player.get_colour(),
            )

    def render_player_resource_text_to(
        self,
        window: pygame.display,
        mouse_pos: tuple[int, int],
    ) -> None:
        curr_player_resources = self.curr_player.get_resources()

        # Renders a hitbox rectangle for detecting hovering.
        resource_text_rect = pygame.Rect(
            20,
            0.75 * self.board_pos_end[1],
            self.board.get_pos()[0],
            (len(curr_player_resources) + 0.5) * 7 * self.font_size,
        )

        # Renders title text.
        self.font.render_to(
            window,
            (
                resource_text_rect.left,
                resource_text_rect.top - self.font_size,
            ),
            f"Resources (hover below):",
            self.text_colour,
        )

        # Handles the hiding/showing of resources depending on whether the mouse is hovering on them.
        if resource_text_rect.collidepoint(mouse_pos):
            for resource_index, (resource_name, resource_amount) in enumerate(
                curr_player_resources.items()
            ):
                # Renders picture icon image.
                window.blit(
                    pygame.transform.scale(
                        self.board.get_icon_sprite_sheet().get_sprite_from_name(
                            resource_name
                        ),
                        (self.font_size, self.font_size),
                    ),
                    (
                        resource_text_rect.left,
                        resource_text_rect.top
                        + (resource_index + 0.5) * 1.5 * self.font_size,
                    ),
                )

                # Renders text for amount.
                self.font.render_to(
                    window,
                    (
                        resource_text_rect.left + 2 * self.font_size,
                        resource_text_rect.top
                        + (resource_index + 0.5) * 1.5 * self.font_size,
                    ),
                    f"{resource_name}: {curr_player_resources[resource_name]}",
                    self.text_colour,
                )

    def render_player_turn_text_to(self, window: pygame.display) -> None:
        # Renders turn counter.
        self.font.render_to(
            window,
            (20, self.board_pos[1]),
            f"Turns taken: {self.players.get_turns_taken()}",
            self.text_colour,
        )

        # Renders current turn tracker.
        self.font.render_to(
            window,
            (
                20,
                self.board_pos[1] + self.tile_border_size[1] + self.font_size,
            ),
            f"Player {self.curr_player.get_num() + 1}'s turn.",
            self.text_colour,
        )

        # Renders number of actions left for the current player.
        self.font.render_to(
            window,
            (
                20,
                self.board_pos[1]
                + 2 * (self.tile_border_size[1] + self.font_size),
            ),
            f"Actions left: {self.curr_player.get_actions_left()}",
            self.text_colour,
        )

    def render_status_text_to(self, window: pygame.display) -> None:
        # Renders feedback on the action last taken (success / reason of failure).
        self.font.render_to(
            window,
            (20, 50),
            self.players.get_status(),
            self.text_colour,
        )

    def render_title_text_to(self, window: pygame.display) -> None:
        title_text = self.font_bold.render(
            "EMPYREUS", self.text_colour, size=self.font_bold_size
        )
        title_text[1].center = (self.window_size[0] / 2, self.board_pos[1] / 2)

        window.blit(title_text[0], title_text[1])
