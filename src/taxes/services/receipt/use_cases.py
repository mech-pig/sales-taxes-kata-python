from dataclasses import dataclass
from functools import reduce
from typing import Callable, Iterable

from taxes.services.basket.entities.article import Article
from taxes.services.receipt.entities.receipt import (
    add_to_receipt,
    empty as create_empty_receipt,
    Receipt,
)
from taxes.services.receipt.entities.taxed_article import TaxedArticle


@dataclass
class CreateReceiptUseCase:
    articles: Iterable[Article]

    @dataclass
    class Environment:
        info: Callable[[str], None]
        add_taxes: Callable[[Iterable[Article]], Iterable[TaxedArticle]]

    def __call__(self, env: Environment) -> Receipt:
        env.info('adding taxes to articles in basket')
        taxed_articles = env.add_taxes(self.articles)
        env.info('taxes added')

        def add_article_to_receipt(receipt, taxed_article):
            env.info(f'adding {taxed_article} to {receipt}')
            return add_to_receipt(taxed_article, receipt)

        env.info('creating receipt')
        receipt = reduce(
            add_article_to_receipt,
            taxed_articles,
            create_empty_receipt(),
        )
        env.info('receipt created')

        return receipt
