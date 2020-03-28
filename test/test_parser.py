import pytest

from taxes.item import Item, InvalidItemError
from taxes.parser import parse_item


@pytest.mark.parametrize('input, expected', [
    pytest.param('1 book at 12.49', Item(quantity=1, product_name='book'), id='quantity: = 1'),
    pytest.param('2 book at 12.49', Item(quantity=2, product_name='book'), id='quantity: > 1'),
    pytest.param('99 book at 12.49', Item(quantity=99, product_name='book'), id='quantity: > 9'),
    pytest.param('10000000 book at 12.49', Item(quantity=10000000, product_name='book'), id='quantity: a very big number'),
    pytest.param('1 item at 12.39', Item(quantity=1, product_name='item'), id='product name: ascii lowercase word'),
    pytest.param('1 ITEM at 12.39', Item(quantity=1, product_name='item'), id='product name: ascii uppercase word'),
    pytest.param('1 ItEm at 12.39', Item(quantity=1, product_name='item'), id='product name: ascii mixed-case word'),
    pytest.param('1 1-t_e.m! at 12.39', Item(quantity=1, product_name='1-t_e.m!'), id='product name: ascii string with symbols'),
    pytest.param('1 👍👍👍 at 12.39', Item(quantity=1, product_name='👍👍👍'), id='product name: unicode word'),
    pytest.param('1 this is an item at 12.39', Item(quantity=1, product_name='this is an item'), id='product name: ascii string with spaces'),
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
])
def test_raises_error_if_string_does_not_match(input):
    with pytest.raises(InvalidItemError):
        parse_item(input)
