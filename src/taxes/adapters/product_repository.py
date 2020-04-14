from dataclasses import dataclass
from typing import List

from taxes.services.basket.entities.product import Product
from taxes.services.basket.service import Dependency as BasketServiceDependency


@dataclass
class InMemoryProductRepository(BasketServiceDependency.ProductRepository):
    """ An in-memory product repository """
    products: List[Product]

    def __post_init__(self):
        self.by_name = {product.name: product for product in self.products}

    def get_by_name(self, name: str):
        return self.by_name.get(name, Product(name=name, category=None))


KATA_EXAMPLE_PRODUCT_REPOSITORY = InMemoryProductRepository(
    products=[
        Product(name='book', category='book'),
        Product(name='chocolate bar', category='food'),
        Product(name='box of chocolates', category='food'),
        Product(name='packet of headache pills', category='medical'),
    ],
)
