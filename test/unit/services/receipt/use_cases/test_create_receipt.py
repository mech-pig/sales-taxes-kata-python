from dataclasses import dataclass
from decimal import Decimal
from typing import List
from unittest.mock import call, Mock, sentinel

import pytest

from taxes.services.basket.entities import article
from taxes.services.receipt.entities import receipt, tax
from taxes.services.receipt.use_cases import create_receipt


@dataclass
class CreateReceiptTestCase:
    params: List['TestCaseParams']
    expected: receipt.Receipt

    @dataclass
    class TestCaseParams:
        article_in_basket: article.Article
        taxes_to_apply: List[tax.Tax]


TEST_CASES = {
    'no articles in basket': CreateReceiptTestCase(
        params=[],
        expected=receipt.empty()
    ),
    'single article in basket, with no taxes': CreateReceiptTestCase(
        params=[
            CreateReceiptTestCase.TestCaseParams(
                article_in_basket=article.create(
                    quantity=1,
                    product_name='test-product',
                    product_unit_price=Decimal('1'),
                ),
                taxes_to_apply=[],
            ),
        ],
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='test-product',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1'),
                ),
            ],
            taxes_due=Decimal('0'),
            total_due=Decimal('1'),
        )
    ),
    'single article in basket (quantity > 1), with no taxes': CreateReceiptTestCase(
        params=[
            CreateReceiptTestCase.TestCaseParams(
                article_in_basket=article.create(
                    quantity=3,
                    product_name='test-product',
                    product_unit_price=Decimal('1'),
                ),
                taxes_to_apply=[],
            ),
        ],
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='test-product',
                    quantity=3,
                    subtotal_price_with_taxes=Decimal('3'),
                ),
            ],
            taxes_due=Decimal('0'),
            total_due=Decimal('3'),
        )
    ),
    'single article in basket, with single tax': CreateReceiptTestCase(
        params=[
            CreateReceiptTestCase.TestCaseParams(
                article_in_basket=article.create(
                    quantity=1,
                    product_name='test-product',
                    product_unit_price=Decimal('2'),
                ),
                taxes_to_apply=[tax.Tax(id='test-tax', rate=Decimal('0.1'))],
            ),
        ],
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='test-product',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('2.2'),
                ),
            ],
            taxes_due=Decimal('0.2'),
            total_due=Decimal('2.2'),
        )
    ),
    'multiple articles in basket, single tax each': CreateReceiptTestCase(
        params=[
            CreateReceiptTestCase.TestCaseParams(
                article_in_basket=article.create(
                    quantity=1,
                    product_name='test-product',
                    product_unit_price=Decimal('2'),
                ),
                taxes_to_apply=[tax.Tax(id='test-tax', rate=Decimal('0.1'))],
            ),
            CreateReceiptTestCase.TestCaseParams(
                article_in_basket=article.create(
                    quantity=1,
                    product_name='test-product-2',
                    product_unit_price=Decimal('1'),
                ),
                taxes_to_apply=[tax.Tax(id='test-tax', rate=Decimal('0.1'))],
            ),
        ],
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='test-product',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('2.2'),
                ),
                receipt.ReceiptItem(
                    description='test-product-2',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.1'),
                ),
            ],
            taxes_due=Decimal('0.2') + Decimal('0.1'),
            total_due=Decimal('2.2') + Decimal('1.1'),
        )
    ),
    'multiple articles in basket, multiple taxes each': CreateReceiptTestCase(
        params=[
            CreateReceiptTestCase.TestCaseParams(
                article_in_basket=article.create(
                    quantity=1,
                    product_name='test-product',
                    product_unit_price=Decimal('2'),
                ),
                taxes_to_apply=[
                    tax.Tax(id='test-tax', rate=Decimal('0.1')),
                    tax.Tax(id='test-tax-2', rate=Decimal('0.1')),
                ],
            ),
            CreateReceiptTestCase.TestCaseParams(
                article_in_basket=article.create(
                    quantity=1,
                    product_name='test-product-2',
                    product_unit_price=Decimal('1'),
                ),
                taxes_to_apply=[
                    tax.Tax(id='test-tax', rate=Decimal('0.1')),
                    tax.Tax(id='test-tax-2', rate=Decimal('0.1')),
                    tax.Tax(id='test-tax-3', rate=Decimal('0.05')),
                ],
            ),
        ],
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='test-product',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('2') + Decimal('0.2') + Decimal('0.2'),
                ),
                receipt.ReceiptItem(
                    description='test-product-2',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1') + Decimal('0.1') + Decimal('0.1') + Decimal('0.05'),
                ),
            ],
            taxes_due=Decimal('0.4') + Decimal('0.25'),
            total_due=Decimal('2.4') + Decimal('1.25'),
        )
    )
}

create_receipt_test_cases = pytest.mark.parametrize(
    'case',
    [pytest.param(case, id=id) for id, case in TEST_CASES.items()],
)


@pytest.fixture
def info():
    def noop(msg: str):
        pass
    return Mock(wraps=noop)


@pytest.fixture
def make_create_basket_fixture():
    def build(params: List[CreateReceiptTestCase.TestCaseParams]):
        return Mock(return_value=[p.article_in_basket for p in params])
    return build


@pytest.fixture
def make_add_taxes_fixture():
    def build(params: List[CreateReceiptTestCase.TestCaseParams]):
        return Mock(return_value=[
            receipt.ItemToInsert(
                description=p.article_in_basket.product.name,
                quantity=p.article_in_basket.quantity,
                unit_price_before_taxes=p.article_in_basket.product.unit_price,
                taxes_to_apply=p.taxes_to_apply,
            ) for p in params
        ])
    return build


@pytest.fixture
def make_env_fixture(info, make_add_taxes_fixture, make_create_basket_fixture):
    def build(params, **overrides):
        return create_receipt.Environment(**{
            'info': info,
            'create_basket': make_create_basket_fixture(params),
            'add_taxes': make_add_taxes_fixture(params),
            **overrides,
        })
    return build


@create_receipt_test_cases
def test_create_returns_use_case(case):
    articles_in_basket = [p.article_in_basket for p in case.params]
    run = create_receipt.create(articles=sentinel.articles)
    assert isinstance(run, create_receipt.CreateReceiptUseCase)


@create_receipt_test_cases
def test_use_case_returns_receipt_from_articles(case, make_env_fixture):
    run = create_receipt.create(articles=sentinel.articles)
    env = make_env_fixture(case.params)
    assert case.expected == run(env)


@create_receipt_test_cases
def test_use_case_calls_create_basket_with_input_articles(case, make_env_fixture):
    run = create_receipt.create(articles=sentinel.articles)
    env = make_env_fixture(case.params)
    run(env)
    assert [call(sentinel.articles)] == env.create_basket.call_args_list


@create_receipt_test_cases
def test_use_case_calls_add_taxes_with_articles_from_basket(case, make_env_fixture):
    run = create_receipt.create(articles=sentinel.articles)
    env = make_env_fixture(case.params)
    run(env)
    assert [call(env.create_basket.return_value)] == env.add_taxes.call_args_list
