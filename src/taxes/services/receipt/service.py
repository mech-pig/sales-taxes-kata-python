from dataclasses import dataclass
from typing import Iterable, Protocol

from taxes.services.basket.entities.article import Article
from taxes.services.receipt.entities.taxed_article import TaxedArticle
from taxes.services.receipt.use_cases import CreateReceiptUseCase


@dataclass
class ReceiptService:
    logger: 'Dependency.Logger'
    tax_service: 'Dependency.TaxService'

    def create_receipt(self, articles: Iterable[Article]):
        run = CreateReceiptUseCase(articles=articles)
        env = CreateReceiptUseCase.Environment(
            info=self.logger.info,
            add_taxes=self.tax_service.add_taxes,
        )
        return run(env)


class Dependency:
    class Logger(Protocol):
        def info(self, msg: str):  # pragma: no cover
            ...

        def debug(self, msg: str):  # pragma: no cover
            ...

    class TaxService(Protocol):
        def add_taxes(
            self,
            articles: Iterable[Article]
        ) -> Iterable[TaxedArticle]:  # pragma: no cover
            ...


def create(logger: Dependency.Logger, tax_service: Dependency.TaxService):
    logger.debug(
        f'instantiating receipt service ',
        f'with logger={logger} and tax_service={tax_service}'
    )
    return ReceiptService(logger=logger, tax_service=tax_service)
