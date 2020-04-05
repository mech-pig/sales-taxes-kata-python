from copy import deepcopy
from decimal import Decimal
from dataclasses import dataclass
from typing import Mapping, NewType

from taxes.services.receipt.entities import article


Quantity = NewType('Quantity', int)


@dataclass
class Basket:
    articles: Mapping['Product', Quantity]


@dataclass(frozen=True)
class Product:
    name: str
    unit_price: Decimal


def empty():
    """ Create a basket without articles. """
    return Basket(articles={})


def get_quantity(product: Product, basket: Basket) -> Quantity:
    """ Return the number of :param product: in :param basket:.

    Returns 0 if :param product: is not found in :param basket:.
    """
    return basket.articles.get(product, 0)


def add_article(article: article.Article, basket: Basket) -> Basket:
    """ Add :param article: to :param basket:.

    If the product is already in the basket, its quantity is increased by
    :param article.quantity:. """
    product = Product(name=article.product_name, unit_price=article.unit_price)
    updated_quantity = get_quantity(product, basket) + article.quantity

    return Basket(articles={
        **deepcopy(basket.articles),
        product: updated_quantity,
    })
