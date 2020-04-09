from dataclasses import dataclass
from functools import reduce
from typing import Callable, Iterable

from taxes.services.basket.entities.article import Article
from taxes.services.receipt.entities import receipt


@dataclass
class CreateReceiptUseCase:
    articles: Iterable[Article]

    def __call__(self, env: 'Environment') -> receipt.Receipt:
        env.info('creating basket')
        articles_in_basket = env.create_basket(self.articles)
        env.info('basket created')

        env.info('adding taxes to articles in basket')
        articles_with_taxes = env.add_taxes(articles_in_basket)
        env.info('taxes added')

        def add_to_receipt(receipt_, to_add):
            env.info(f'adding {to_add} to {receipt_}')
            return receipt.add_to_receipt(to_add, receipt_)

        env.info('creating receipt')
        final_receipt = reduce(
            add_to_receipt,
            articles_with_taxes,
            receipt.empty(),
        )
        env.info('receipt created')

        return final_receipt


@dataclass
class Environment:
    info: Callable[[str], None]
    create_basket: Callable[[Iterable[Article]], Iterable[Article]]
    add_taxes: Callable[[Iterable[Article]], Iterable[receipt.ItemToInsert]]


def create(articles: Iterable[Article]) -> CreateReceiptUseCase:
    return CreateReceiptUseCase(articles=articles)
