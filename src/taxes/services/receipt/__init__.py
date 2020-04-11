from dataclasses import dataclass
from typing import Iterable, Protocol

from taxes.services.basket.entities.article import Article
from taxes.services.receipt.entities.receipt import ItemToInsert
from taxes.services.receipt.use_cases import create_receipt as create_receipt_use_case


@dataclass
class ReceiptService:
    logger: 'Dependency.Logger'
    basket_service: 'Dependency.BasketService'
    tax_service: 'Dependency.TaxService'

    def create_receipt(self, articles: Iterable[Article]):
        run = create_receipt_use_case.create(articles=articles)
        env = create_receipt_use_case.Environment(
            info=self.logger.info,
            create_basket=self.basket_service.create_basket,
            add_taxes=self.tax_service.add_taxes,
        )
        return run(env)

class Dependency:
    class Logger(Protocol):
        def info(self, msg: str):
            ...

        def debug(self, msg: str):
            ...

    class TaxService(Protocol):
        def add_taxes(self, articles: Iterable[Article]) -> Iterable[ItemToInsert]:
            ...

    class BasketService(Protocol):
        def create_basket(self, articles: Iterable[Article]) -> Iterable[Article]:
            ...


def create(logger: Dependency.Logger, basket_service: Dependency.BasketService, tax_service: Dependency.TaxService):
    logger.debug(
        f'instantiating receipt service with logger={logger}, ',
        f'basket_service={basket_service} and tax_service={tax_service}'
    )
    return ReceiptService(logger=logger, basket_service=basket_service, tax_service=tax_service)
