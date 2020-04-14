from dataclasses import dataclass
from typing import Callable, Iterable

from taxes.services.basket.entities.article import Article
from taxes.services.receipt.entities.taxed_article import TaxedArticle
from taxes.services.tax.entities.applicable_taxes import get_applicable_taxes
from taxes.services.tax.entities.tax import apply as apply_taxes


@dataclass
class TaxArticlesUseCase:
    articles: Iterable[Article]

    def __call__(self, env: 'Environment') -> Iterable[TaxedArticle]:
        env.info('adding taxes to articles in basket')

        def tax_article(article):
            env.info(f'get applicable taxes for {article}')
            taxes_to_apply = get_applicable_taxes(article)

            env.info(f'taxes to apply: {taxes_to_apply}')
            tax_amount_due_per_unit = apply_taxes(
                price=article.unit_price_before_taxes,
                taxes=taxes_to_apply
            )
            env.info(f'tax amount due per unit: {tax_amount_due_per_unit}')

            taxed_article = TaxedArticle(
                product=article.product,
                quantity=article.quantity,
                imported=article.imported,
                unit_price_before_taxes=article.unit_price_before_taxes,
                tax_amount_due_per_unit=tax_amount_due_per_unit,
            )
            env.info(f'taxes have been applied: {taxed_article}')
            return taxed_article

        taxed_articles = [tax_article(article) for article in self.articles]
        env.info('taxes added')

        return taxed_articles


@dataclass
class Environment:
    info: Callable[[str], None]


def create(articles: Iterable[Article]) -> TaxArticlesUseCase:
    return TaxArticlesUseCase(articles=articles)
