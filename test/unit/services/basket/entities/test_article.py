from decimal import Decimal

import pytest

from taxes.services.basket.entities import article, product


@pytest.fixture
def make_article_kwargs():
    def build(**overrides):
        return {
            'quantity': 12,
            'product_name': 'a-cool-product',
            'product_category': 'test-product-category',
            'unit_price_before_taxes': Decimal('12.23'),
            'imported': False,
            **overrides,
        }
    return build


def test_create_returns_article(make_article_kwargs):
    kwargs = make_article_kwargs()
    expected = article.Article(
        product=product.Product(
            name=kwargs['product_name'],
            category=kwargs['product_category'],
        ),
        unit_price_before_taxes=kwargs['unit_price_before_taxes'],
        quantity=kwargs['quantity'],
        imported=kwargs['imported'],
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


def test_article_unit_price_before_taxes_cant_be_negative(make_article_kwargs):
    unit_price_before_taxes = Decimal('-1')
    expected_error_cls = article.ArticleError.NegativeUnitPrice
    expected_error_msg = f'unit_price_before_taxes can\'t be negative: {unit_price_before_taxes}'
    with pytest.raises(expected_error_cls, match=expected_error_msg):
        article.create(**make_article_kwargs(unit_price_before_taxes=unit_price_before_taxes))


def test_article_unit_price_before_taxes_can_be_zero(make_article_kwargs):
    unit_price_before_taxes = Decimal('0')
    created = article.create(
        **make_article_kwargs(unit_price_before_taxes=unit_price_before_taxes),
    )
    assert unit_price_before_taxes == created.unit_price_before_taxes
