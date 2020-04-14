from dataclasses import dataclass
from decimal import Decimal

import pytest

from taxes.services.basket.entities.product import Product
from taxes.services.receipt.entities.receipt import (
    add_to_receipt,
    describe,
    empty as create_empty_receipt,
    Receipt,
    ReceiptItem,
)
from taxes.services.receipt.entities.taxed_article import TaxedArticle
from taxes.services.tax.entities import tax


def test_empty_returns_receipt_without_items():
    expected = Receipt(
        items=[],
        taxes_due=Decimal('0'),
        total_due=Decimal('0'),
    )
    assert expected == create_empty_receipt()


@pytest.mark.parametrize('input, expected', [
    pytest.param(
        TaxedArticle(
            product=Product(name='a', category='dummy'),
            imported=False,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
            tax_amount_due_per_unit=Decimal('0'),
        ),
        'a',
        id='non imported article'
    ),
    pytest.param(
        TaxedArticle(
            product=Product(name='a', category='dummy'),
            imported=True,
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
            tax_amount_due_per_unit=Decimal('0'),
        ),
        'imported a',
        id='imported article'
    ),
])
def test_describe_returns_article_description(input, expected):
    assert expected == describe(input)


@dataclass
class AddToReceiptTestCase:
    input: 'TestCaseInput'
    expected: Receipt

    @dataclass
    class TestCaseInput:
        to_add: TaxedArticle
        receipt: Receipt


