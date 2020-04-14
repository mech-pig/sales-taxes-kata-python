import argparse
import logging

from taxes.adapters.product_repository import KATA_EXAMPLE_PRODUCT_REPOSITORY
from taxes.services.basket.service import create as create_basket_service
from taxes.services.receipt.entities.receipt import Receipt, ReceiptItem
from taxes.services.receipt.service import create as create_receipt_service
from taxes.services.parser import parse_item
from taxes.services.tax import create as create_tax_service


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


def load_basket_file(file):
    with open(file, mode='r', encoding='utf-8') as f:
        return [parse_item(row) for row in f]


def dump_receipt(receipt: Receipt):
    def dump_item(item: ReceiptItem):
        return ' '.join([
            f'{item.quantity}',
            f'{item.description}:',
            f'{item.subtotal_price_with_taxes}'
        ])

    return '\n'.join([
        *[dump_item(item) for item in receipt.items],
        f'Sales Taxes: {receipt.taxes_due}',
        f'Total: {receipt.total_due}',
    ])


def main():
    tax_service = create_tax_service(
        logger=logging.getLogger('tax'),
    )
    basket_service = create_basket_service(
        logger=logging.getLogger('basket'),
        product_repository=KATA_EXAMPLE_PRODUCT_REPOSITORY,
    )
    receipt_service = create_receipt_service(
        logger=logging.getLogger('receipt'),
        tax_service=tax_service,
    )

    args = parser.parse_args()
    if not args.input:
        parser.print_help()

    purchased_articles = load_basket_file(args.input)
    articles_in_basket = basket_service.create_basket(purchased_articles)
    receipt = receipt_service.create_receipt(articles=articles_in_basket)
    result = dump_receipt(receipt)
    print(result)
