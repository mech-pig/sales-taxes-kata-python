from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PurchasedItem:
    product_name: str
    unit_price: Decimal
    imported: bool
    quantity: int
