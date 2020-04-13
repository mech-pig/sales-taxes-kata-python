from dataclasses import dataclass
from functools import reduce
from typing import Callable, Iterable

from taxes.services.basket.entities.article import Article
from taxes.services.basket.entities.basket import (
    add_article as add_article_to_basket,
    empty as create_empty_basket,
    list_articles as list_articles_in_basket,
)


@dataclass
class CreateBasketUseCase:
    articles: Iterable[Article]

    def __call__(self, env: 'Environment') -> Iterable[Article]:
        env.info('creating basket')

        def add_article(basket_, to_add):
            env.info(f'adding {to_add} to {basket_}')
            return add_article_to_basket(to_add, basket_)

        basket = reduce(add_article, self.articles, create_empty_basket())
        return list_articles_in_basket(basket)


@dataclass
class Environment:
    info: Callable[[str], None]


def create(articles: Iterable[Article]) -> CreateBasketUseCase:
    return CreateBasketUseCase(articles=articles)
