from taxes.services import parser
from taxes.services.basket.entities import article
from taxes.services.receipt.entities.receipt import Receipt, ReceiptItem


def loads(file):
    with open(file, mode='r', encoding='utf-8') as f:
        items = (parser.parse_item(row) for row in f)
        return [
            article.create(
                product_unit_price=row['unit_price'],
                product_name=row['product_name'],
                quantity=row['quantity'],
            ) for row in items
        ]


def dump(receipt: Receipt):
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
