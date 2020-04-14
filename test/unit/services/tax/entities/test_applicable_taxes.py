from dataclasses import dataclass
from decimal import Decimal
from typing import List

import pytest

from taxes.services.basket.entities import article, product
from taxes.services.tax.entities import applicable_taxes, tax


@dataclass
class GetApplicableTaxesTestCase:
    input: article.Article
    expected: List[tax.Tax]


GET_APPLICABLE_TAXES_TEST_CASES = {
    'non imported article of non-exempt category': GetApplicableTaxesTestCase(
        input=article.Article(
            product=product.Product(name='item', category='dummy'),
            imported=False,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
        ),
        expected={applicable_taxes.TAX_PRODUCT_CATEGORY},
    ),
    'uncategorized non imported article': GetApplicableTaxesTestCase(
        input=article.Article(
            product=product.Product(name='item', category=None),
            imported=False,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
        ),
        expected={applicable_taxes.TAX_PRODUCT_CATEGORY},
    ),
    'non imported food article': GetApplicableTaxesTestCase(
        input=article.Article(
            product=product.Product(name='item', category='food'),
            imported=False,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
        ),
        expected=set(),
    ),
    'non imported medical article': GetApplicableTaxesTestCase(
        input=article.Article(
            product=product.Product(name='item', category='medical'),
            imported=False,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
        ),
        expected=set(),
    ),
    'non imported book article': GetApplicableTaxesTestCase(
        input=article.Article(
            product=product.Product(name='item', category='book'),
            imported=False,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
        ),
        expected=set(),
    ),
    'imported article of non-exempt category': GetApplicableTaxesTestCase(
        input=article.Article(
            product=product.Product(name='item', category='dummy'),
            imported=True,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
        ),
        expected={applicable_taxes.TAX_PRODUCT_CATEGORY, applicable_taxes.TAX_IMPORT},
    ),
    'uncategorized imported article': GetApplicableTaxesTestCase(
        input=article.Article(
            product=product.Product(name='item', category=None),
            imported=True,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
        ),
        expected={applicable_taxes.TAX_PRODUCT_CATEGORY, applicable_taxes.TAX_IMPORT},
    ),
    'imported food article': GetApplicableTaxesTestCase(
        input=article.Article(
            product=product.Product(name='item', category='food'),
            imported=True,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
        ),
        expected={applicable_taxes.TAX_IMPORT},
    ),
    'imported medical article': GetApplicableTaxesTestCase(
        input=article.Article(
            product=product.Product(name='item', category='medical'),
            imported=True,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
        ),
        expected={applicable_taxes.TAX_IMPORT},
    ),
    'imported book article': GetApplicableTaxesTestCase(
        input=article.Article(
            product=product.Product(name='item', category='book'),
            imported=True,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
        ),
        expected={applicable_taxes.TAX_IMPORT},
    ),
}

@pytest.mark.parametrize('case', [
    pytest.param(case, id=id)
    for id, case in GET_APPLICABLE_TAXES_TEST_CASES.items()
])
def test_get_applicable_taxes(case):
    assert case.expected == applicable_taxes.get_applicable_taxes(case.input)
