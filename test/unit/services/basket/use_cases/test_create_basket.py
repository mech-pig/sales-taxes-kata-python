from dataclasses import dataclass
from decimal import Decimal
from typing import List
from unittest.mock import Mock

import pytest

from taxes.services.basket.entities import article, basket, product
from taxes.services.basket.use_cases import create_basket


@dataclass
class CreateBasketTestCase:
    articles: List[article.Article]
    expected: basket.Basket


TEST_CASES = {
    'empty article list': CreateBasketTestCase(
        articles=[],
        expected=basket.empty()
    ),
    'list with single article': CreateBasketTestCase(
        articles=[
            article.create(product_name='A', product_unit_price=Decimal('1'), quantity=1),
        ],
        expected=basket.Basket(
            articles={
                product.create(name='A', unit_price=Decimal('1')): 1,
            }
        ),
    ),
    'multiple products': CreateBasketTestCase(
        articles=[
            article.create(product_name='B', product_unit_price=Decimal('1'), quantity=2),
            article.create(product_name='A', product_unit_price=Decimal('1'), quantity=3),
            article.create(product_name='C', product_unit_price=Decimal('1'), quantity=5),
        ],
        expected=basket.Basket(
            articles={
                product.create(name='A', unit_price=Decimal('1')): 3,
                product.create(name='B', unit_price=Decimal('1')): 2,
                product.create(name='C', unit_price=Decimal('1')): 5,
            }
        ),
    ),
    'same product added multiple times': CreateBasketTestCase(
        articles=[
            article.create(product_name='B', product_unit_price=Decimal('1'), quantity=1),
            article.create(product_name='A', product_unit_price=Decimal('1'), quantity=1),
            article.create(product_name='B', product_unit_price=Decimal('1'), quantity=5),
            article.create(product_name='B', product_unit_price=Decimal('1'), quantity=3),
            article.create(product_name='A', product_unit_price=Decimal('1'), quantity=2),
        ],
        expected=basket.Basket(
            articles={
                product.create(name='A', unit_price=Decimal('1')): 3,
                product.create(name='B', unit_price=Decimal('1')): 9,
            }
        ),
    ),
    'same product name, but different unit prices': CreateBasketTestCase(
        articles=[
            article.create(product_name='A', product_unit_price=Decimal('1'), quantity=2),
            article.create(product_name='A', product_unit_price=Decimal('1.1'), quantity=3),
        ],
        expected=basket.Basket(
            articles={
                product.create(name='A', unit_price=Decimal('1')): 2,
                product.create(name='A', unit_price=Decimal('1.1')): 3,
            }
        ),
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
    run = create_basket.create(articles=case.articles)
    assert isinstance(run, create_basket.CreateBasketUseCase)


@create_basket_test_cases
def test_running_create_basket_use_cases_returns_basket(case, make_env_fixture):
    run = create_basket.create(articles=case.articles)
    env = make_env_fixture()
    assert isinstance(run(env), basket.Basket)


@create_basket_test_cases
def test_returned_basket_contains_added_articles(case, make_env_fixture):
    run = create_basket.create(articles=case.articles)
    env = make_env_fixture()
    assert case.expected == run(env)
