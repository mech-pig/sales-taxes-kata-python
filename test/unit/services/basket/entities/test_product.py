import pytest

from taxes.services.basket.entities import product


@pytest.mark.parametrize('name', [
    pytest.param('', id='empty string'),
    pytest.param(' ', id='space'),
    pytest.param('\t', id='tab'),
    pytest.param('\n', id='newline'),
    pytest.param(None, id='none'),
    pytest.param(0, id='non string'),
])
def test_product_name_must_be_a_non_blank_string(name):
    error_cls = product.ProductError.InvalidName
    error_msg = f'invalid product name: {name}'
    with pytest.raises(error_cls, match=error_msg):
        product.create(name=name, category='dummy')
