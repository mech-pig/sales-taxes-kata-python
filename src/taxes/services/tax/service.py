from dataclasses import dataclass
from typing import Iterable, Protocol

from taxes.services.basket.entities.article import Article
from taxes.services.receipt.entities.receipt import ItemToInsert
from taxes.services.tax.use_cases import tax_articles as tax_articles_use_case


@dataclass
class TaxService:
    logger: 'Dependency.Logger'

    def add_taxes(self, articles: Iterable[Article]) -> Iterable[ItemToInsert]:
        tax_articles = tax_articles_use_case.create(articles=articles)
        env = tax_articles_use_case.Environment(
            info=self.logger.info,
        )
        return tax_articles(env)


class Dependency:
    class Logger(Protocol):
        def info(self, msg: str):  # pragma: no cover
            ...

        def debug(self, msg: str):  # pragma: no cover
            ...


def create(logger: Dependency.Logger):
    logger.debug(f'instantiating tax service with logger={logger}')
    return TaxService(logger=logger)
