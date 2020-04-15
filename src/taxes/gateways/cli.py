import argparse
import logging
from dataclasses import dataclass

from taxes.adapters.product_repository import KATA_EXAMPLE_PRODUCT_REPOSITORY
from taxes.services.basket.service import create as create_basket_service
from taxes.services.receipt.entities.receipt import Receipt, ReceiptItem
from taxes.services.receipt.service import create as create_receipt_service
from taxes.services.parser import parse_item
from taxes.services.tax.service import create as create_tax_service


class CliController:

    @dataclass
    class Config:
        log_level: str
        encoding: str

    def __init__(self, config: Config):
        logging.basicConfig(level=config.log_level)

        basket_service = create_basket_service(
            logger=logging.getLogger('basket'),
            product_repository=KATA_EXAMPLE_PRODUCT_REPOSITORY,
        )

        tax_service = create_tax_service(
            logger=logging.getLogger('tax'),
        )

        receipt_service = create_receipt_service(
            logger=logging.getLogger('receipt'),
            tax_service=tax_service,
        )

        self.config = config
        self.create_basket = basket_service.create_basket
        self.create_receipt = receipt_service.create_receipt

    def load_purchased_items(self, filepath):
        with open(filepath, mode='r', encoding=self.config.encoding) as f:
            return [parse_item(row) for row in f]

    @staticmethod
    def receipt_to_str(receipt: Receipt):
        def item_to_str(item: ReceiptItem):
            return ' '.join([
                f'{item.quantity}',
                f'{item.description}:',
                f'{item.subtotal_price_with_taxes}'
            ])

        return '\n'.join([
            *[item_to_str(item) for item in receipt.items],
            f'Sales Taxes: {receipt.taxes_due}',
            f'Total: {receipt.total_due}',
        ])

    def print_receipt(self, purchased_items_filepath: str) -> str:
        purchased_items = self.load_purchased_items(purchased_items_filepath)
        articles_in_basket = self.create_basket(purchased_items)
        receipt = self.create_receipt(articles_in_basket)
        printed_receipt = self.receipt_to_str(receipt)
        return printed_receipt


def parse_args():
    parser = argparse.ArgumentParser(
        prog='receipt',
        description='Add taxes to purchased items and prints the receipt.',
    )
    parser.add_argument(
        '-i',
        '--input',
        metavar='BASKET',
        help='a path to a file containing a basket',
        required=True,
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='set verbosity level',
        action='count',
        default=0,
    )
    return parser.parse_args()


def log_level_from_verbosity(verbosity: int):
    if verbosity > 1:
        return logging.DEBUG
    elif verbosity > 0:
        return logging.INFO
    return logging.ERROR


def main():
    args = parse_args()
    config = CliController.Config(
        log_level=log_level_from_verbosity(args.verbose),
        encoding='utf-8',
    )
    controller = CliController(config=config)

    printed_receipt = controller.print_receipt(args.input)
    print(printed_receipt)
