from decimal import Decimal

import pytest

from taxes.services.basket.entities import basket, product
from taxes.services.basket.entities.article import (
    Article,
    create as create_article,
)


def test_empty_returns_basket_without_articles():
    empty_basket = basket.empty()
    assert {} == empty_basket.articles


@pytest.fixture
def make_article_fixture():
    def build(**overrides):
        return create_article(**{
            'product_name': 'dummy',
            'product_category': 'dummy-category',
            'unit_price_before_taxes': Decimal('1'),
            'imported': True,
            'quantity': 1,
            **overrides
        })
    return build


def test_get_quantity_of_articles_not_in_basket_returns_zero(make_article_fixture):
    article_in_basket = make_article_fixture(product_name='dummy')
    article_not_in_basket = make_article_fixture(product_name='dummy2')

    basket_to_test = basket.Basket(
        articles={
            basket.BasketEntryKey(
                product_name=article_in_basket.product.name,
                unit_price=article_in_basket.unit_price_before_taxes,
                imported=article_in_basket.imported,
            ): article_in_basket,
        }
    )

    article_not_in_basket_key = basket.BasketEntryKey(
        product_name=article_not_in_basket.product.name,
        unit_price=article_not_in_basket.unit_price_before_taxes,
        imported=article_not_in_basket.imported,
    )
    assert article_not_in_basket_key not in basket_to_test.articles

    assert 0 == basket.get_quantity(article_not_in_basket_key, basket_to_test)


def test_get_quantity_of_product_in_basket_returns_quantity_of_that_product(make_article_fixture):
    quantity = 123
    article_in_basket = make_article_fixture(quantity=quantity)
    article_basket_key = basket.BasketEntryKey(
        product_name=article_in_basket.product.name,
        unit_price=article_in_basket.unit_price_before_taxes,
        imported=article_in_basket.imported,
    )
    basket_to_test = basket.Basket(articles={article_basket_key: article_in_basket})

    assert quantity == basket.get_quantity(article_basket_key, basket_to_test)


def test_add_article_to_empty_basket_returns_basket_with_added_article(make_article_fixture):
    quantity = 2
    article_to_add = make_article_fixture(quantity=quantity)
    article_basket_key = basket.BasketEntryKey(
        product_name=article_to_add.product.name,
        unit_price=article_to_add.unit_price_before_taxes,
        imported=article_to_add.imported,
    )

    initial_basket = basket.empty()
    expected_basket = basket.Basket(articles={article_basket_key: article_to_add})
    assert expected_basket == basket.add_article(article_to_add, initial_basket)


def test_add_article_with_article_already_in_basket_increases_quantity_of_that_article(make_article_fixture):
    initial_quantity = 2
    added_quantity = 3

    article_in_basket = make_article_fixture(quantity=initial_quantity)
    article_to_add = make_article_fixture(quantity=added_quantity)
    expected_article = make_article_fixture(quantity=initial_quantity + added_quantity)

    article_basket_key = basket.BasketEntryKey(
        product_name=article_in_basket.product.name,
        unit_price=article_in_basket.unit_price_before_taxes,
        imported=article_in_basket.imported,
    )
    initial_basket = basket.Basket(articles={article_basket_key: article_in_basket})
    expected_basket = basket.Basket(articles={article_basket_key: expected_article})

    assert expected_basket == basket.add_article(article_to_add, initial_basket)


def test_add_article_doesnt_modify_quantity_of_other_articles_already_in_basket(make_article_fixture):
    article_in_basket_quantity = 2
    article_in_basket = make_article_fixture(
        product_name='dummy',
        quantity=article_in_basket_quantity,
    )
    article_in_basket_key = basket.BasketEntryKey(
        product_name=article_in_basket.product.name,
        unit_price=article_in_basket.unit_price_before_taxes,
        imported=article_in_basket.imported,
    )
    initial_basket = basket.Basket(articles={article_in_basket_key: article_in_basket})

    article_to_add = make_article_fixture(
        product_name='dummy2',
        quantity=32,
    )

    updated_basket = basket.add_article(article_to_add, initial_basket)
    assert article_in_basket_quantity == basket.get_quantity(article_in_basket_key, updated_basket)


def test_list_articles_returns_empty_list_if_basket_is_emtpy(make_article_fixture):
    empty_basket = basket.empty()
    assert [] == basket.list_articles(empty_basket)


def test_list_articles_returns_list_of_added_articles_sorted_by_insertion_order():
    articles_to_add = [
        create_article(quantity=1, product_name='B', product_category='dummy', unit_price_before_taxes=Decimal('1'), imported=True),
        create_article(quantity=1, product_name='A', product_category='dummy', unit_price_before_taxes=Decimal('1'), imported=True),
        create_article(quantity=1, product_name='B', product_category='dummy', unit_price_before_taxes=Decimal('1'), imported=True),
    ]
    expected = [
        create_article(quantity=2, product_name='B', product_category='dummy', unit_price_before_taxes=Decimal('1'), imported=True),
        create_article(quantity=1, product_name='A', product_category='dummy', unit_price_before_taxes=Decimal('1'), imported=True),
    ]

    basket_with_articles = basket.empty()
    for a in articles_to_add:
        basket_with_articles = basket.add_article(a, basket_with_articles)

    assert expected == basket.list_articles(basket_with_articles)
