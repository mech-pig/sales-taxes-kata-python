from dataclasses import dataclass
from decimal import Decimal
from typing import List
from unittest.mock import Mock

import pytest

from taxes.services.basket.entities import article, product
from taxes.services.receipt.entities import taxed_article


@dataclass
class AddTaxesTestCase:
    input: List[article.Article]
    expected: List[taxed_article.TaxedArticle]


TEST_CASES = {
    'no articles': AddTaxesTestCase(
        input=[],
        expected=[],
    ),
    'non imported, exempt category article': AddTaxesTestCase(
        input=[
            article.Article(
                product=product.Product(name='test', category='food'),
                quantity=2,
                unit_price_before_taxes=Decimal('1'),
                imported=False,
            ),
        ],
        expected=[
            taxed_article.TaxedArticle(
                product=product.Product(name='test', category='food'),
                quantity=2,
                imported=False,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0'),
            )
        ],
    ),
    'imported, exempt category article': AddTaxesTestCase(
        input=[
            article.Article(
                product=product.Product(name='test', category='book'),
                quantity=2,
                unit_price_before_taxes=Decimal('1'),
                imported=True,
            ),
        ],
        expected=[
            taxed_article.TaxedArticle(
                product=product.Product(name='test', category='book'),
                quantity=2,
                imported=True,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0.05'),
            )
        ],
    ),
    'non imported, exempt category article': AddTaxesTestCase(
        input=[
            article.Article(
                product=product.Product(name='test', category='food'),
                quantity=2,
                unit_price_before_taxes=Decimal('1'),
                imported=False,
            ),
        ],
        expected=[
            taxed_article.TaxedArticle(
                product=product.Product(name='test', category='food'),
                quantity=2,
                imported=False,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0.00'),
            )
        ],
    ),
    'imported, non-exempt category article': AddTaxesTestCase(
        input=[
            article.Article(
                product=product.Product(name='test', category='dummy'),
                quantity=2,
                unit_price_before_taxes=Decimal('2'),
                imported=True,
            ),
        ],
        expected=[
            taxed_article.TaxedArticle(
                product=product.Product(name='test', category='dummy'),
                quantity=2,
                imported=True,
                unit_price_before_taxes=Decimal('2'),
                tax_amount_due_per_unit=Decimal('0.3'),
            )
        ],
    ),
    'multiple articles, mixed': AddTaxesTestCase(
        input=[
            article.Article(
                product=product.Product(name='exempt', category='medical'),
                quantity=2,
                unit_price_before_taxes=Decimal('1'),
                imported=True,
            ),
            article.Article(
                product=product.Product(name='non-exempt', category='dummy-2'),
                quantity=1,
                unit_price_before_taxes=Decimal('2'),
                imported=False,
            ),
            article.Article(
                product=product.Product(name='non-exempt', category='dummy-2'),
                quantity=1,
                unit_price_before_taxes=Decimal('2'),
                imported=True,
            ),
        ],
        expected=[
            taxed_article.TaxedArticle(
                product=product.Product(name='exempt', category='medical'),
                quantity=2,
                imported=True,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0.05'),
            ),
            taxed_article.TaxedArticle(
                product=product.Product(name='non-exempt', category='dummy-2'),
                quantity=1,
                imported=False,
                unit_price_before_taxes=Decimal('2'),
                tax_amount_due_per_unit=Decimal('0.2'),
            ),
            taxed_article.TaxedArticle(
                product=product.Product(name='non-exempt', category='dummy-2'),
                quantity=1,
                imported=True,
                unit_price_before_taxes=Decimal('2'),
                tax_amount_due_per_unit=Decimal('0.3'),
            )
        ],
    ),
}


add_taxes_test_cases = pytest.mark.parametrize(
    'case',
    [pytest.param(case, id=id) for id, case in TEST_CASES.items()],
)
