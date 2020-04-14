from dataclasses import dataclass
from decimal import Decimal

from taxes.services.basket.entities.product import Product


@dataclass(frozen=True)
class TaxedArticle:
    product: Product
    quantity: int
    imported: bool
    unit_price_before_taxes: Decimal
    tax_amount_due_per_unit: Decimal
