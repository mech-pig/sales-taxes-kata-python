from dataclasses import dataclass
from decimal import Decimal
from typing import List
from unittest.mock import Mock

import pytest

from taxes.services.basket.entities import article
from taxes.services.receipt.entities import receipt


@dataclass
class AddTaxesTestCase:
    articles: List[article.Article]
    expected: List[receipt.ItemToInsert]


TEST_CASES = {
    'no articles': AddTaxesTestCase(
        articles=[],
        expected=[],
    ),
    'single, non-imported article': AddTaxesTestCase(
        articles=[
            article.create(quantity=2, product_name='test', product_unit_price=Decimal('1'), imported=False),
        ],
        expected=[
            receipt.ItemToInsert(
                description='test',
                quantity=2,
                unit_price_before_taxes=Decimal('1'),
                taxes_to_apply=[],
            )
        ],
    ),
    'single, imported article': AddTaxesTestCase(
        articles=[
            article.create(quantity=2, product_name='test', product_unit_price=Decimal('1'), imported=True),
        ],
        expected=[
            receipt.ItemToInsert(
                description='imported test',
                quantity=2,
                unit_price_before_taxes=Decimal('1'),
                taxes_to_apply=[],
            )
        ],
    ),
    'multiple articles': AddTaxesTestCase(
        articles=[
            article.create(quantity=2, product_name='test', product_unit_price=Decimal('1'), imported=False),
            article.create(quantity=3, product_name='test-2', product_unit_price=Decimal('2.34'), imported=True),
        ],
        expected=[
            receipt.ItemToInsert(
                description='test',
                quantity=2,
                unit_price_before_taxes=Decimal('1'),
                taxes_to_apply=[],
            ),
            receipt.ItemToInsert(
                description='imported test-2',
                quantity=3,
                unit_price_before_taxes=Decimal('2.34'),
                taxes_to_apply=[],
            )
        ],
    )
}


add_taxes_test_cases = pytest.mark.parametrize(
    'case',
    [pytest.param(case, id=id) for id, case in TEST_CASES.items()],
)
