from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal
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
    """ Returns a Receipt without articles. """
    return Receipt(items=[], taxes_due=Decimal('0'), total_due=Decimal('0'))


def add_to_receipt(to_add: ItemToInsert, receipt: Receipt) -> Receipt:
    """ Returns a copy to :param receipt: with :param to_add: added to it. """
    quantity = to_add.quantity
    taxes_to_apply = to_add.taxes_to_apply

    unit_price_before_taxes = to_add.unit_price_before_taxes
    unit_price_with_taxes = tax.apply(unit_price_before_taxes, taxes_to_apply)
    unit_taxes_due = unit_price_with_taxes - unit_price_before_taxes

    subtotal_with_taxes = quantity * unit_price_with_taxes
    subtoal_taxes_due = quantity * unit_taxes_due

    return Receipt(
        items=[
            *deepcopy(receipt.items),
            ReceiptItem(
                description=to_add.description,
                quantity=quantity,
                subtotal_price_with_taxes=subtotal_with_taxes,
            )
        ],
        taxes_due=receipt.taxes_due + subtoal_taxes_due,
        total_due=receipt.total_due + subtotal_with_taxes,
    )
