from decimal import Decimal

import pytest

from taxes import item


@pytest.fixture
def item_kwargs_fixture():
    def build(**overrides):
        return {
            'quantity': 12,
            'product_name': 'a-cool-product',
            'unit_price': Decimal('12.23'),
            **overrides,
        }
    return build


def test_create_returns_item(item_kwargs_fixture):
    kwargs = item_kwargs_fixture()
    expected = item.Item(
        quantity=kwargs['quantity'],
        product_name=kwargs['product_name'],
        unit_price=kwargs['unit_price'],
    )
    assert expected == item.create(**kwargs)


@pytest.mark.parametrize('quantity', [
    pytest.param(0, id='quantity = 0'),
    pytest.param(-12, id='quantity < 0'),
])
def test_item_quantity_cannot_be_non_positive(item_kwargs_fixture, quantity):
    kwargs = item_kwargs_fixture(quantity=quantity)
    error_cls = item.ItemError.NonPositiveQuantity
    error_msg = f'quantity must be positive: {quantity}'
    with pytest.raises(error_cls, match=error_msg):
        item.create(**kwargs)


def test_item_unit_price_cannot_be_negative(item_kwargs_fixture):
    unit_price = Decimal('-1')
    kwargs = item_kwargs_fixture(unit_price=unit_price)
    error_cls = item.ItemError.NegativeUnitPrice
    error_msg = f'unit_price can\'t be negative: {unit_price}'
    with pytest.raises(error_cls, match=error_msg):
        item.create(**kwargs)


def test_item_can_have_unit_price_equal_to_zero(item_kwargs_fixture):
    unit_price = 0
    kwargs = item_kwargs_fixture(unit_price=unit_price)
    assert unit_price == item.create(**kwargs).unit_price
