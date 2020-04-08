from dataclasses import dataclass
from decimal import Decimal
from functools import reduce
from typing import List

from taxes.services.receipt.entities import tax


@dataclass(frozen=True)
class ItemToInsert:
    description: str
    quantity: int
    unit_price_before_taxes: Decimal
    taxes_to_apply: List[tax.Tax]


@dataclass(frozen=True)
class Receipt:
    items: List['ReceiptItem']
    taxes_due: Decimal
    total_due: Decimal


@dataclass(frozen=True)
class ReceiptItem:
    description: str
    quantity: int
    subtotal_price_with_taxes: Decimal


def empty():
    return Receipt(items=[], taxes_due=Decimal('0'), total_due=Decimal('0'))


def insert_item(to_insert: ItemToInsert, receipt: Receipt) -> Receipt:
    new_receipt_item = ReceiptItem(
        description=to_insert.description,
        quantity=to_insert.quantity,
        subtotal_price_with_taxes=tax.apply(
            to_insert.unit_price_before_taxes,
            to_insert.taxes_to_apply,
        ),
    )

    item_taxes_due = new_receipt_item.subtotal_price_with_taxes - to_insert.unit_price_before_taxes

    return Receipt(
        items=[*receipt.items, new_receipt_item],
        taxes_due=receipt.taxes_due + item_taxes_due,
        total_due=receipt.total_due + new_receipt_item.subtotal_price_with_taxes,
    )


def finalize(items_to_insert: List[ItemToInsert]) -> Receipt:
    return reduce(
        lambda receipt, to_insert: insert_item(to_insert, receipt),
        items_to_insert,
        empty(),
    )
