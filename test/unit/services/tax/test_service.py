from unittest.mock import Mock, sentinel

import pytest

from taxes.services.tax.service import (
    create as create_tax_service,
    Dependency as TaxServiceDependency,
    TaxService,
)
from tax.use_cases.test_add_taxes import add_taxes_test_cases


@pytest.fixture
def make_dependencies_fixture():
    def build():
        return {
            'logger': Mock(spec=TaxServiceDependency.Logger),
        }
    return build


def test_create_returns_service(make_dependencies_fixture):
    service = create_tax_service(**make_dependencies_fixture())
    assert isinstance(service, TaxService)


@add_taxes_test_cases
def test_add_taxes_returns_taxed_items(case, make_dependencies_fixture):
    service = create_tax_service(**make_dependencies_fixture())
    assert case.expected == service.add_taxes(articles=case.input)
