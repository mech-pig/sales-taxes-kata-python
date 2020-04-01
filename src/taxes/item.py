from dataclasses import dataclass
from decimal import Decimal


class InvalidItemError(Exception):
    pass


@dataclass
class Item:
    quantity: int
    product_name: str
    unit_price: Decimal
