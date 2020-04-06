from decimal import Decimal

import pytest

from taxes.services.receipt.entities import product


@pytest.fixture
def make_product_kwargs():
    def build(**overrides):
        return {
            'name': 'test-product',
            'unit_price': Decimal('1.42'),
            **overrides
        }
    return build


def test_create_returns_a_product(make_product_kwargs):
    actual = product.create(**make_product_kwargs())
    assert isinstance(actual, product.Product)


def test_two_products_are_equal_if_all_attributes_are_equal(make_product_kwargs):
    kwargs = make_product_kwargs()
    product_one = product.create(**kwargs)
    product_two = product.create(**kwargs)
    assert product_one is not product_two
    assert product_one == product_two


@pytest.mark.parametrize('case', [
    pytest.param(
        {
            'attr': 'name',
            'value': 'one',
            'other_value': 'two',
        },
        id='name',
    ),
    pytest.param(
        {
            'attr': 'unit_price',
            'value': Decimal('1'),
            'other_value': Decimal('1.1'),
        },
        id='unit_price',
    ),
])
def test_two_products_are_not_equal_if_they_different_attribute_values(case, make_product_kwargs):
    product_one = product.create(**make_product_kwargs(**{case['attr']: case['value']}))
    product_two = product.create(**make_product_kwargs(**{case['attr']: case['other_value']}))
    assert product_one != product_two


def test_product_unit_price_cant_be_negative(make_product_kwargs):
    unit_price = Decimal('-1')
    expected_error_cls = product.ProductError.NegativeUnitPrice
    expected_error_msg = f'unit_price can\'t be negative: {unit_price}'
    with pytest.raises(expected_error_cls, match=expected_error_msg):
        product.create(**make_product_kwargs(unit_price=unit_price))


def test_product_can_have_unit_price_equal_to_zero(make_product_kwargs):
    unit_price = 0
    created = product.create(**make_product_kwargs(unit_price=unit_price))
    assert unit_price == created.unit_price
