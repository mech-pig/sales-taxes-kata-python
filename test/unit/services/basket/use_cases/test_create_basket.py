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
    input: List[PurchasedItem]
    expected: List[article.Article]


TEST_CASES = {
    'empty article list': CreateBasketTestCase(
        input=[],
        expected=[]
    ),
    'list with single article': CreateBasketTestCase(
        input=[
            PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=1, imported=False),
        ],
        expected=[
            article.create(product_name='A', product_unit_price=Decimal('1'), quantity=1),
        ],
    ),
    'multiple products': CreateBasketTestCase(
        input=[
            PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=2, imported=False),
            PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=3, imported=False),
            PurchasedItem(product_name='C', unit_price=Decimal('1'), quantity=5, imported=False),
        ],
        expected=[
            article.create(product_name='B', product_unit_price=Decimal('1'), quantity=2),
            article.create(product_name='A', product_unit_price=Decimal('1'), quantity=3),
            article.create(product_name='C', product_unit_price=Decimal('1'), quantity=5),
        ],
    ),
    'same product added multiple times': CreateBasketTestCase(
        input=[
            PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=1, imported=False),
            PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=1, imported=False),
            PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=5, imported=False),
            PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=3, imported=False),
            PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=2, imported=False),
        ],
        expected=[
            article.create(product_name='B', product_unit_price=Decimal('1'), quantity=9),
            article.create(product_name='A', product_unit_price=Decimal('1'), quantity=3),
        ],
    ),
    'same product name, but different unit prices': CreateBasketTestCase(
        input=[
            PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=2, imported=False),
            PurchasedItem(product_name='A', unit_price=Decimal('1.1'), quantity=3, imported=False),
        ],
        expected=[
            article.create(product_name='A', product_unit_price=Decimal('1'), quantity=2),
            article.create(product_name='A', product_unit_price=Decimal('1.1'), quantity=3),
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
    run = create_basket.create(purchased_items=case.input)
    assert isinstance(run, create_basket.CreateBasketUseCase)


@create_basket_test_cases
def test_use_cases_return_list_of_articles_in_basket(case, make_env_fixture):
    run = create_basket.create(purchased_items=case.input)
    env = make_env_fixture()
    assert case.expected == run(env)
