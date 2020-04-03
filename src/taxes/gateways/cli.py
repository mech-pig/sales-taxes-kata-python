import argparse


parser = argparse.ArgumentParser(
    prog='receipt',
    description='Add taxes to purchased items and prints the receipt.',
)


def main():
    parser.print_help()
