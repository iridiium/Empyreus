from __future__ import annotations

from typing import Callable

from .player import Player


class Shop:
    def __init__(self, products: list[Product]):
        self.products = products

        self.idxs = [product.get_idx() for product in self.products]
        self.idxs_ascii = [ord(idx) for idx in self.idxs]

    def get_products(self):
        return self.products

    def get_idxs(self):
        return self.idxs

    def get_idxs_ascii(self):
        return self.idxs_ascii

    def check_product_reqs(self, player: Player, product_idx: int) -> bool:
        return self.products[product_idx - 1].check_reqs(player)


class Product:
    def __init__(self, idx, name, icon_image, cost, effect, score, effect_desc):
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

        for resource, resource_amount in self.cost:
            if player_resources[resource] < resource_amount:
                return False

        return True
