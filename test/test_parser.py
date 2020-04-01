from decimal import Decimal

import pytest

from taxes.item import Item, InvalidItemError
from taxes.parser import parse_item


@pytest.mark.parametrize('input, expected', [
    # quantity
    pytest.param('1 book at 12.49', Item(quantity=1, product_name='book', unit_price=Decimal('12.49')), id='quantity: = 1'),
    pytest.param('2 book at 12.49', Item(quantity=2, product_name='book', unit_price=Decimal('12.49')), id='quantity: > 1'),
    pytest.param('99 book at 12.49', Item(quantity=99, product_name='book', unit_price=Decimal('12.49')), id='quantity: > 9'),
    pytest.param('10000000 book at 12.49', Item(quantity=10000000, product_name='book', unit_price=Decimal('12.49')), id='quantity: a very big number'),

    # name
    pytest.param('1 item at 12.39', Item(quantity=1, product_name='item', unit_price=Decimal('12.39')), id='product name: ascii lowercase word'),
    pytest.param('1 ITEM at 12.39', Item(quantity=1, product_name='item', unit_price=Decimal('12.39')), id='product name: ascii uppercase word'),
    pytest.param('1 ItEm at 12.39', Item(quantity=1, product_name='item', unit_price=Decimal('12.39')), id='product name: ascii mixed-case word'),
    pytest.param('1 1-t_e.m! at 12.39', Item(quantity=1, product_name='1-t_e.m!', unit_price=Decimal('12.39')), id='product name: ascii string with symbols'),
    pytest.param('1 👍👍👍 at 12.39', Item(quantity=1, product_name='👍👍👍', unit_price=Decimal('12.39')), id='product name: unicode word'),
    pytest.param('1 this is an item at 12.39', Item(quantity=1, product_name='this is an item', unit_price=Decimal('12.39')), id='product name: ascii string with spaces'),

    # unit price
    pytest.param('1 item at 0', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with no decimal part'),
    pytest.param('1 item at 00', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with single leading zero'),
    pytest.param('1 item at 000', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with multiple leading zeros'),
    pytest.param('1 item at 0.', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with no trailing zeros'),
    pytest.param('1 item at 00.', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with single leading zero and no trailing zeros'),
    pytest.param('1 item at 000.', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with multiple leading zeros and no trailing zeros'),
    pytest.param('1 item at 0.0', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with single trailing zero'),
    pytest.param('1 item at 00.0', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with single leading zero and single trailing zero'),
    pytest.param('1 item at 000.0', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with multiple leading zeros and single trailing zero'),
    pytest.param('1 item at 0.000', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with multiple trailing zeros'),
    pytest.param('1 item at 00.000', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with single leading zero and multiple trailing zeros'),
    pytest.param('1 item at 000.000', Item(quantity=1, product_name='item', unit_price=Decimal('0')), id='unit price: zero with multiple leading zeros and multiple trailing zeros'),

    pytest.param('1 item at 0.1', Item(quantity=1, product_name='item', unit_price=Decimal('0.1')), id='unit price: single-digit decimal (< 1) with single decimal digit'),
    pytest.param('1 item at 0.0113', Item(quantity=1, product_name='item', unit_price=Decimal('0.0113')), id='unit price: single-digit decimal (< 1) with multiple decimal digits'),
    pytest.param('1 item at 0.10', Item(quantity=1, product_name='item', unit_price=Decimal('0.1')), id='unit price: single-digit decimal (< 1) with single decimal digit and single trailing zero'),
    pytest.param('1 item at 0.1000', Item(quantity=1, product_name='item', unit_price=Decimal('0.1')), id='unit price: single-digit decimal (< 1) with single decimal digit and multiple trailing zeros'),
    pytest.param('1 item at 00.1', Item(quantity=1, product_name='item', unit_price=Decimal('0.1')), id='unit price: single-digit decimal (< 1) with single leading zero and single decimal digit'),
    pytest.param('1 item at 00.0113', Item(quantity=1, product_name='item', unit_price=Decimal('0.0113')), id='unit price: single-digit decimal (< 1) with single leading zero and multiple decimal digits'),
    pytest.param('1 item at 00.10', Item(quantity=1, product_name='item', unit_price=Decimal('0.1')), id='unit price: single-digit decimal (< 1) with single leading zero and single decimal digit and single trailing zero'),
    pytest.param('1 item at 00.1000', Item(quantity=1, product_name='item', unit_price=Decimal('0.1')), id='unit price: single-digit decimal (< 1) with single leading zero and single decimal digit and multiple trailing zeros'),

    pytest.param('1 item at 1', Item(quantity=1, product_name='item', unit_price=Decimal('1')), id='unit price: single-digit integer with no decimal part'),
    pytest.param('1 item at 1.', Item(quantity=1, product_name='item', unit_price=Decimal('1')), id='unit price: single-digit integer with no trailing zero'),
    pytest.param('1 item at 1.0', Item(quantity=1, product_name='item', unit_price=Decimal('1')), id='unit price: single-digit integer with single trailing zero'),
    pytest.param('1 item at 01.0', Item(quantity=1, product_name='item', unit_price=Decimal('1')), id='unit price: single-digit integer with single leading zero and single trailing zero'),
    pytest.param('1 item at 0001.0', Item(quantity=1, product_name='item', unit_price=Decimal('1')), id='unit price: single-digit integer with multiple leading zeros and single trailing zero'),
    pytest.param('1 item at 1.000', Item(quantity=1, product_name='item', unit_price=Decimal('1')), id='unit price: single-digit integer with multiple trailing zeros'),
    pytest.param('1 item at 1.1', Item(quantity=1, product_name='item', unit_price=Decimal('1.1')), id='unit price: single-digit decimal with single decimal digit'),
    pytest.param('1 item at 1.0113', Item(quantity=1, product_name='item', unit_price=Decimal('1.0113')), id='unit price: single-digit decimal with multiple decimal digits'),
    pytest.param('1 item at 1.10', Item(quantity=1, product_name='item', unit_price=Decimal('1.1')), id='unit price: single-digit decimal with single decimal digit and single trailing zero'),
    pytest.param('1 item at 1.1000', Item(quantity=1, product_name='item', unit_price=Decimal('1.1')), id='unit price: single-digit decimal with single decimal digit and multiple trailing zeros'),

    pytest.param('1 item at 311', Item(quantity=1, product_name='item', unit_price=Decimal('311')), id='unit price: multiple-digits integer with no decimal part'),
    pytest.param('1 item at 311.', Item(quantity=1, product_name='item', unit_price=Decimal('311')), id='unit price: multiple-digits integer with no trailing zero'),
    pytest.param('1 item at 311.0', Item(quantity=1, product_name='item', unit_price=Decimal('311')), id='unit price: multiple-digits integer with single trailing zero'),
    pytest.param('1 item at 311.000', Item(quantity=1, product_name='item', unit_price=Decimal('311')), id='unit price: multiple-digits integer with multiple trailing zeros'),
    pytest.param('1 item at 311.0113', Item(quantity=1, product_name='item', unit_price=Decimal('311.0113')), id='unit price: multiple-digits decimal with multiple decimal digits'),
    pytest.param('1 item at 0311.0113', Item(quantity=1, product_name='item', unit_price=Decimal('311.0113')), id='unit price: multiple-digits decimal with single leading zero and multiple decimal digits'),
    pytest.param('1 item at 000311.0113', Item(quantity=1, product_name='item', unit_price=Decimal('311.0113')), id='unit price: multiple-digits decimal with multiple leading zeros and multiple decimal digits'),

])
def test_returns_parsed_item_from_matching_string(input, expected):
    assert expected == parse_item(input)


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
