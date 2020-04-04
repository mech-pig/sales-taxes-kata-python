import re
from decimal import Decimal


class ParserError:
    class MalformedInput(Exception):
        pass


RE_SPACE = r'\s'
RE_GROUP_QUANTITY = r'(?P<quantity>\d+)'
RE_GROUP_PRODUCT_NAME = r'(?P<product_name>.+)'
RE_UNIT_PRICE_TAG = r'at'
RE_GROUP_UNIT_PRICE = r'(?P<unit_price>\d+(\.\d*)?)'

RE_PARSE_ROW = ''.join([
    r'^',
    RE_SPACE.join([
        RE_GROUP_QUANTITY,
        RE_GROUP_PRODUCT_NAME,
        RE_UNIT_PRICE_TAG,
        RE_GROUP_UNIT_PRICE
    ]),
    r'$',
])

parse_row = re.compile(RE_PARSE_ROW).match


def parse_item(input: str):
    """ Parses the :param input: string and returns a dictionary representing
    the parsed item. """
    parsed = parse_row(input)
    if not parsed:
        raise ParserError.MalformedInput()
    return {
        'quantity': int(parsed['quantity']),
        'product_name': parsed['product_name'].lower(),
        'unit_price': Decimal(parsed['unit_price']),
    }
