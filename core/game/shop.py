from __future__ import annotations

from typing import Callable

from .player import Player


class Shop:

    def __init__(self, products: list[Product]):
        self.products = products

        self.idxs = [product.get_idx() for product in self.products]
        self.idxs_ascii = [ord(idx) for idx in self.idxs]

    def get_products(self) -> list[Product]:
        return self.products

    def get_idxs(self) -> list[int]:
        return self.idxs

    def get_idxs_ascii(self) -> list[int]:
        return self.idxs_ascii

    def buy_product(self, player: Player, product_idx: int) -> None:
        product = self.products[product_idx - 1]

        # Runs the effect command, stored as an function attribute.
        product.get_effect()()

        # Grants score points from purchase to player.
        player.change_score_by(product.get_score())

        # Removes all specified resources for the product.
        player_resources = player.get_resources()
        for resource, resource_amount in product.get_cost().items():
            player_resources[resource] -= resource_amount
        player.set_resources(player_resources)

    def check_product_reqs(self, player: Player, product_idx: int) -> bool:
        # Calls function of aggregated element.
        return self.products[product_idx - 1].check_reqs(player)


class Product:

    def __init__(
        self,
        idx: str,
        name: str,
        icon_image: pygame.Surface,
        cost: dict[str, int],
        effect: Callable,
        score: int,
        effect_desc: str,
    ):
        self.idx = idx
        self.name = name
        self.icon_image = icon_image
        self.cost = cost
        self.effect = effect
        self.score = score
        self.effect_desc = effect_desc

    def get_idx(self):
        return self.idx

    def get_name(self):
        return self.name

    def get_icon_image(self):
        return self.icon_image

    def get_cost(self):
        return self.cost

    def get_effect(self):
        return self.effect

    def get_score(self):
        return self.score

    def get_effect_desc(self):
        return self.effect_desc

    def check_reqs(self, player: Player) -> bool:
        player_resources = player.get_resources()

        # Checks that every individual player resources is higher than the individual resource needed.
        for resource, resource_amount in self.cost.items():
            if player_resources[resource] < resource_amount:
                return False

        return True
