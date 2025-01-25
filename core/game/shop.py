from __future__ import annotations

from typing import Callable


class Shop:
    def __init__(self, products: list[Product]):
        self.products = products

    def get_products(self):
        return self.products

    def render_to(self, window):
        pass


class Product:
    def __init__(self, name, icon_image, cost, effect, effect_desc):
        self.name = name
        self.icon_image = icon_image
        self.cost = cost
        self.effect = effect
        self.effect_desc = effect_desc

    def get_name(self):
        return self.name

    def get_icon_image(self):
        return self.icon_image

    def get_cost(self):
        return self.cost

    def get_effect(self):
        return self.effect

    def get_effect_desc(self):
        return self.effect_desc
