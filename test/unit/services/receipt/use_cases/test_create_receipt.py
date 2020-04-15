from dataclasses import dataclass
from decimal import Decimal
from typing import List
from unittest.mock import call, Mock

import pytest

from taxes.services.basket.entities import article
from taxes.services.receipt.entities import receipt
from taxes.services.receipt.entities.taxed_article import TaxedArticle
from taxes.services.receipt.use_cases import CreateReceiptUseCase


@dataclass
class CreateReceiptTestCase:
    input: List['TestCaseInput']
    expected: receipt.Receipt

    @dataclass
    class TestCaseInput:
        article: article.Article
        tax_amount_due_per_unit: Decimal


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
                    product_category='cat-dummy',
                    unit_price_before_taxes=Decimal('1'),
                    imported=False,
                ),
                tax_amount_due_per_unit=Decimal('0'),
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
    'single imported article in basket, with no taxes': CreateReceiptTestCase(
        input=[
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=1,
                    product_name='test-product',
                    product_category='cat-dummy',
                    unit_price_before_taxes=Decimal('1'),
                    imported=True,
                ),
                tax_amount_due_per_unit=Decimal('0'),
            ),
        ],
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='imported test-product',
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
                    product_category='cat-dummy',
                    unit_price_before_taxes=Decimal('1'),
                    imported=False,
                ),
                tax_amount_due_per_unit=Decimal('0'),
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
    'single article in basket, with taxes': CreateReceiptTestCase(
        input=[
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=1,
                    product_name='test-product',
                    product_category='cat-dummy',
                    unit_price_before_taxes=Decimal('2'),
                    imported=False,
                ),
                tax_amount_due_per_unit=Decimal('0.2'),
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
    'single article in basket (quantity > 1), with taxes': CreateReceiptTestCase(
        input=[
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=3,
                    product_name='test-product',
                    product_category='cat-dummy',
                    unit_price_before_taxes=Decimal('1'),
                    imported=False,
                ),
                tax_amount_due_per_unit=Decimal('0.05'),
            ),
        ],
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='test-product',
                    quantity=3,
                    subtotal_price_with_taxes=Decimal('3.15'),
                ),
            ],
            taxes_due=Decimal('0.15'),
            total_due=Decimal('3.15'),
        )
    ),
    'multiple articles in basket, with taxes': CreateReceiptTestCase(
        input=[
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=1,
                    product_name='test-product',
                    product_category='cat-dummy',
                    unit_price_before_taxes=Decimal('2'),
                    imported=False,
                ),
                tax_amount_due_per_unit=Decimal('0.2'),
            ),
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=1,
                    product_name='test-product-2',
                    product_category='cat-dummy',
                    unit_price_before_taxes=Decimal('1'),
                    imported=True,
                ),
                tax_amount_due_per_unit=Decimal('0.1'),
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
                    description='imported test-product-2',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.1'),
                ),
            ],
            taxes_due=Decimal('0.2') + Decimal('0.1'),
            total_due=Decimal('2.2') + Decimal('1.1'),
        )
    ),
    'multiple articles in basket (quantity > 1), with taxes': CreateReceiptTestCase(
        input=[
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=2,
                    product_name='test-product',
                    product_category='cat-dummy',
                    unit_price_before_taxes=Decimal('2'),
                    imported=False,
                ),
                tax_amount_due_per_unit=Decimal('0.1'),
            ),
            CreateReceiptTestCase.TestCaseInput(
                article=article.create(
                    quantity=3,
                    product_name='test-product-2',
                    product_category='cat-dummy',
                    unit_price_before_taxes=Decimal('1'),
                    imported=True,
                ),
                tax_amount_due_per_unit=Decimal('0.1'),
            ),
        ],
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='test-product',
                    quantity=2,
                    subtotal_price_with_taxes=Decimal('4.2'),
                ),
                receipt.ReceiptItem(
                    description='imported test-product-2',
                    quantity=3,
                    subtotal_price_with_taxes=Decimal('3.3'),
                ),
            ],
            taxes_due=Decimal('0.2') + Decimal('0.3'),
            total_due=Decimal('4.2') + Decimal('3.3'),
        )
    ),
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
            TaxedArticle(
                product=i.article.product,
                quantity=i.article.quantity,
                imported=i.article.imported,
                unit_price_before_taxes=i.article.unit_price_before_taxes,
                tax_amount_due_per_unit=i.tax_amount_due_per_unit,
            ) for i in input
        ])
    return build


@pytest.fixture
def make_env_fixture(info, make_add_taxes_fixture):
    def build(params, **overrides):
        return CreateReceiptUseCase.Environment(**{
            'info': info,
            'add_taxes': make_add_taxes_fixture(params),
            **overrides,
        })
    return build


@create_receipt_test_cases
def test_use_case_returns_receipt_from_articles(case, make_env_fixture):
    articles = [i.article for i in case.input]
    run = CreateReceiptUseCase(articles=articles)
    env = make_env_fixture(case.input)
    assert case.expected == run(env)


@create_receipt_test_cases
def test_use_case_calls_add_taxes_with_articles(case, make_env_fixture):
    articles = [i.article for i in case.input]
    run = CreateReceiptUseCase(articles=articles)
    env = make_env_fixture(case.input)
    run(env)
    assert [call(articles)] == env.add_taxes.call_args_list
