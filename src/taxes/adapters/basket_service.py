from dataclasses import dataclass
from typing import Iterable

from taxes.services.basket import BasketService
from taxes.services.basket.entities import article
from taxes.services.receipt import Dependency as ReceiptServiceDependency


@dataclass
class BasketServiceAdapter(ReceiptServiceDependency.BasketService):
    basket_service: BasketService

    def create_basket(
        self,
        articles: Iterable[article.Article],
    ) -> Iterable[article.Article]:
        basket = self.basket_service.create_basket(articles=articles)
        return [
            article.create(
                product_name=product.name,
                product_unit_price=product.unit_price,
                quantity=quantity,
            ) for product, quantity in basket.articles.items()
        ]
