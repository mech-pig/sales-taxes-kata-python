from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Mapping

from taxes.services.basket.entities.article import (
    Article,
    create as create_article,
    Quantity,
)


@dataclass(frozen=True)
class Basket:
    articles: Mapping['BasketEntryKey', Article]


@dataclass(frozen=True)
class BasketEntryKey:
    product_name: str
    unit_price: Decimal
    imported: bool


def create_key(article: Article) -> BasketEntryKey:
    return BasketEntryKey(
        product_name=article.product.name,
        unit_price=article.unit_price_before_taxes,
        imported=article.imported,
    )


def empty():
    """ Create a basket without articles. """
    return Basket(articles={})


def get_quantity(key: BasketEntryKey, basket: Basket) -> Quantity:
    article = basket.articles.get(key)
    if article:
        return article.quantity
    return 0


def add_article(article: Article, basket: Basket) -> Basket:
    """ Add :param article: to :param basket:.

    If the product is already in the basket, its quantity is increased by
    :param article.quantity:. """
    key = create_key(article)
    updated_article = create_article(
        product_name=key.product_name,
        product_category=article.product.category,
        unit_price_before_taxes=key.unit_price,
        quantity=get_quantity(key, basket) + article.quantity,
        imported=key.imported
    )

    return Basket(articles={**deepcopy(basket.articles), key: updated_article})


def list_articles(basket: Basket) -> Iterable[Article]:
    """ Return the list of articles in :param basket:. """
    return [
        create_article(
            product_name=article.product.name,
            product_category=article.product.category,
            unit_price_before_taxes=article.unit_price_before_taxes,
            imported=article.imported,
            quantity=article.quantity,
        ) for article in basket.articles.values()
    ]
