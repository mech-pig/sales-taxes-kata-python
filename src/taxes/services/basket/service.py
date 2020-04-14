from dataclasses import dataclass
from typing import Iterable, Protocol

from taxes.services.basket.entities.article import Article
from taxes.services.basket.entities.purchased_item import PurchasedItem
from taxes.services.basket.use_cases import (
    create_basket as create_basket_use_case,
)


@dataclass
class BasketService:
    logger: 'Dependency.Logger'
    product_repository: 'Dependency.ProductRepository'

    def create_basket(
        self,
        purchased_items: Iterable[PurchasedItem],
    ) -> Iterable[Article]:
        run = create_basket_use_case.create(purchased_items=purchased_items)
        env = create_basket_use_case.Environment(
            info=self.logger.info,
            get_product_by_name=self.product_repository.get_by_name,
        )
        return run(env)


class Dependency:
    class Logger(Protocol):
        def info(self, msg: str):  # pragma: no cover
            ...

        def debug(self, msg: str):  # pragma: no cover
            ...

    class ProductRepository(Protocol):
        def get_by_name(name: str):  # pragma: no cover
            ...


def create(
    logger: Dependency.Logger,
    product_repository=Dependency.ProductRepository,
):
    logger.debug(
        f'instantiating basket service ',
        f'with logger={logger} and product_repository={product_repository}',
    )
    return BasketService(logger=logger, product_repository=product_repository)
