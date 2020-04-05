from decimal import Decimal

import pytest

from taxes.services.receipt.entities import article, basket


def test_empty_returns_basket_without_articles():
    empty_basket = basket.empty()
    assert {} == empty_basket.articles


def test_get_quantity_of_product_not_in_basket_returns_zero():
    basket_to_test = basket.Basket(
        articles={
            basket.Product(name='dummy', unit_price=Decimal('1')): 1,
        }
    )
    not_in_basket = basket.Product(name='not-in-basket', unit_price=Decimal('1'))
    assert not_in_basket not in basket_to_test.articles

    assert 0 == basket.get_quantity(not_in_basket, basket_to_test)


def test_get_quantity_of_product_in_basket_returns_quantity_of_that_product():
    product = basket.Product(name='dummy', unit_price=Decimal('1'))
    quantity = 123
    basket_to_test = basket.Basket(articles={product: quantity})

    assert quantity == basket.get_quantity(product, basket_to_test)


def test_add_article_to_empty_basket_returns_basket_with_added_article():
    product = basket.Product(name='dummy', unit_price=Decimal('1'))
    initial_basket = basket.empty()

    quantity = 1
    article_to_add = article.Article(
        product_name=product.name,
        unit_price=product.unit_price,
        quantity=quantity,
    )

    expected_basket = basket.Basket(articles={product: quantity})
    assert expected_basket == basket.add_article(article_to_add, initial_basket)


def test_add_article_of_product_already_in_basket_increases_quantity_of_that_product():
    product = basket.Product(name='dummy', unit_price=Decimal('1'))
    initial_quantity = 2
    initial_basket = basket.Basket(articles={product: initial_quantity})

    added_quantity = 3
    article_to_add = article.Article(
        product_name=product.name,
        unit_price=product.unit_price,
        quantity=added_quantity,
    )
    expected_basket = basket.Basket(articles={product: initial_quantity + added_quantity})
    assert expected_basket == basket.add_article(article_to_add, initial_basket)


def test_add_article_doesnt_modify_quantity_of_different_products_already_in_basket():
    product_in_basket = basket.Product(name='dummy', unit_price=Decimal('1'))
    product_in_basket_quantity = 2
    initial_basket = basket.Basket(articles={product_in_basket: product_in_basket_quantity})

    new_product = basket.Product(name='new', unit_price=Decimal('1'))
    assert new_product != product_in_basket

    article_to_add = article.Article(
        product_name=new_product.name,
        unit_price=new_product.unit_price,
        quantity=1,
    )
    updated_basket = basket.add_article(article_to_add, initial_basket)
    assert product_in_basket_quantity == basket.get_quantity(product_in_basket, updated_basket)
