from dataclasses import dataclass
from decimal import Decimal
from typing import List
from unittest.mock import call, Mock

import pytest

from taxes.services.basket.entities import article
from taxes.services.receipt.entities import receipt, tax
from taxes.services.receipt.use_cases import create_receipt


@dataclass
class CreateReceiptTestCase:
    input: List['TestCaseInput']
    expected: receipt.Receipt

    @dataclass
    class TestCaseInput:
        article: article.Article
        taxes_to_apply: List[tax.Tax]


TEST_CASES = {
    'no articles in basket': CreateReceiptTestCase(
        input=[],
        expected=receipt.empty()
    ),
    'single article in basket, with no taxes': CreateReceiptTestCase(
        input=[
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=1,
                    product_name='test-product',
                    product_unit_price=Decimal('1'),
                    imported=False,
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
        input=[
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=3,
                    product_name='test-product',
                    product_unit_price=Decimal('1'),
                    imported=False,
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
        input=[
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=1,
                    product_name='test-product',
                    product_unit_price=Decimal('2'),
                    imported=False,
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
        input=[
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=1,
                    product_name='test-product',
                    product_unit_price=Decimal('2'),
                    imported=False,
                ),
                taxes_to_apply=[tax.Tax(id='test-tax', rate=Decimal('0.1'))],
            ),
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=1,
                    product_name='test-product-2',
                    product_unit_price=Decimal('1'),
                    imported=True,
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
        input=[
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=1,
                    product_name='test-product',
                    product_unit_price=Decimal('2'),
                    imported=False,
                ),
                taxes_to_apply=[
                    tax.Tax(id='test-tax', rate=Decimal('0.1')),
                    tax.Tax(id='test-tax-2', rate=Decimal('0.1')),
                ],
            ),
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=1,
                    product_name='test-product-2',
                    product_unit_price=Decimal('1'),
                    imported=True,
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
def make_add_taxes_fixture():
    def build(input: List[CreateReceiptTestCase.TestCaseInput]):
        return Mock(return_value=[
            receipt.ItemToInsert(
                description=i.article.product.name,
                quantity=i.article.quantity,
                unit_price_before_taxes=i.article.product.unit_price,
                taxes_to_apply=i.taxes_to_apply,
            ) for i in input
        ])
    return build


@pytest.fixture
def make_env_fixture(info, make_add_taxes_fixture):
    def build(params, **overrides):
        return create_receipt.Environment(**{
            'info': info,
            'add_taxes': make_add_taxes_fixture(params),
            **overrides,
        })
    return build


@create_receipt_test_cases
def test_create_returns_use_case(case):
    articles = [i.article for i in case.input]
    run = create_receipt.create(articles=articles)
    assert isinstance(run, create_receipt.CreateReceiptUseCase)


@create_receipt_test_cases
def test_use_case_returns_receipt_from_articles(case, make_env_fixture):
    articles = [i.article for i in case.input]
    run = create_receipt.create(articles=articles)
    env = make_env_fixture(case.input)
    assert case.expected == run(env)


@create_receipt_test_cases
def test_use_case_calls_add_taxes_with_articles(case, make_env_fixture):
    articles = [i.article for i in case.input]
    run = create_receipt.create(articles=articles)
    env = make_env_fixture(case.input)
    run(env)
    assert [call(articles)] == env.add_taxes.call_args_list
