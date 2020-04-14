from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal
from typing import List


from taxes.services.receipt.entities.taxed_article import TaxedArticle


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


def describe(article):
    imported = 'imported ' if article.imported else ''
    return f'{imported}{article.product.name}'


def add_to_receipt(taxed_article: TaxedArticle, receipt: Receipt) -> Receipt:
    """ Add :param taxed_article: to :param receipt: """
    unit_price_with_taxes = taxed_article.unit_price_before_taxes + taxed_article.tax_amount_due_per_unit   # noqa: E501
    quantity = taxed_article.quantity

    subtotal_taxes_due = quantity * taxed_article.tax_amount_due_per_unit
    subtotal_with_taxes = quantity * unit_price_with_taxes

    return Receipt(
        items=[
            *deepcopy(receipt.items),
            ReceiptItem(
                description=describe(taxed_article),
                quantity=quantity,
                subtotal_price_with_taxes=subtotal_with_taxes,
            )
        ],
        taxes_due=receipt.taxes_due + subtotal_taxes_due,
        total_due=receipt.total_due + subtotal_with_taxes,
    )
