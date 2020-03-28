import re

from taxes.item import Item, InvalidItemError


RE_GROUP_QUANTITY = r'(?P<quantity>\d+)'
RE_ITEM = ''.join([
    r'^',
    RE_GROUP_QUANTITY,
    r'\s',
    r'.*$',
])

match_item_parts = re.compile(RE_ITEM).match


def parse_item(input: str):
    """ Parses the :param input: string and returns an :param Item: """
    parsed = match_item_parts(input)
    if not parsed:
        raise InvalidItemError()
    return Item(quantity=int(parsed['quantity']))
