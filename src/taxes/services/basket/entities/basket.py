from copy import deepcopy
from dataclasses import dataclass
from typing import Iterable, Mapping

from taxes.services.basket.entities.article import (
    Article,
    create as create_article,
    Quantity,
)
from taxes.services.basket.entities.product import Product


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


def list_articles(basket: Basket) -> Iterable[Article]:
    """ Return the list of articles in :param basket:. """
    return [
        create_article(
            quantity=quantity,
            product_name=product.name,
            product_unit_price=product.unit_price,
        ) for product, quantity in basket.articles.items()
    ]
