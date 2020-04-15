from dataclasses import dataclass
from decimal import Decimal

from taxes.services.basket.entities.product import (
    Product,
    create as create_product,
)


@dataclass(frozen=True)
class Article:
    product: Product
    imported: bool
    quantity: int
    unit_price_before_taxes: Decimal


class ArticleError:
    class NonPositiveQuantity(Exception):
        def __init__(self, value):
            super().__init__(f'quantity must be positive: {value}')

    class NegativeUnitPrice(Exception):
        def __init__(self, value):
            super().__init__(
                f'unit_price_before_taxes can\'t be negative: {value}'
            )


def create(
    quantity: int,
    imported: bool,
    product_name: str,
    product_category: str,
    unit_price_before_taxes: Decimal,
):
    """ Creates an article.

    :param quantity: must be greater than zero, an error is raised otherwise.
    :param unit_price_before_taxes: can't be less than zero, an error is raised
    otherwise.
    """
    if quantity <= 0:
        raise ArticleError.NonPositiveQuantity(quantity)

    if unit_price_before_taxes < 0:
        raise ArticleError.NegativeUnitPrice(unit_price_before_taxes)

    return Article(
        product=create_product(
            name=product_name,
            category=product_category,
        ),
        unit_price_before_taxes=unit_price_before_taxes,
        imported=imported,
        quantity=quantity,
    )
