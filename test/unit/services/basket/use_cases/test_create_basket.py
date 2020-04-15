from dataclasses import dataclass
from decimal import Decimal
from typing import List
from unittest.mock import Mock

import pytest

from taxes.services.basket.entities import article
from taxes.services.basket.entities.product import Product
from taxes.services.basket.entities.purchased_item import PurchasedItem
from taxes.services.basket.use_cases import CreateBasketUseCase


@dataclass
class CreateBasketTestCase:
    input: 'TestCaseInput'
    expected: List[article.Article]

    @dataclass
    class TestCaseInput:
        purchased_items: List[PurchasedItem]
        products: List[Product]


TEST_CASES = {
    'empty article list': CreateBasketTestCase(
        input=CreateBasketTestCase.TestCaseInput(
            purchased_items=[],
            products=[],
        ),
        expected=[]
    ),
    'list with single article': CreateBasketTestCase(
        input=CreateBasketTestCase.TestCaseInput(
            purchased_items=[
                PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=1, imported=False),
            ],
            products=[Product(name='A', category='dummy')],
        ),
        expected=[
            article.create(product_name='A', product_category='dummy', unit_price_before_taxes=Decimal('1'), quantity=1, imported=False),
        ],
    ),
    'multiple products': CreateBasketTestCase(
        input=CreateBasketTestCase.TestCaseInput(
            purchased_items=[
                PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=2, imported=False),
                PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=3, imported=False),
                PurchasedItem(product_name='C', unit_price=Decimal('1'), quantity=5, imported=False),
            ],
            products=[
                Product(name='A', category='cat-a'),
                Product(name='B', category='cat-b'),
                Product(name='C', category='cat-c')
            ],
        ),
        expected=[
            article.create(product_name='B', product_category='cat-b', unit_price_before_taxes=Decimal('1'), quantity=2, imported=False),
            article.create(product_name='A', product_category='cat-a', unit_price_before_taxes=Decimal('1'), quantity=3, imported=False),
            article.create(product_name='C', product_category='cat-c', unit_price_before_taxes=Decimal('1'), quantity=5, imported=False),
        ],
    ),
    'same product added multiple times': CreateBasketTestCase(
        input=CreateBasketTestCase.TestCaseInput(
            purchased_items=[
                PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=1, imported=True),
                PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=1, imported=False),
                PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=5, imported=True),
                PurchasedItem(product_name='B', unit_price=Decimal('1'), quantity=3, imported=True),
                PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=2, imported=False),
            ],
            products=[
                Product(name='A', category='cat-a'),
                Product(name='B', category='cat-b'),
            ],
        ),
        expected=[
            article.create(product_name='B', product_category='cat-b', unit_price_before_taxes=Decimal('1'), quantity=9, imported=True),
            article.create(product_name='A', product_category='cat-a', unit_price_before_taxes=Decimal('1'), quantity=3, imported=False),
        ],
    ),
    'same product, but different unit prices': CreateBasketTestCase(
        input=CreateBasketTestCase.TestCaseInput(
            purchased_items=[
                PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=2, imported=False),
                PurchasedItem(product_name='A', unit_price=Decimal('1.1'), quantity=3, imported=False),
            ],
            products=[
                Product(name='A', category='cat-a'),
            ],
        ),
        expected=[
            article.create(product_name='A', product_category='cat-a', unit_price_before_taxes=Decimal('1'), quantity=2, imported=False),
            article.create(product_name='A', product_category='cat-a', unit_price_before_taxes=Decimal('1.1'), quantity=3, imported=False),
        ],
    ),
    'same product and unit price, from different origins': CreateBasketTestCase(
        input=CreateBasketTestCase.TestCaseInput(
            purchased_items=[
                PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=2, imported=False),
                PurchasedItem(product_name='A', unit_price=Decimal('1'), quantity=3, imported=True),
            ],
            products=[
                Product(name='A', category='cat-a'),
            ],
        ),
        expected=[
            article.create(product_name='A', product_category='cat-a', unit_price_before_taxes=Decimal('1'), quantity=2, imported=False),
            article.create(product_name='A', product_category='cat-a', unit_price_before_taxes=Decimal('1'), quantity=3, imported=True),
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
def make_get_product_fixture():
    def build(input: CreateBasketTestCase.TestCaseInput):
        db = {product.name: product for product in input.products}
        def get_product(name: str):
            return db.get(name)
        return Mock(side_effect=get_product)
    return build


@pytest.fixture
def make_env_fixture(info, make_get_product_fixture):
    def build(input: CreateBasketTestCase.TestCaseInput, **overrides):
        return CreateBasketUseCase.Environment(**{
            'info': info,
            'get_product_by_name': make_get_product_fixture(input),
            **overrides,
        })
    return build


@create_basket_test_cases
def test_use_cases_return_list_of_articles_in_basket(case, make_env_fixture):
    run = CreateBasketUseCase(purchased_items=case.input.purchased_items)
    env = make_env_fixture(case.input)
    assert case.expected == run(env)
