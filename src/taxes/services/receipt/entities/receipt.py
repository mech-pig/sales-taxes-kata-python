from dataclasses import dataclass
from decimal import Decimal
from functools import reduce
from typing import List

from taxes.services.receipt.entities import tax


@dataclass(frozen=True)
class Receipt:
    items: List['ReceiptItem']


@dataclass(frozen=True)
class ReceiptItem:
    description: str
    quantity: int
    unit_price_before_taxes: Decimal
    taxes_to_apply: List[tax.Tax]


@dataclass(frozen=True)
class FinalizedReceipt:
    items: List['FinalizedReceiptItem']
    taxes_due: Decimal
    total_due: Decimal


@dataclass(frozen=True)
class FinalizedReceiptItem:
    description: str
    quantity: int
    subtotal_price_with_taxes: Decimal


def empty():
    return Receipt(items=[])


def finalize_item(finalized: FinalizedReceipt, item: ReceiptItem) -> FinalizedReceipt:
    taxed_item = FinalizedReceiptItem(
        description=item.description,
        quantity=item.quantity,
        subtotal_price_with_taxes=tax.apply(item.unit_price_before_taxes, item.taxes_to_apply),
    )

    item_taxes_due = taxed_item.subtotal_price_with_taxes - item.unit_price_before_taxes

    return FinalizedReceipt(
        items=[*finalized.items, taxed_item],
        taxes_due=finalized.taxes_due + item_taxes_due,
        total_due=finalized.total_due + taxed_item.subtotal_price_with_taxes,
    )


def finalize(receipt: Receipt) -> FinalizedReceipt:
    return reduce(
        finalize_item,
        receipt.items,
        FinalizedReceipt(items=[], taxes_due=Decimal('0'), total_due=Decimal('0')),
    )
