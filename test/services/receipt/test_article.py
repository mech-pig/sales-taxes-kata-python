from decimal import Decimal

import pytest

from taxes.services.receipt.entities import article


@pytest.fixture
def article_kwargs_fixture():
    def build(**overrides):
        return {
            'quantity': 12,
            'product_name': 'a-cool-product',
            'unit_price': Decimal('12.23'),
            **overrides,
        }
    return build


def test_create_returns_article(article_kwargs_fixture):
    kwargs = article_kwargs_fixture()
    expected = article.Article(
        quantity=kwargs['quantity'],
        product_name=kwargs['product_name'],
        unit_price=kwargs['unit_price'],
    )
    assert expected == article.create(**kwargs)


@pytest.mark.parametrize('quantity', [
    pytest.param(0, id='quantity = 0'),
    pytest.param(-12, id='quantity < 0'),
])
def test_article_quantity_cannot_be_non_positive(article_kwargs_fixture, quantity):
    kwargs = article_kwargs_fixture(quantity=quantity)
    error_cls = article.ArticleError.NonPositiveQuantity
    error_msg = f'quantity must be positive: {quantity}'
    with pytest.raises(error_cls, match=error_msg):
        article.create(**kwargs)


def test_article_unit_price_cannot_be_negative(article_kwargs_fixture):
    unit_price = Decimal('-1')
    kwargs = article_kwargs_fixture(unit_price=unit_price)
    error_cls = article.ArticleError.NegativeUnitPrice
    error_msg = f'unit_price can\'t be negative: {unit_price}'
    with pytest.raises(error_cls, match=error_msg):
        article.create(**kwargs)


def test_article_can_have_unit_price_equal_to_zero(article_kwargs_fixture):
    unit_price = 0
    kwargs = article_kwargs_fixture(unit_price=unit_price)
    assert unit_price == article.create(**kwargs).unit_price
