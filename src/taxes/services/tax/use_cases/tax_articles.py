from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, Iterable

from taxes.services.basket.entities import article
from taxes.services.receipt.entities import taxed_article


@dataclass
class TaxArticlesUseCase:
    articles: Iterable[article.Article]

    def __call__(self, env: 'Environment') -> Iterable[taxed_article.TaxedArticle]:  # noqa: E501
        env.info('adding taxes to articles in basket')
        taxed_items = [
            taxed_article.TaxedArticle(
                product=article.product,
                quantity=article.quantity,
                imported=article.imported,
                unit_price_before_taxes=article.unit_price_before_taxes,
                tax_amount_due_per_unit=Decimal('0.00'),
            ) for article in self.articles
        ]
        env.info('taxes added')

        return taxed_items


@dataclass
class Environment:
    info: Callable[[str], None]


def create(articles: Iterable[article.Article]) -> TaxArticlesUseCase:
    return TaxArticlesUseCase(articles=articles)
