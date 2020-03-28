from dataclasses import dataclass


class InvalidItemError(Exception):
    pass


@dataclass
class Item:
    quantity: int
    product_name: str
