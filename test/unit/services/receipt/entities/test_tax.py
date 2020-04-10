from decimal import Decimal

import pytest

from taxes.services.receipt.entities import tax


@pytest.fixture
def make_tax_kwargs():
    def build(**overrides):
        return {
            'rate': Decimal('0.05'),
            'id': 'a-not-so-cool-tax',
            **overrides,
        }
    return build


def test_create_returns_tax():
    rate = Decimal('0.01')
    id = 'a-test-tax'
    expected = tax.Tax(id=id, rate=rate)
    assert expected == tax.create(id=id, rate=rate)


@pytest.mark.parametrize('rate', [
    pytest.param(0, id='rate = 0'),
    pytest.param(-12, id='rate < 0'),
])
def test_create_raises_error_if_tax_is_not_positive(make_tax_kwargs, rate):
    kwargs = make_tax_kwargs(rate=rate)
    expected_error_cls = tax.TaxError.NonPositiveRate
    expected_error_msg = f'rate must be positive: {rate}'
    with pytest.raises(expected_error_cls, match=expected_error_msg):
        tax.create(**kwargs)


@pytest.mark.parametrize('case', [
    pytest.param(
        {
            'price': Decimal('0'),
            'rate': Decimal('0.05'),
            'expected': Decimal('0'),
        },
        id='price = 0 results in amount = 0',
    ),
    pytest.param(
        {
            'price': Decimal('10'),
            'rate': Decimal('0.1'),
            'expected': Decimal('1'),
        },
        id='amount = price * rate (integer amount)',
    ),
    pytest.param(
        {
            'price': Decimal('10'),
            'rate': Decimal('0.025'),
            'expected': Decimal('0.25'),
        },
        id='amount = price * rate (decimal amount)',
    ),
    pytest.param(
        {
            'price': Decimal('1.0251'),
            'rate': Decimal('1'),
            'expected': Decimal('1.05'),
        },
        id='amount rounded up to nearest 0.05 (half up)',
    ),
    pytest.param(
        {
            'price': Decimal('1.025'),
            'rate': Decimal('1'),
            'expected': Decimal('1.05'),
        },
        id='amount rounded up to nearest 0.05 (half up with tie)',
    ),
    pytest.param(
        {
            'price': Decimal('1.0249'),
            'rate': Decimal('1'),
            'expected': Decimal('1'),
        },
        id='amount rounded up to nearest 0.05 (down)',
    ),
    pytest.param(
        {
            'price': Decimal('1.05'),
            'rate': Decimal('1'),
            'expected': Decimal('1.05'),
        },
        id='amount rounded up to nearest 0.05 (equal to precision)',
    ),
])
def test_calculate_tax_amount_returns_amount_due_to_tax(case, make_tax_kwargs):
    test_tax = tax.create(**make_tax_kwargs(rate=case['rate']))
    price = case['price']
    expected = case['expected']
    assert expected == tax.calculate_tax_amount(price=price, tax=test_tax)


@pytest.mark.parametrize('case', [
    pytest.param(
        {
            'rates': [],
            'price': Decimal('1'),
            'expected': Decimal('1'),
        },
        id='no taxes to apply',
    ),
    pytest.param(
        {
            'rates': [Decimal('1'), Decimal('1')],
            'price': Decimal('0'),
            'expected': Decimal('0'),
        },
        id='price is equal to 0',
    ),
    pytest.param(
        {
            'rates': [Decimal('0.05')],
            'price': Decimal('2'),
            'expected': Decimal('2') + Decimal('0.1'),
        },
        id='single tax',
    ),
    pytest.param(
        {
            'rates': [Decimal('1')],
            'price': Decimal('1.0249'),
            'expected': Decimal('1.0249') + Decimal('1'),
        },
        id='single tax with rounding (down)',
    ),
    pytest.param(
        {
            'rates': [Decimal('1')],
            'price': Decimal('1.025'),
            'expected': Decimal('1.025') + Decimal('1.05'),
        },
        id='single tax with rounding (up)',
    ),
    pytest.param(
        {
            'rates': [Decimal('0.05'), Decimal('0.1')],
            'price': Decimal('2'),
            'expected': Decimal('2') + Decimal('0.1') + Decimal('0.2'),
        },
        id='multiple taxes',
    ),
])
def test_apply_returns_amount_due_to_application_of_taxes_to_price(case, make_tax_kwargs):
    taxes = [tax.create(**make_tax_kwargs(rate=rate)) for rate in case['rates']]
    price = case['price']
    expected = case['expected']
    assert expected == tax.apply(price=price, taxes=taxes)
