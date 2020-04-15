from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Product:
    name: str
    category: str


class ProductError:
    class InvalidName(Exception):
        def __init__(self, value):
            super().__init__(f'invalid product name: {value}')


def create(name: str, category: Optional[str]):
    """ Create a Product from :param name: and an optional :param category:

    :param name: must be a non empty string, otherwise an error is raised.
    """
    def is_valid_string(s):
        return (isinstance(s, str) and s.strip() != '')

    if not is_valid_string(name):
        raise ProductError.InvalidName(name)

    return Product(name=name.strip(), category=category)
