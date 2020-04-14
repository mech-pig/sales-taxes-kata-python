from dataclasses import dataclass
from typing import Callable, Iterable

from taxes.services.basket.entities.article import Article
from taxes.services.receipt.entities.receipt import ItemToInsert


@dataclass
class TaxArticlesUseCase:
    articles: Iterable[Article]

    def __call__(self, env: 'Environment') -> Iterable[ItemToInsert]:
        env.info('adding taxes to articles in basket')

        def describe(article):
            imported = 'imported ' if article.imported else ''
            return f'{imported}{article.product.name}'

        taxed_items = [
            ItemToInsert(
                description=describe(article),
                quantity=article.quantity,
                unit_price_before_taxes=article.unit_price_before_taxes,
                taxes_to_apply=[],
            ) for article in self.articles
        ]
        env.info('taxes added')
        return taxed_items


@dataclass
class Environment:
    info: Callable[[str], None]


def create(articles: Iterable[Article]) -> TaxArticlesUseCase:
    return TaxArticlesUseCase(articles=articles)
