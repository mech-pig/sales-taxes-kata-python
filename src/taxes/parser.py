import re

from taxes.item import Item, InvalidItemError


RE_GROUP_QUANTITY = r'(?P<quantity>\d+)'
RE_GROUP_PRODUCT_NAME = r'(?P<product_name>.+)'
RE_ITEM = ''.join([
    r'^',
    RE_GROUP_QUANTITY,
    r'\s',
    RE_GROUP_PRODUCT_NAME,
    r' at ',
    r'.*$',
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
    )
