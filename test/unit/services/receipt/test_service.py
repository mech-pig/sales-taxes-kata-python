from unittest.mock import Mock, sentinel

import pytest

from taxes.services.receipt.service import (
    create as create_receipt_service,
    Dependency as ReceiptServiceDependency,
    ReceiptService,
)
from taxes.services.receipt.entities.receipt import ItemToInsert
from receipt.use_cases.test_create_receipt import create_receipt_test_cases


@pytest.fixture
def make_dependencies_fixture():
    def build():
        return {
            'logger': Mock(spec=ReceiptServiceDependency.Logger),
            'basket_service': Mock(spec=ReceiptServiceDependency.BasketService),
            'tax_service': Mock(spec=ReceiptServiceDependency.TaxService),
        }
    return build


def test_create_returns_service(make_dependencies_fixture):
    service = create_receipt_service(**make_dependencies_fixture())
    assert isinstance(service, ReceiptService)


@create_receipt_test_cases
def test_create_receipt_returns_receipt(case, make_dependencies_fixture):
    service = create_receipt_service(**make_dependencies_fixture())
    service.basket_service.create_basket.side_effect = lambda a: a
    service.tax_service.add_taxes.return_value = [
        ItemToInsert(
            description=p.article_in_basket.product.name,
            quantity=p.article_in_basket.quantity,
            unit_price_before_taxes=p.article_in_basket.product.unit_price,
            taxes_to_apply=p.taxes_to_apply,
        ) for p in case.params
    ]

    articles = [p.article_in_basket for p in case.params]
    assert case.expected == service.create_receipt(articles=articles)
