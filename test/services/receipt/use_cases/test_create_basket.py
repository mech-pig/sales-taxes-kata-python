from decimal import Decimal
from unittest.mock import Mock

import pytest

from taxes.services.receipt.entities import article, basket, product
from taxes.services.receipt.use_cases import create_basket


basket_test_cases = pytest.mark.parametrize(
    'case',
    [
        pytest.param(
            {
                'articles': [],
                'expected': basket.empty(),
            },
            id='empty article list',
        ),
        pytest.param(
            {
                'articles': [
                    article.create(product_name='A', product_unit_price=Decimal('1'), quantity=1),
                ],
                'expected': basket.Basket(
                    articles={
                        product.create(name='A', unit_price=Decimal('1')): 1,
                    }
                ),
            },
            id='list with single article',
        ),
        pytest.param(
            {
                'articles': [
                    article.create(product_name='B', product_unit_price=Decimal('1'), quantity=2),
                    article.create(product_name='A', product_unit_price=Decimal('1'), quantity=3),
                    article.create(product_name='C', product_unit_price=Decimal('1'), quantity=5),
                ],
                'expected': basket.Basket(
                    articles={
                        product.create(name='A', unit_price=Decimal('1')): 3,
                        product.create(name='B', unit_price=Decimal('1')): 2,
                        product.create(name='C', unit_price=Decimal('1')): 5,
                    }
                ),
            },
            id='multiple products',
        ),
        pytest.param(
            {
                'articles': [
                    article.create(product_name='B', product_unit_price=Decimal('1'), quantity=1),
                    article.create(product_name='A', product_unit_price=Decimal('1'), quantity=1),
                    article.create(product_name='B', product_unit_price=Decimal('1'), quantity=5),
                    article.create(product_name='B', product_unit_price=Decimal('1'), quantity=3),
                    article.create(product_name='A', product_unit_price=Decimal('1'), quantity=2),
                ],
                'expected': basket.Basket(
                    articles={
                        product.create(name='A', unit_price=Decimal('1')): 3,
                        product.create(name='B', unit_price=Decimal('1')): 9,
                    }
                ),
            },
            id='same product added multiple times',
        ),
        pytest.param(
            {
                'articles': [
                    article.create(product_name='A', product_unit_price=Decimal('1'), quantity=2),
                    article.create(product_name='A', product_unit_price=Decimal('1.1'), quantity=3),
                ],
                'expected': basket.Basket(
                    articles={
                        product.create(name='A', unit_price=Decimal('1')): 2,
                        product.create(name='A', unit_price=Decimal('1.1')): 3,
                    }
                ),
            },
            id='same product name, but different unit prices',
        ),
    ],
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


@basket_test_cases
def test_create_returns_use_case(case):
    articles = case['articles']
    run = create_basket.create(articles=articles)
    assert isinstance(run, create_basket.CreateBasketUseCase)


@basket_test_cases
def test_running_create_basket_use_cases_returns_basket(case, make_env_fixture):
    articles = case['articles']
    run = create_basket.create(articles=articles)
    env = make_env_fixture()
    assert isinstance(run(env), basket.Basket)


@basket_test_cases
def test_returned_basket_contains_added_articles(case, make_env_fixture):
    articles = case['articles']
    expected = case['expected']
    run = create_basket.create(articles=articles)
    env = make_env_fixture()
    assert expected == run(env)
