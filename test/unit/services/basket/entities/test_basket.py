from decimal import Decimal

import pytest

from taxes.services.basket.entities import article, basket, product


def test_empty_returns_basket_without_articles():
    empty_basket = basket.empty()
    assert {} == empty_basket.articles


def test_get_quantity_of_product_not_in_basket_returns_zero():
    basket_to_test = basket.Basket(
        articles={
            product.Product(name='dummy', unit_price=Decimal('1')): 1,
        }
    )
    not_in_basket = product.Product(name='not-in-basket', unit_price=Decimal('1'))
    assert not_in_basket not in basket_to_test.articles

    assert 0 == basket.get_quantity(not_in_basket, basket_to_test)


def test_get_quantity_of_product_in_basket_returns_quantity_of_that_product():
    product_in_basket = product.Product(name='dummy', unit_price=Decimal('1'))
    quantity = 123
    basket_to_test = basket.Basket(articles={product_in_basket: quantity})

    assert quantity == basket.get_quantity(product_in_basket, basket_to_test)


def test_add_article_to_empty_basket_returns_basket_with_added_article():
    quantity = 1
    product_to_add = product.Product(name='dummy', unit_price=Decimal('1'))
    article_to_add = article.Article(product=product_to_add, quantity=quantity)

    initial_basket = basket.empty()
    expected_basket = basket.Basket(articles={product_to_add: quantity})
    assert expected_basket == basket.add_article(article_to_add, initial_basket)


def test_add_article_of_product_already_in_basket_increases_quantity_of_that_product():
    product_in_basket = product.Product(name='dummy', unit_price=Decimal('1'))
    initial_quantity = 2
    initial_basket = basket.Basket(articles={product_in_basket: initial_quantity})

    added_quantity = 3
    article_to_add = article.Article(product=product_in_basket, quantity=added_quantity)
    expected_basket = basket.Basket(articles={product_in_basket: initial_quantity + added_quantity})

    assert expected_basket == basket.add_article(article_to_add, initial_basket)


def test_add_article_doesnt_modify_quantity_of_different_products_already_in_basket():
    product_in_basket = product.Product(name='dummy', unit_price=Decimal('1'))
    product_in_basket_quantity = 2
    initial_basket = basket.Basket(articles={product_in_basket: product_in_basket_quantity})

    new_product = product.Product(name='new', unit_price=Decimal('1'))
    assert new_product != product_in_basket

    article_to_add = article.Article(product=new_product, quantity=1)
    updated_basket = basket.add_article(article_to_add, initial_basket)
    assert product_in_basket_quantity == basket.get_quantity(product_in_basket, updated_basket)


def test_list_articles_returns_empty_list_if_basket_is_emtpy():
    empty_basket = basket.empty()
    assert [] == basket.list_articles(empty_basket)


def test_list_articles_returns_list_of_added_articles_sorted_by_insertion_order():
    articles_to_add = [
        article.create(quantity=1, product_name='B', product_unit_price=Decimal('1')),
        article.create(quantity=1, product_name='A', product_unit_price=Decimal('1')),
        article.create(quantity=1, product_name='B', product_unit_price=Decimal('1'))
    ]
    expected = [
        article.create(quantity=2, product_name='B', product_unit_price=Decimal('1')),
        article.create(quantity=1, product_name='A', product_unit_price=Decimal('1'))
    ]

    basket_with_articles = basket.empty()
    for a in articles_to_add:
        basket_with_articles = basket.add_article(a, basket_with_articles)

    assert expected == basket.list_articles(basket_with_articles)
