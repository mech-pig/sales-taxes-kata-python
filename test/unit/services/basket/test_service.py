from unittest.mock import Mock, sentinel

import pytest

from taxes.services import basket
from basket.use_cases.test_create_basket import create_basket_test_cases


@pytest.fixture
def make_dependencies_fixture():
    def build():
        return {
            'logger': Mock(spec=basket.Dependency.Logger),
        }
    return build


def test_create_returns_service(make_dependencies_fixture):
    service = basket.create(**make_dependencies_fixture())
    assert isinstance(service, basket.BasketService)


@create_basket_test_cases
def test_create_basket_returns_basket(case, make_dependencies_fixture):
    service = basket.create(**make_dependencies_fixture())
    assert case.expected == service.create_basket(articles=case.articles)
