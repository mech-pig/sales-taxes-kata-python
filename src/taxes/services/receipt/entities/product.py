from decimal import Decimal
from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    name: str
    unit_price: Decimal


class ProductError:
    class NegativeUnitPrice(Exception):
        def __init__(self, value):
            super().__init__(f'unit_price can\'t be negative: {value}')


def create(name: str, unit_price: Decimal):
    """ Creates a product.

    Raises error if :param unit_price: is negative.
    """
    if unit_price < 0:
        raise ProductError.NegativeUnitPrice(unit_price)

    return Product(name=name, unit_price=unit_price)
