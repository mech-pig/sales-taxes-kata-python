import re
from decimal import Decimal

from taxes.services.basket.entities.purchased_item import PurchasedItem


class ParserError:
    class MalformedInput(Exception):
        pass


RE_SPACE = r'\s'
RE_GROUP_QUANTITY = r'(?P<quantity>\d+)'
RE_GROUP_PRODUCT_DESCRIPTION = r'(?P<product_description>.+)'
RE_UNIT_PRICE_TAG = r'at'
RE_GROUP_UNIT_PRICE = r'(?P<unit_price>\d+(\.\d*)?)'

RE_PARSE_ROW = ''.join([
    r'^',
    RE_SPACE.join([
        RE_GROUP_QUANTITY,
        RE_GROUP_PRODUCT_DESCRIPTION,
        RE_UNIT_PRICE_TAG,
        RE_GROUP_UNIT_PRICE
    ]),
    r'$',
])

parse_row = re.compile(RE_PARSE_ROW).match


IMPORTED_LABEL = 'imported'


def parse_description(description):
    tokens = description.split()
    lowercase_tokens = [t.lower() for t in tokens]
    try:
        imported_token_location = lowercase_tokens.index(IMPORTED_LABEL)
    except ValueError:
        return {
            'imported': False,
            'product_name': ' '.join(tokens)
        }
    else:
        imported_token = tokens[imported_token_location]
        tokens.remove(imported_token)
        return {
            'imported': True,
            'product_name': ' '.join(tokens)
        }


def parse_item(input: str) -> PurchasedItem:
    """ Parses the :param input: string and returns a PurchasedItem. """
    parsed = parse_row(input)

    if not parsed:
        raise ParserError.MalformedInput()

    parsed_description = parse_description(parsed['product_description'])

    return PurchasedItem(
        quantity=int(parsed['quantity']),
        product_name=parsed_description['product_name'],
        unit_price=Decimal(parsed['unit_price']),
        imported=parsed_description['imported'],
    )