ADD_TO_RECEIPT_TEST_CASES = {
    'empty receipt, quantity = 1, no taxes': AddToReceiptTestCase(
        input=AddToReceiptTestCase.TestCaseInput(
            to_add=TaxedArticle(
                product=Product(name='a', category='dummy'),
                imported=False,
                quantity=1,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0'),
            ),
            receipt=create_empty_receipt(),
        ),
        expected=Receipt(
            items=[
                ReceiptItem(
                    description='a',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1'),
                )
            ],
            taxes_due=Decimal('0'),
            total_due=Decimal('1'),
        )
    ),
    'empty receipt, imported article': AddToReceiptTestCase(
        input=AddToReceiptTestCase.TestCaseInput(
            to_add=TaxedArticle(
                product=Product(name='a', category='dummy'),
                imported=True,
                quantity=1,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0'),
            ),
            receipt=create_empty_receipt(),
        ),
        expected=Receipt(
            items=[
                ReceiptItem(
                    description='imported a',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1'),
                )
            ],
            taxes_due=Decimal('0'),
            total_due=Decimal('1'),
        )
    ),
    'empty receipt, quantity = 1, with taxes': AddToReceiptTestCase(
        input=AddToReceiptTestCase.TestCaseInput(
            to_add=TaxedArticle(
                product=Product(name='a', category='dummy'),
                imported=False,
                quantity=1,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0.1'),
            ),
            receipt=create_empty_receipt(),
        ),
        expected=Receipt(
            items=[
                ReceiptItem(
                    description='a',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.1'),
                )
            ],
            taxes_due=Decimal('0.1'),
            total_due=Decimal('1.1'),
        )
    ),
    'empty receipt, quantity > 1, no taxes': AddToReceiptTestCase(
        input=AddToReceiptTestCase.TestCaseInput(
            to_add=TaxedArticle(
                product=Product(name='a', category='dummy'),
                imported=False,
                quantity=3,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0'),
            ),
            receipt=create_empty_receipt(),
        ),
        expected=Receipt(
            items=[
                ReceiptItem(
                    description='a',
                    quantity=3,
                    subtotal_price_with_taxes=Decimal('3'),
                )
            ],
            taxes_due=Decimal('0'),
            total_due=Decimal('3'),
        )
    ),
    'empty receipt, quantity > 1, with taxes': AddToReceiptTestCase(
        input=AddToReceiptTestCase.TestCaseInput(
            to_add=TaxedArticle(
                product=Product(name='a', category='dummy'),
                imported=False,
                quantity=3,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0.1'),
            ),
            receipt=create_empty_receipt(),
        ),
        expected=Receipt(
            items=[
                ReceiptItem(
                    description='a',
                    quantity=3,
                    subtotal_price_with_taxes=Decimal('3.3'),
                )
            ],
            taxes_due=Decimal('0.3'),
            total_due=Decimal('3.3'),
        )
    ),
    'non empty receipt, quantity = 1, no taxes': AddToReceiptTestCase(
        input=AddToReceiptTestCase.TestCaseInput(
            to_add=TaxedArticle(
                product=Product(name='a', category='dummy'),
                imported=False,
                quantity=1,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0'),
            ),
            receipt=Receipt(
                items=[
                    ReceiptItem(
                        description='b',
                        quantity=1,
                        subtotal_price_with_taxes=Decimal('1.1'),
                    )
                ],
                taxes_due=Decimal('0.1'),
                total_due=Decimal('1.1'),
            )
        ),
        expected=Receipt(
            items=[
                ReceiptItem(
                    description='b',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.1'),
                ),
                ReceiptItem(
                    description='a',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1'),
                )
            ],
            taxes_due=Decimal('0.1') + Decimal('0'),
            total_due=Decimal('1.1') + Decimal('1'),
        )
    ),
    'non empty receipt, quantity > 1, no taxes': AddToReceiptTestCase(
        input=AddToReceiptTestCase.TestCaseInput(
            to_add=TaxedArticle(
                product=Product(name='a', category='dummy'),
                imported=False,
                quantity=3,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0'),
            ),
            receipt=Receipt(
                items=[
                    ReceiptItem(
                        description='b',
                        quantity=1,
                        subtotal_price_with_taxes=Decimal('1.1'),
                    )
                ],
                taxes_due=Decimal('0.1'),
                total_due=Decimal('1.1'),
            )
        ),
        expected=Receipt(
            items=[
                ReceiptItem(
                    description='b',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.1'),
                ),
                ReceiptItem(
                    description='a',
                    quantity=3,
                    subtotal_price_with_taxes=Decimal('3'),
                )
            ],
            taxes_due=Decimal('0.1') + Decimal('0'),
            total_due=Decimal('1.1') + Decimal('3'),
        )
    ),
    'non empty receipt, quantity = 1, with taxes': AddToReceiptTestCase(
        input=AddToReceiptTestCase.TestCaseInput(
            to_add=TaxedArticle(
                product=Product(name='a', category='dummy'),
                imported=False,
                quantity=1,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0.2'),
            ),
            receipt=Receipt(
                items=[
                    ReceiptItem(
                        description='b',
                        quantity=1,
                        subtotal_price_with_taxes=Decimal('1.1'),
                    )
                ],
                taxes_due=Decimal('0.1'),
                total_due=Decimal('1.1'),
            )
        ),
        expected=Receipt(
            items=[
                ReceiptItem(
                    description='b',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.1'),
                ),
                ReceiptItem(
                    description='a',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.2'),
                )
            ],
            taxes_due=Decimal('0.1') + Decimal('0.2'),
            total_due=Decimal('1.1') + Decimal('1.2'),
        )
    ),
    'non empty receipt, quantity > 1, with taxes': AddToReceiptTestCase(
        input=AddToReceiptTestCase.TestCaseInput(
            to_add=TaxedArticle(
                product=Product(name='a', category='dummy'),
                imported=False,
                quantity=3,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0.2'),
            ),
            receipt=Receipt(
                items=[
                    ReceiptItem(
                        description='b',
                        quantity=1,
                        subtotal_price_with_taxes=Decimal('1.1'),
                    )
                ],
                taxes_due=Decimal('0.1'),
                total_due=Decimal('1.1'),
            )
        ),
        expected=Receipt(
            items=[
                ReceiptItem(
                    description='b',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.1'),
                ),
                ReceiptItem(
                    description='a',
                    quantity=3,
                    subtotal_price_with_taxes=Decimal('3.6'),
                )
            ],
            taxes_due=Decimal('0.1') + Decimal('0.6'),
            total_due=Decimal('1.1') + Decimal('3.6'),
        )
    ),
    'non empty receipt, quantity > 1, imported article with taxes': AddToReceiptTestCase(
        input=AddToReceiptTestCase.TestCaseInput(
            to_add=TaxedArticle(
                product=Product(name='a', category='dummy'),
                imported=True,
                quantity=3,
                unit_price_before_taxes=Decimal('1'),
                tax_amount_due_per_unit=Decimal('0.2'),
            ),
            receipt=Receipt(
                items=[
                    ReceiptItem(
                        description='b',
                        quantity=1,
                        subtotal_price_with_taxes=Decimal('1.1'),
                    )
                ],
                taxes_due=Decimal('0.1'),
                total_due=Decimal('1.1'),
            )
        ),
        expected=Receipt(
            items=[
                ReceiptItem(
                    description='b',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.1'),
                ),
                ReceiptItem(
                    description='imported a',
                    quantity=3,
                    subtotal_price_with_taxes=Decimal('3.6'),
                )
            ],
            taxes_due=Decimal('0.1') + Decimal('0.6'),
            total_due=Decimal('1.1') + Decimal('3.6'),
        )
    ),
}

@pytest.mark.parametrize('case', [
    pytest.param(case, id=id) for id, case in ADD_TO_RECEIPT_TEST_CASES.items()
])
def test_add_to_receipt_returns_receipt_with_added_item(case):
    receipt = add_to_receipt(taxed_article=case.input.to_add, receipt=case.input.receipt)
    assert case.expected == receipt
