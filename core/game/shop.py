from __future__ import annotations

from typing import Callable


class Shop:
    def __init__(self, products: list[dict]):
        self.products = products

    def get_products(self):
        return self.products

    def render_to(self, window):
        pass
