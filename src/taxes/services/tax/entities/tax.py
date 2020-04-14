from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from functools import reduce
from typing import Iterable


@dataclass(frozen=True)
class Tax:
    rate: Decimal
    id: str


class TaxError:
    class NonPositiveRate(Exception):
        def __init__(self, value):
            super().__init__(f'rate must be positive: {value}')


def create(id: str, rate: Decimal):
    """ Return a Tax object.

    Raise exception if :param rate: is less than 0.
    """
    if rate <= 0:
        raise TaxError.NonPositiveRate(rate)

    return Tax(id=id, rate=rate)


def round_tax_amount(amount: Decimal) -> Decimal:
    """ Round tax amount up to the nearest `0.05`. """
    precision = Decimal('0.05')
    return (amount / precision).quantize(0, ROUND_HALF_UP) * precision


def calculate_tax_amount(price: Decimal, tax: Tax) -> Decimal:
    """ Calculate the amount due to :param tax: for a price :param price:.

    The amount is calculated by multiplying :param price: and the rate of
    :param tax: and then by rouding the result to the nearest '0.05'.
    """
    return round_tax_amount(price * tax.rate)


def apply(price: Decimal, taxes: Iterable[Tax]) -> Decimal:
    """ Apply :param taxes: to :param price: and return the amount due. """
    def add_to_subtotal(subtotal: Decimal, tax: Tax) -> Decimal:
        return subtotal + calculate_tax_amount(price, tax)

    return reduce(add_to_subtotal, taxes, Decimal('0.00'))
