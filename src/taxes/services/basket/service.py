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

    def create_basket(
        self,
        purchased_items: Iterable[PurchasedItem],
    ) -> Iterable[Article]:
        run = create_basket_use_case.create(purchased_items=purchased_items)
        env = create_basket_use_case.Environment(info=self.logger.info)
        return run(env)


class Dependency:
    class Logger(Protocol):
        def info(self, msg: str):  # pragma: no cover
            ...

        def debug(self, msg: str):  # pragma: no cover
            ...


def create(logger: Dependency.Logger):
    logger.debug(f'instantiating basket service with logger={logger}')
    return BasketService(logger=logger)
