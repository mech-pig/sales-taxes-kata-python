from decimal import Decimal

import pytest

from taxes.services.receipt.entities.item import InvalidItemError
from taxes.services.parser import parse_item


@pytest.mark.parametrize('text, quantity, product_name, unit_price', [
    # quantity
    pytest.param('1 book at 12.49', 1, 'book', Decimal('12.49'), id='quantity: = 1'),
    pytest.param('2 book at 12.49', 2, 'book', Decimal('12.49'), id='quantity: > 1'),
    pytest.param('99 book at 12.49', 99, 'book', Decimal('12.49'), id='quantity: > 9'),
    pytest.param('10000000 book at 12.49', 10000000, 'book', Decimal('12.49'), id='quantity: a very big number'),

    # name
    pytest.param('1 item at 12.39', 1, 'item', Decimal('12.39'), id='product name: ascii lowercase word'),
    pytest.param('1 ITEM at 12.39', 1, 'item', Decimal('12.39'), id='product name: ascii uppercase word'),
    pytest.param('1 ItEm at 12.39', 1, 'item', Decimal('12.39'), id='product name: ascii mixed-case word'),
    pytest.param('1 1-t_e.m! at 12.39', 1, '1-t_e.m!', Decimal('12.39'), id='product name: ascii string with symbols'),
    pytest.param('1 👍👍👍 at 12.39', 1, '👍👍👍', Decimal('12.39'), id='product name: unicode word'),
    pytest.param('1 this is an item at 12.39', 1, 'this is an item', Decimal('12.39'), id='product name: ascii string with spaces'),

    # unit price
    pytest.param('1 item at 0', 1, 'item', Decimal('0'), id='unit price: zero with no decimal part'),
    pytest.param('1 item at 00', 1, 'item', Decimal('0'), id='unit price: zero with single leading zero'),
    pytest.param('1 item at 000', 1, 'item', Decimal('0'), id='unit price: zero with multiple leading zeros'),
    pytest.param('1 item at 0.', 1, 'item', Decimal('0'), id='unit price: zero with no trailing zeros'),
    pytest.param('1 item at 00.', 1, 'item', Decimal('0'), id='unit price: zero with single leading zero and no trailing zeros'),
    pytest.param('1 item at 000.', 1, 'item', Decimal('0'), id='unit price: zero with multiple leading zeros and no trailing zeros'),
    pytest.param('1 item at 0.0', 1, 'item', Decimal('0'), id='unit price: zero with single trailing zero'),
    pytest.param('1 item at 00.0', 1, 'item', Decimal('0'), id='unit price: zero with single leading zero and single trailing zero'),
    pytest.param('1 item at 000.0', 1, 'item', Decimal('0'), id='unit price: zero with multiple leading zeros and single trailing zero'),
    pytest.param('1 item at 0.000', 1, 'item', Decimal('0'), id='unit price: zero with multiple trailing zeros'),
    pytest.param('1 item at 00.000', 1, 'item', Decimal('0'), id='unit price: zero with single leading zero and multiple trailing zeros'),
    pytest.param('1 item at 000.000', 1, 'item', Decimal('0'), id='unit price: zero with multiple leading zeros and multiple trailing zeros'),

    pytest.param('1 item at 0.1', 1, 'item', Decimal('0.1'), id='unit price: single-digit decimal (< 1) with single decimal digit'),
    pytest.param('1 item at 0.0113', 1, 'item', Decimal('0.0113'), id='unit price: single-digit decimal (< 1) with multiple decimal digits'),
    pytest.param('1 item at 0.10', 1, 'item', Decimal('0.1'), id='unit price: single-digit decimal (< 1) with single decimal digit and single trailing zero'),
    pytest.param('1 item at 0.1000', 1, 'item', Decimal('0.1'), id='unit price: single-digit decimal (< 1) with single decimal digit and multiple trailing zeros'),
    pytest.param('1 item at 00.1', 1, 'item', Decimal('0.1'), id='unit price: single-digit decimal (< 1) with single leading zero and single decimal digit'),
    pytest.param('1 item at 00.0113', 1, 'item', Decimal('0.0113'), id='unit price: single-digit decimal (< 1) with single leading zero and multiple decimal digits'),
    pytest.param('1 item at 00.10', 1, 'item', Decimal('0.1'), id='unit price: single-digit decimal (< 1) with single leading zero and single decimal digit and single trailing zero'),
    pytest.param('1 item at 00.1000', 1, 'item', Decimal('0.1'), id='unit price: single-digit decimal (< 1) with single leading zero and single decimal digit and multiple trailing zeros'),

    pytest.param('1 item at 1', 1, 'item', Decimal('1'), id='unit price: single-digit integer with no decimal part'),
    pytest.param('1 item at 1.', 1, 'item', Decimal('1'), id='unit price: single-digit integer with no trailing zero'),
    pytest.param('1 item at 1.0', 1, 'item', Decimal('1'), id='unit price: single-digit integer with single trailing zero'),
    pytest.param('1 item at 01.0', 1, 'item', Decimal('1'), id='unit price: single-digit integer with single leading zero and single trailing zero'),
    pytest.param('1 item at 0001.0', 1, 'item', Decimal('1'), id='unit price: single-digit integer with multiple leading zeros and single trailing zero'),
    pytest.param('1 item at 1.000', 1, 'item', Decimal('1'), id='unit price: single-digit integer with multiple trailing zeros'),
    pytest.param('1 item at 1.1', 1, 'item', Decimal('1.1'), id='unit price: single-digit decimal with single decimal digit'),
    pytest.param('1 item at 1.0113', 1, 'item', Decimal('1.0113'), id='unit price: single-digit decimal with multiple decimal digits'),
    pytest.param('1 item at 1.10', 1, 'item', Decimal('1.1'), id='unit price: single-digit decimal with single decimal digit and single trailing zero'),
    pytest.param('1 item at 1.1000', 1, 'item', Decimal('1.1'), id='unit price: single-digit decimal with single decimal digit and multiple trailing zeros'),

    pytest.param('1 item at 311', 1, 'item', Decimal('311'), id='unit price: multiple-digits integer with no decimal part'),
    pytest.param('1 item at 311.', 1, 'item', Decimal('311'), id='unit price: multiple-digits integer with no trailing zero'),
    pytest.param('1 item at 311.0', 1, 'item', Decimal('311'), id='unit price: multiple-digits integer with single trailing zero'),
    pytest.param('1 item at 311.000', 1, 'item', Decimal('311'), id='unit price: multiple-digits integer with multiple trailing zeros'),
    pytest.param('1 item at 311.0113', 1, 'item', Decimal('311.0113'), id='unit price: multiple-digits decimal with multiple decimal digits'),
    pytest.param('1 item at 0311.0113', 1, 'item', Decimal('311.0113'), id='unit price: multiple-digits decimal with single leading zero and multiple decimal digits'),
    pytest.param('1 item at 000311.0113', 1, 'item', Decimal('311.0113'), id='unit price: multiple-digits decimal with multiple leading zeros and multiple decimal digits'),
])
def test_returns_parsed_item_from_matching_string(text, quantity, product_name, unit_price):
    expected = {'quantity': quantity, 'product_name': product_name, 'unit_price': unit_price}
    assert expected == parse_item(text)


@pytest.mark.parametrize('input', [
    pytest.param('', id='emtpy string'),
    pytest.param('-1 book at 12.49', id='negative quantity'),
    pytest.param('1.0 book at 12.49', id='non-integer quantity'),
    pytest.param('qty book at 12.49', id='non-number quantity'),
    pytest.param('item at 12.32', id='missing quantity'),
    pytest.param('1 at 12.32', id='missing product name'),
    pytest.param('1 item', id='missing unit price'),
    pytest.param('1 item at', id='missing unit price amount'),
    pytest.param('1 item 12.32', id='missing unit price intro tag'),
])
def test_raises_error_if_string_does_not_match(input):
    with pytest.raises(InvalidItemError):
        parse_item(input)
