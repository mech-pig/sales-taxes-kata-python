from dataclasses import dataclass
from decimal import Decimal


class InvalidItemError(Exception):
    pass


class ItemError:
    class NonPositiveQuantity(Exception):
        def __init__(self, value):
            super().__init__(f'quantity must be positive: {value}')

    class NegativeUnitPrice(Exception):
        def __init__(self, value):
            super().__init__(f'unit_price can\'t be negative: {value}')


@dataclass
class Item:
    quantity: int
    product_name: str
    unit_price: Decimal


def create(quantity: int, product_name: str, unit_price: Decimal):
    """ Creates an item.

    Item quantity must be greater than zero, unit_price can't be less than
    zero.
    """
    if quantity <= 0:
        raise ItemError.NonPositiveQuantity(quantity)

    if unit_price < 0:
        raise ItemError.NegativeUnitPrice(unit_price)

    return Item(
        quantity=quantity,
        product_name=product_name,
        unit_price=unit_price,
    )
