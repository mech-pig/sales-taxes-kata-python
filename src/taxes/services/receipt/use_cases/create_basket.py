from dataclasses import dataclass
from functools import reduce
from typing import Callable, Iterable

from taxes.services.receipt.entities import article, basket


@dataclass
class CreateBasketUseCase:
    articles: Iterable[article.Article]

    def __call__(self, env: 'Environment'):
        env.info('creating basket')

        def add_article(basket_, to_add):
            env.info(f'adding {to_add} to {basket_}')
            return basket.add_article(to_add, basket_)

        return reduce(add_article, self.articles, basket.empty())


@dataclass
class Environment:
    info: Callable[[str], None]


def create(articles: Iterable[article.Article]) -> CreateBasketUseCase:
    return CreateBasketUseCase(articles=articles)
