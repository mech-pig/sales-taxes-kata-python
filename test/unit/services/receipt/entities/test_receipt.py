from dataclasses import dataclass
from decimal import Decimal

import pytest

from taxes.services.receipt.entities import receipt
from taxes.services.tax.entities import tax


def test_empty_returns_receipt_without_items():
    expected = receipt.Receipt(
        items=[],
        taxes_due=Decimal('0'),
        total_due=Decimal('0'),
    )
    assert expected == receipt.empty()


@dataclass
class AddToReceiptTestCase:
    to_add: receipt.ItemToInsert
    initial: receipt.Receipt
    expected: receipt.Receipt


ADD_TO_RECEIPT_TEST_CASES = {
    'empty receipt, quantity = 1, no taxes': AddToReceiptTestCase(
        initial=receipt.empty(),
        to_add=receipt.ItemToInsert(
            description='a test item',
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
            taxes_to_apply=[]
        ),
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1'),
                )
            ],
            taxes_due=Decimal('0'),
            total_due=Decimal('1'),
        )
    ),
    'empty receipt, quantity = 1, single tax': AddToReceiptTestCase(
        initial=receipt.empty(),
        to_add=receipt.ItemToInsert(
            description='a test item',
            quantity=1,
            unit_price_before_taxes=Decimal('1'),
            taxes_to_apply=[tax.Tax(rate=Decimal('0.1'), id='10%')]
        ),
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.1'),
                )
            ],
            taxes_due=Decimal('0.1'),
            total_due=Decimal('1.1'),
        )
    ),
    'empty receipt, quantity > 1, no taxes': AddToReceiptTestCase(
        initial=receipt.empty(),
        to_add=receipt.ItemToInsert(
            description='a test item',
            quantity=3,
            unit_price_before_taxes=Decimal('1'),
            taxes_to_apply=[]
        ),
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=3,
                    subtotal_price_with_taxes=Decimal('3'),
                )
            ],
            taxes_due=Decimal('0'),
            total_due=Decimal('3'),
        )
    ),
    'empty receipt, quantity > 1, single tax': AddToReceiptTestCase(
        initial=receipt.empty(),
        to_add=receipt.ItemToInsert(
            description='a test item',
            quantity=3,
            unit_price_before_taxes=Decimal('1'),
            taxes_to_apply=[tax.Tax(rate=Decimal('0.1'), id='10%')]
        ),
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=3,
                    subtotal_price_with_taxes=Decimal('3.3'),
                )
            ],
            taxes_due=Decimal('0.3'),
            total_due=Decimal('3.3'),
        )
    ),
    'empty receipt, quantity > 1, multiple taxes': AddToReceiptTestCase(
        initial=receipt.empty(),
        to_add=receipt.ItemToInsert(
            description='a test item',
            quantity=2,
            unit_price_before_taxes=Decimal('1'),
            taxes_to_apply=[
                tax.Tax(rate=Decimal('0.1'), id='10%'),
                tax.Tax(rate=Decimal('0.05'), id='5%'),
            ]
        ),
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=2,
                    subtotal_price_with_taxes=Decimal('2.30'),
                )
            ],
            taxes_due=Decimal('0.3'),
            total_due=Decimal('2.30'),
        )
    ),
    'receipt with items, quantity > 1, multiple taxes': AddToReceiptTestCase(
        initial=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=2,
                    subtotal_price_with_taxes=Decimal('2.30'),
                )
            ],
            taxes_due=Decimal('0.3'),
            total_due=Decimal('2.30'),
        ),
        to_add=receipt.ItemToInsert(
            description='a test item 2',
            quantity=3,
            unit_price_before_taxes=Decimal('2'),
            taxes_to_apply=[
                tax.Tax(rate=Decimal('0.2'), id='20%'),
                tax.Tax(rate=Decimal('0.1'), id='10%'),
                tax.Tax(rate=Decimal('0.05'), id='5%'),
            ]
        ),
        expected=receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=2,
                    subtotal_price_with_taxes=Decimal('2.30'),
                ),
                receipt.ReceiptItem(
                    description='a test item 2',
                    quantity=3,
                    subtotal_price_with_taxes=3 * (Decimal('2') + Decimal('0.4') + Decimal('0.2') + Decimal('0.1')),
                )
            ],
            taxes_due=Decimal('0.3') + 3 * (Decimal('0.4') + Decimal('0.2') + Decimal('0.1')),
            total_due=Decimal('2.30') + 3 * (Decimal('2') + Decimal('0.4') + Decimal('0.2') + Decimal('0.1')),
        )
    )
}

@pytest.mark.parametrize('case', [
    pytest.param(case, id=id) for id, case in ADD_TO_RECEIPT_TEST_CASES.items()
])
def test_add_to_receipt_returns_receipt_with_added_item(case):
    assert case.expected == receipt.add_to_receipt(to_add=case.to_add, receipt=case.initial)
