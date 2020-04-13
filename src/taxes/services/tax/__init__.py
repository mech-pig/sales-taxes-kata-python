from dataclasses import dataclass
from typing import Iterable, Protocol

from taxes.services.basket.entities.article import Article
from taxes.services.receipt.entities.receipt import ItemToInsert


@dataclass
class TaxService:
    logger: 'Dependency.Logger'

    def add_taxes(self, articles: Iterable[Article]) -> Iterable[ItemToInsert]:
        self.logger.info('wip: no taxes will be added')

        def describe(article):
            imported = 'imported ' if article.imported else ''
            return f'{imported}{article.product.name}'

        return [
            ItemToInsert(
                description=describe(article),
                quantity=article.quantity,
                unit_price_before_taxes=article.product.unit_price,
                taxes_to_apply=[],
            ) for article in articles
        ]


class Dependency:
    class Logger(Protocol):
        def info(self, msg: str):  # pragma: no cover
            ...

        def debug(self, msg: str):  # pragma: no cover
            ...


def create(logger: Dependency.Logger):
    logger.debug(f'instantiating tax service with logger={logger}')
    return TaxService(logger=logger)
