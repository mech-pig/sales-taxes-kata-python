from unittest.mock import Mock, sentinel

import pytest

from taxes.services.receipt.service import (
    create as create_receipt_service,
    Dependency as ReceiptServiceDependency,
    ReceiptService,
)
from taxes.services.receipt.entities.taxed_article import TaxedArticle
from receipt.use_cases.test_create_receipt import create_receipt_test_cases


@pytest.fixture
def make_dependencies_fixture():
    def build():
        return {
            'logger': Mock(spec=ReceiptServiceDependency.Logger),
            'tax_service': Mock(spec=ReceiptServiceDependency.TaxService),
        }
    return build


def test_create_returns_service(make_dependencies_fixture):
    service = create_receipt_service(**make_dependencies_fixture())
    assert isinstance(service, ReceiptService)


@create_receipt_test_cases
def test_create_receipt_returns_receipt(case, make_dependencies_fixture):
    service = create_receipt_service(**make_dependencies_fixture())
    service.tax_service.add_taxes.return_value = [
        TaxedArticle(
            product=i.article.product,
            quantity=i.article.quantity,
            imported=i.article.imported,
            unit_price_before_taxes=i.article.unit_price_before_taxes,
            tax_amount_due_per_unit=i.tax_amount_due_per_unit,
        ) for i in case.input
    ]

    articles = [i.article for i in case.input]
    assert case.expected == service.create_receipt(articles=articles)
