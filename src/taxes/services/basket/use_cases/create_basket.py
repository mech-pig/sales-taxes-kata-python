from dataclasses import dataclass
from functools import reduce
from typing import Callable, Iterable

from taxes.services.basket.entities.article import (
    Article, create as create_article,
)
from taxes.services.basket.entities.basket import (
    add_article as add_article_to_basket,
    Basket,
    empty as create_empty_basket,
    list_articles as list_articles_in_basket,
)
from taxes.services.basket.entities.product import Product
from taxes.services.basket.entities.purchased_item import PurchasedItem


@dataclass
class CreateBasketUseCase:
    purchased_items: Iterable[PurchasedItem]

    def __call__(self, env: 'Environment') -> Iterable[Article]:
        env.info('creating basket')

        def add_item(basket: Basket, item: PurchasedItem):
            env.info(f'creating article from {item}')
            # TODO fetch from repository
            product = Product(
                name=item.product_name,
                category='dummy',
            )
            article = create_article(
                quantity=item.quantity,
                product_name=product.name,
                product_category=product.category,
                unit_price_before_taxes=item.unit_price,
                imported=item.imported,
            )
            env.info(f'adding {article} to {basket}')
            return add_article_to_basket(article, basket)

        basket = reduce(add_item, self.purchased_items, create_empty_basket())
        return list_articles_in_basket(basket)


@dataclass
class Environment:
    info: Callable[[str], None]


def create(purchased_items: Iterable[PurchasedItem]) -> CreateBasketUseCase:
    return CreateBasketUseCase(purchased_items=purchased_items)
