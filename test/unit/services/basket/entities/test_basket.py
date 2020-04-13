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


def test_get_quantity_of_articles_not_in_basket_returns_zero():
    article_in_basket = create_article(
        product_name='dummy',
        product_unit_price=Decimal('1'),
        imported=True,
        quantity=1,
    )

    article_not_in_basket = create_article(
        product_name='dummy2',
        product_unit_price=Decimal('1'),
        imported=True,
        quantity=1,
    )

    basket_to_test = basket.Basket(
        articles={
            basket.BasketEntryKey(
                product_name=article_in_basket.product.name,
                unit_price=article_in_basket.product.unit_price,
                imported=article_in_basket.imported,
            ): article_in_basket,
        }
    )

    article_not_in_basket_key = basket.BasketEntryKey(
        product_name=article_not_in_basket.product.name,
        unit_price=article_not_in_basket.product.unit_price,
        imported=article_not_in_basket.imported,
    )
    assert article_not_in_basket_key not in basket_to_test.articles

    assert 0 == basket.get_quantity(article_not_in_basket_key, basket_to_test)


def test_get_quantity_of_product_in_basket_returns_quantity_of_that_product():
    quantity = 123
    article_in_basket = create_article(
        product_name='dummy',
        product_unit_price=Decimal('1'),
        imported=True,
        quantity=quantity,
    )
    article_basket_key = basket.BasketEntryKey(
        product_name=article_in_basket.product.name,
        unit_price=article_in_basket.product.unit_price,
        imported=article_in_basket.imported,
    )
    basket_to_test = basket.Basket(articles={article_basket_key: article_in_basket})

    assert quantity == basket.get_quantity(article_basket_key, basket_to_test)


def test_add_article_to_empty_basket_returns_basket_with_added_article():
    quantity = 2
    article_to_add = create_article(
        product_name='dummy',
        product_unit_price=Decimal('1'),
        imported=True,
        quantity=quantity,
    )
    article_basket_key = basket.BasketEntryKey(
        product_name=article_to_add.product.name,
        unit_price=article_to_add.product.unit_price,
        imported=article_to_add.imported,
    )

    initial_basket = basket.empty()
    expected_basket = basket.Basket(articles={article_basket_key: article_to_add})
    assert expected_basket == basket.add_article(article_to_add, initial_basket)


def test_add_article_with_article_already_in_basket_increases_quantity_of_that_article():
    initial_quantity = 2
    article_in_basket = create_article(
        product_name='dummy',
        product_unit_price=Decimal('1'),
        imported=True,
        quantity=initial_quantity,
    )

    added_quantity = 3
    article_to_add = create_article(
        product_name=article_in_basket.product.name,
        product_unit_price=article_in_basket.product.unit_price,
        imported=article_in_basket.imported,
        quantity=added_quantity,
    )

    expected_article = create_article(
        product_name=article_in_basket.product.name,
        product_unit_price=article_in_basket.product.unit_price,
        imported=article_in_basket.imported,
        quantity=initial_quantity + added_quantity,
    )
    article_basket_key = basket.BasketEntryKey(
        product_name=article_in_basket.product.name,
        unit_price=article_in_basket.product.unit_price,
        imported=article_in_basket.imported,
    )
    initial_basket = basket.Basket(articles={article_basket_key: article_in_basket})
    expected_basket = basket.Basket(articles={article_basket_key: expected_article})

    assert expected_basket == basket.add_article(article_to_add, initial_basket)


def test_add_article_doesnt_modify_quantity_of_other_articles_already_in_basket():
    article_in_basket_quantity = 2
    article_in_basket = create_article(
        product_name='dummy',
        product_unit_price=Decimal('1'),
        imported=True,
        quantity=article_in_basket_quantity,
    )
    article_in_basket_key = basket.BasketEntryKey(
        product_name=article_in_basket.product.name,
        unit_price=article_in_basket.product.unit_price,
        imported=article_in_basket.imported,
    )
    initial_basket = basket.Basket(articles={article_in_basket_key: article_in_basket})

    article_to_add = create_article(
        product_name='dummy2',
        product_unit_price=Decimal('1'),
        imported=True,
        quantity=32,
    )

    updated_basket = basket.add_article(article_to_add, initial_basket)
    assert article_in_basket_quantity == basket.get_quantity(article_in_basket_key, updated_basket)


def test_list_articles_returns_empty_list_if_basket_is_emtpy():
    empty_basket = basket.empty()
    assert [] == basket.list_articles(empty_basket)


def test_list_articles_returns_list_of_added_articles_sorted_by_insertion_order():
    articles_to_add = [
        create_article(quantity=1, product_name='B', product_unit_price=Decimal('1'), imported=True),
        create_article(quantity=1, product_name='A', product_unit_price=Decimal('1'), imported=True),
        create_article(quantity=1, product_name='B', product_unit_price=Decimal('1'), imported=True),
    ]
    expected = [
        create_article(quantity=2, product_name='B', product_unit_price=Decimal('1'), imported=True),
        create_article(quantity=1, product_name='A', product_unit_price=Decimal('1'), imported=True),
    ]

    basket_with_articles = basket.empty()
    for a in articles_to_add:
        basket_with_articles = basket.add_article(a, basket_with_articles)

    assert expected == basket.list_articles(basket_with_articles)
