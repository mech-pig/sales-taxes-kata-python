from dataclasses import dataclass
from decimal import Decimal
from typing import List
from unittest.mock import Mock

import pytest

from taxes.services.basket.entities import article, basket, product
from taxes.services.basket.entities.purchased_item import PurchasedItem
from taxes.services.basket.use_cases import create_basket


@dataclass
class CreateBasketTestCase:
    input: List['TestCaseInput']
    expected: List[article.Article]

    @dataclass
    class TestCaseInput:
        purchased_item: PurchasedItem
        product_category: str


TEST_CASES = {
    'empty article list': CreateBasketTestCase(
        input=[],
        expected=[]
    ),
    'list with single article': CreateBasketTestCase(
        input=[
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=1, imported=False),
                product_category='dummy',
            ),
        ],
        expected=[
            article.create(product_name='A', product_category='dummy', unit_price_before_taxes=Decimal('1'), quantity=1, imported=False),
        ],
    ),
    'multiple products': CreateBasketTestCase(
        input=[
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=2, imported=False),
                product_category='dummy',
            ),
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=3, imported=False),
                product_category='dummy',
            ),
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='C', unit_price=Decimal('1'), quantity=5, imported=False),
                product_category='dummy',
            )
        ],
        expected=[
            article.create(product_name='B', product_category='dummy', unit_price_before_taxes=Decimal('1'), quantity=2, imported=False),
            article.create(product_name='A', product_category='dummy', unit_price_before_taxes=Decimal('1'), quantity=3, imported=False),
            article.create(product_name='C', product_category='dummy', unit_price_before_taxes=Decimal('1'), quantity=5, imported=False),
        ],
    ),
    'same product added multiple times': CreateBasketTestCase(
        input=[
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=1, imported=True),
                product_category='dummy',
            ),
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=1, imported=False),
                product_category='dummy',
            ),
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=5, imported=True),
                product_category='dummy',
            ),
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=3, imported=True),
                product_category='dummy',
            ),
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=2, imported=False),
                product_category='dummy',
            ),
        ],
        expected=[
            article.create(product_name='B', product_category='dummy', unit_price_before_taxes=Decimal('1'), quantity=9, imported=True),
            article.create(product_name='A', product_category='dummy', unit_price_before_taxes=Decimal('1'), quantity=3, imported=False),
        ],
    ),
    'same product, but different unit prices': CreateBasketTestCase(
        input=[
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=2, imported=False),
                product_category='dummy',
            ),
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='A', unit_price=Decimal('1.1'), quantity=3, imported=False),
                product_category='dummy',
            ),
        ],
        expected=[
            article.create(product_name='A', product_category='dummy', unit_price_before_taxes=Decimal('1'), quantity=2, imported=False),
            article.create(product_name='A', product_category='dummy', unit_price_before_taxes=Decimal('1.1'), quantity=3, imported=False),
        ],
    ),
    'same product and unit price, from different origins': CreateBasketTestCase(
        input=[
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=2, imported=False),
                product_category='dummy',
            ),
            CreateBasketTestCase.TestCaseInput(
                purchased_item=PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=3, imported=True),
                product_category='dummy',
            ),
        ],
        expected=[
            article.create(product_name='A', product_category='dummy', unit_price_before_taxes=Decimal('1'), quantity=2, imported=False),
            article.create(product_name='A', product_category='dummy', unit_price_before_taxes=Decimal('1'), quantity=3, imported=True),
        ],
    ),
}

create_basket_test_cases = pytest.mark.parametrize(
    'case',
    [pytest.param(case, id=id) for id, case in TEST_CASES.items()],
)


@pytest.fixture
def info():
    def noop(msg: str):
        pass
    return Mock(wraps=noop)


@pytest.fixture
def make_env_fixture(info):
    def build(**overrides):
        return create_basket.Environment(**{
            'info': info,
            **overrides,
        })
    return build


@create_basket_test_cases
def test_create_returns_use_case(case):
    purchased_items = [i.purchased_item for i in case.input]
    run = create_basket.create(purchased_items=purchased_items)
    assert isinstance(run, create_basket.CreateBasketUseCase)


@create_basket_test_cases
def test_use_cases_return_list_of_articles_in_basket(case, make_env_fixture):
    purchased_items = [i.purchased_item for i in case.input]
    run = create_basket.create(purchased_items=purchased_items)
    env = make_env_fixture()
    assert case.expected == run(env)
