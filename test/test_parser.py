import pytest

from taxes.item import Item, InvalidItemError
from taxes.parser import parse_item


@pytest.mark.parametrize('input, expected', [
    pytest.param('1 book at 12.49', Item(quantity=1), id='quantity = 1'),
    pytest.param('2 book at 12.49', Item(quantity=2), id='quantity > 1'),
    pytest.param('99 book at 12.49', Item(quantity=99), id='quantity > 9'),
    pytest.param('10000000 book at 12.49', Item(quantity=10000000), id='a very big quantity'),
])
def test_returns_parsed_item_from_matching_string(input, expected):
    assert expected == parse_item(input)


@pytest.mark.parametrize('input', [
    pytest.param('', id='emtpy string'),
    pytest.param('-1 book at 12.49', id='negative quantity'),
    pytest.param('1.0 book at 12.49', id='non-integer quantity'),
    pytest.param('qty book at 12.49', id='non-number quantity'),
])
def test_raises_error_if_string_does_not_match(input):
    with pytest.raises(InvalidItemError):
        parse_item(input)
