from decimal import Decimal

import pytest

from taxes.services.receipt.entities import receipt, tax


def test_empty_returns_receipt_without_items():
    expected = receipt.Receipt(items=[])
    assert expected == receipt.empty()


@pytest.mark.parametrize('input_receipt, printed_receipt', [
    pytest.param(
        receipt.empty(),
        receipt.FinalizedReceipt(
            items=[],
            taxes_due=Decimal('0'),
            total_due=Decimal('0'),
        ),
        id='empty receipt',
    ),
    pytest.param(
        receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=1,
                    unit_price_before_taxes=Decimal('1'),
                    taxes_to_apply=[tax.Tax(rate=Decimal('0.1'), id='10%')]
                ),
            ],
        ),
        receipt.FinalizedReceipt(
            items=[
                receipt.FinalizedReceiptItem(
                    description='a test item',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.1'),
                )
            ],
            taxes_due=Decimal('0.1'),
            total_due=Decimal('1.1'),
        ),
        id='single item with single tax',
    ),
    pytest.param(
        receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=1,
                    unit_price_before_taxes=Decimal('1.04'),
                    taxes_to_apply=[tax.Tax(rate=Decimal('0.1'), id='10%')]
                ),
            ],
        ),
        receipt.FinalizedReceipt(
            items=[
                receipt.FinalizedReceiptItem(
                    description='a test item',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.14'),
                )
            ],
            taxes_due=Decimal('0.10'),
            total_due=Decimal('1.14'),
        ),
        id='single item with single tax (tax amount rounded down)',
    ),
    pytest.param(
        receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=1,
                    unit_price_before_taxes=Decimal('1.48'),
                    taxes_to_apply=[tax.Tax(rate=Decimal('0.1'), id='10%')]
                ),
            ],
        ),
        receipt.FinalizedReceipt(
            items=[
                receipt.FinalizedReceiptItem(
                    description='a test item',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.63'),
                )
            ],
            taxes_due=Decimal('0.15'),
            total_due=Decimal('1.63'),
        ),
        id='single item with single tax (tax amount rounded up)',
    ),
    pytest.param(
        receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=1,
                    unit_price_before_taxes=Decimal('1'),
                    taxes_to_apply=[
                        tax.Tax(rate=Decimal('0.1'), id='10%'),
                        tax.Tax(rate=Decimal('0.2'), id='20%')
                    ]
                ),
            ],
        ),
        receipt.FinalizedReceipt(
            items=[
                receipt.FinalizedReceiptItem(
                    description='a test item',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.3'),
                )
            ],
            taxes_due=Decimal('0.3'),
            total_due=Decimal('1.3'),
        ),
        id='single item with multiple taxes',
    ),
    pytest.param(
        receipt.Receipt(
            items=[
                receipt.ReceiptItem(
                    description='a test item',
                    quantity=1,
                    unit_price_before_taxes=Decimal('1'),
                    taxes_to_apply=[
                        tax.Tax(rate=Decimal('0.1'), id='10%'),
                        tax.Tax(rate=Decimal('0.2'), id='20%'),
                    ]
                ),
                receipt.ReceiptItem(
                    description='a second test item',
                    quantity=1,
                    unit_price_before_taxes=Decimal('2'),
                    taxes_to_apply=[
                        tax.Tax(rate=Decimal('0.3'), id='30%'),
                        tax.Tax(rate=Decimal('0.05'), id='5%'),
                    ]
                ),
            ],
        ),
        receipt.FinalizedReceipt(
            items=[
                receipt.FinalizedReceiptItem(
                    description='a test item',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('1.3'),
                ),
                receipt.FinalizedReceiptItem(
                    description='a second test item',
                    quantity=1,
                    subtotal_price_with_taxes=Decimal('2.7'),
                )
            ],
            taxes_due=Decimal('1'),
            total_due=Decimal('4'),
        ),
        id='multiple items with multiple taxes',
    ),
])
def test_finalize_returns_finalized_receipt_with_taxes_applied(
    input_receipt,
    printed_receipt,
):
    assert printed_receipt == receipt.finalize(input_receipt)
