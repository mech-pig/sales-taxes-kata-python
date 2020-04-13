import argparse
import logging

from taxes.adapters import stdio
from taxes.adapters.basket_service import BasketServiceAdapter
from taxes.services.basket.service import create as create_basket_service
from taxes.services.receipt.service import create as create_receipt_service
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
)


def main():
    tax_service = create_tax_service(logger=logging.getLogger('tax'))
    basket_service = BasketServiceAdapter(
        basket_service=create_basket_service(
            logger=logging.getLogger('basket')
        )
    )
    receipt_service = create_receipt_service(
        logger=logging.getLogger('receipt'),
        basket_service=basket_service,
        tax_service=tax_service,
    )
    args = parser.parse_args()
    if args.input:
        articles = stdio.loads(args.input)
        receipt = receipt_service.create_receipt(articles=articles)
        result = stdio.dump(receipt)
        print(result)
