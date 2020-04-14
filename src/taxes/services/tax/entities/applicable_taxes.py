from decimal import Decimal
from typing import Set

from taxes.services.tax.entities.tax import Tax


EXEMPT_CATEGORIES = [
    'book',
    'food',
    'medical',
]

TAX_IMPORT = Tax(id='import', rate=Decimal('0.05'))
TAX_PRODUCT_CATEGORY = Tax(id='non-exempt-category', rate=Decimal('0.1'))


def get_applicable_taxes(article) -> Set[Tax]:
    return {
        *get_import_taxes(article),
        *get_product_category_taxes(article),
    }


def get_import_taxes(article) -> Set[Tax]:
    if article.imported:
        return {TAX_IMPORT}
    return set()


def get_product_category_taxes(article) -> Set[Tax]:
    if article.product.category not in EXEMPT_CATEGORIES:
        return {TAX_PRODUCT_CATEGORY}
    return set()
