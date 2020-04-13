from dataclasses import dataclass
from typing import Iterable, Protocol

from taxes.services.basket.entities.article import Article
from taxes.services.basket.use_cases import (
    create_basket as create_basket_use_case,
)


@dataclass
class BasketService:
    logger: 'Dependency.Logger'

    def create_basket(self, articles: Iterable[Article]):
        run = create_basket_use_case.create(articles=articles)
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
