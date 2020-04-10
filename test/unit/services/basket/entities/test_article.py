from decimal import Decimal

import pytest

from taxes.services.basket.entities import article, product


@pytest.fixture
def make_article_kwargs():
    def build(**overrides):
        return {
            'quantity': 12,
            'product_name': 'a-cool-product',
            'product_unit_price': Decimal('12.23'),
            **overrides,
        }
    return build


def test_create_returns_article(make_article_kwargs):
    kwargs = make_article_kwargs()
    expected = article.Article(
        product=product.Product(
            name=kwargs['product_name'],
            unit_price=kwargs['product_unit_price'],
        ),
        quantity=kwargs['quantity'],
    )
    assert expected == article.create(**kwargs)


@pytest.mark.parametrize('quantity', [
    pytest.param(0, id='quantity = 0'),
    pytest.param(-12, id='quantity < 0'),
])
def test_article_quantity_cannot_be_non_positive(make_article_kwargs, quantity):
    kwargs = make_article_kwargs(quantity=quantity)
    error_cls = article.ArticleError.NonPositiveQuantity
    error_msg = f'quantity must be positive: {quantity}'
    with pytest.raises(error_cls, match=error_msg):
        article.create(**kwargs)
