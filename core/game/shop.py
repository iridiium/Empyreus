from __future__ import annotations


class Shop:
    def __init__(self, products: list[Product]):
        self.products = products

    def get_products(self):
        return self.products


class Product:
    def __init__(
        self, name: str, icon_image: pygame.Surface, cost: dict[str:int]
    ):
        self.name = name
        self.icon_image = icon_image
        self.cost = cost

        self.cost_resources = cost.keys()
        self.cost_amounts = cost.values()
