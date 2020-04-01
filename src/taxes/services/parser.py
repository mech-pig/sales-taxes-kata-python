import re
from decimal import Decimal

from taxes.services.receipt.entities.item import Item, InvalidItemError


RE_SPACE = r'\s'
RE_GROUP_QUANTITY = r'(?P<quantity>\d+)'
RE_GROUP_PRODUCT_NAME = r'(?P<product_name>.+)'
RE_UNIT_PRICE_TAG = r'at'
RE_GROUP_UNIT_PRICE = r'(?P<unit_price>\d+(\.\d*)?)'

RE_ITEM = ''.join([
    r'^',
    RE_SPACE.join([
        RE_GROUP_QUANTITY,
        RE_GROUP_PRODUCT_NAME,
        RE_UNIT_PRICE_TAG,
        RE_GROUP_UNIT_PRICE
    ]),
    r'$',
])

match_item_parts = re.compile(RE_ITEM).match


def parse_item(input: str):
    """ Parses the :param input: string and returns an :param Item: """
    parsed = match_item_parts(input)
    if not parsed:
        raise InvalidItemError()
    return Item(
        quantity=int(parsed['quantity']),
        product_name=parsed['product_name'].lower(),
        unit_price=Decimal(parsed['unit_price']),
    )
