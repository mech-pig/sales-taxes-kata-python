from copy import deepcopy
from dataclasses import dataclass
from typing import Mapping

from taxes.services.receipt.entities.article import Article, Quantity
from taxes.services.receipt.entities.product import Product


@dataclass(frozen=True)
class Basket:
    articles: Mapping[Product, Quantity]


def empty():
    """ Create a basket without articles. """
    return Basket(articles={})


def get_quantity(product: Product, basket: Basket) -> Quantity:
    """ Return the number of :param product: in :param basket:.

    Returns 0 if :param product: is not found in :param basket:.
    """
    return basket.articles.get(product, 0)


def add_article(article: Article, basket: Basket) -> Basket:
    """ Add :param article: to :param basket:.

    If the product is already in the basket, its quantity is increased by
    :param article.quantity:. """
    product_to_add = deepcopy(article.product)
    quantity = get_quantity(product_to_add, basket) + article.quantity

    return Basket(articles={
        **deepcopy(basket.articles),
        product_to_add: quantity,
    })
