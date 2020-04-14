from unittest.mock import Mock, sentinel

import pytest

from taxes.services.basket.service import (
    BasketService,
    create as create_basket_service,
    Dependency as BasketServiceDependency,
)
from basket.use_cases.test_create_basket import create_basket_test_cases


@pytest.fixture
def make_dependencies_fixture():
    def build():
        return {
            'logger': Mock(spec=BasketServiceDependency.Logger),
            'product_repository': Mock(spec=BasketServiceDependency.ProductRepository),
        }
    return build


def test_create_returns_service(make_dependencies_fixture):
    service = create_basket_service(**make_dependencies_fixture())
    assert isinstance(service, BasketService)


@create_basket_test_cases
def test_create_basket_returns_basket(case, make_dependencies_fixture):
    products = {product.name: product for product in case.input.products}

    def get_product_by_name(name):
        return products[name]

    service = create_basket_service(**make_dependencies_fixture())
    service.product_repository.get_by_name.side_effect = get_product_by_name

    assert case.expected == service.create_basket(purchased_items=case.input.purchased_items)
