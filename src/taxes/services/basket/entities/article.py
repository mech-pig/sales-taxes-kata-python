from dataclasses import dataclass
from decimal import Decimal
from typing import NewType


from taxes.services.basket.entities import product


Quantity = NewType('Quantity', int)


@dataclass(frozen=True)
class Article:
    quantity: Quantity
    product: product.Product


class ArticleError:
    class NonPositiveQuantity(Exception):
        def __init__(self, value):
            super().__init__(f'quantity must be positive: {value}')


def create(quantity: int, product_name: str, product_unit_price: Decimal):
    """ Creates an article.

    Article quantity must be greater than zero, unit_price can't be less than
    zero.
    """
    if quantity <= 0:
        raise ArticleError.NonPositiveQuantity(quantity)

    return Article(
        product=product.create(
            name=product_name,
            unit_price=product_unit_price,
        ),
        quantity=quantity,
    )
