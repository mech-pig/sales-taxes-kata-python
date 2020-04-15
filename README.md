# Sales taxes kata

The classic sales taxes kata, in python.

- [Installation](#installation)
  - [Local](#local)
  - [Docker](#docker)
- [Usage](#usage)
- [The Kata](#the-kata)
  - [Examples](#examples)
  - [Goal](#goal)
  - [Requirements](#requirements)

## Installation

### Local
#### Requirements
- Python 3.8.X (you can install it from the [official site](https://www.python.org/downloads/) or you can use your OS's package manager; you can also install it via [pyenv](https://github.com/pyenv/pyenv) to easily switch between multiple versions of Python installed on your system)
- [poetry 1.0.X](https://python-poetry.org/)

#### Install
Install the `receipt` command in a dedicated virtual environment:
```sh
make install
```

#### Run
Spawn a shell within the virtual environment:
```sh
poetry shell
```

The `receipt` command is available:
```sh
receipt -h
```

Deactivate the environment with:
```sh
deactivate
```

### Docker

#### Build
Build a Docker container with
```sh
docker build -t sales-taxes .
```

#### Run
Run the command with
```sh
docker run -v "$PWD/examples:/usr/app/examples" --rm sales-taxes -i /usr/app/examples/new-products.txt
```

## Usage

Given a `basket.txt` file:

```
1 book at 12.49
1 music CD at 14.99
1 chocolate bar at 0.85
```

run the command specifying the input file
```sh
receipt -i basket.txt
```

and the receipt will be printed on stdout
```
1 book: 12.49
1 music cd: 14.99
1 chocolate bar: 0.85
Sales Taxes: 0.00
Total: 28.33
```

## The Kata
On each purchase governments impose sales taxes that depend on many
criteria like:
- article category
- article origin (when different from the country in which the article
is sold)
- shipping destination

### Overview
Basic sales tax is applicable at a rate of `10%` on all articles
except the ones belonging to categories that are exempt:
- book
- food
- medical

Import duty is an additional sales tax applicable on all imported
articles at a rate of `5%`, with no exemptions.
For a shelf price of p and a tax rate of t% the tax amount is
`p*t/100` rounded up to the nearest `0.05`.

Customers making a purchase receive a receipt containing:
- a list of items (quantity, article name and price with taxes)
- sales taxes due
- total to be paid (including taxes)

#### Examples
##### Purchase 1
###### Basket
```
1 book at 12.49
1 music CD at 14.99
1 chocolate bar at 0.85
```
###### Receipt
```
1 book: 12.49
1 music CD: 16.49
1 chocolate bar: 0.85
Sales Taxes: 1.50
Total: 29.83
```
##### Purchase 2
###### Basket
```
1 imported box of chocolates at 10.00
1 imported bottle of perfume at 47.50
```
###### Receipt
```
1 imported box of chocolates: 10.50
1 imported bottle of perfume: 54.65
Sales Taxes: 7.65
Total: 65.15
```
##### Purchase 3
###### Basket
```
1 imported bottle of perfume at 27.99
1 bottle of perfume at 18.99
1 packet of headache pills at 9.75
1 box of imported chocolates at 11.25
```
###### Receipt
```
1 imported bottle of perfume: 32.19
1 bottle of perfume: 20.89
1 packet of headache pills: 9.75
1 imported box of chocolates: 11.85
Sales Taxes: 6.70
Total: 74.68
```

### Goal
Design and implement a solution that prints the receipt for a purchase
and demonstrate your problem solving approach and coding style and
skills with a focus on:
- simple design
- separation of concerns
- readability
- testability

### Requirements
- Use a programming language of your choice
- Use a build automation tool
- Keep it simple: do not use third-party libraries apart for unit
testing and, if needed, mocking frameworks (no Web, ORM, DI)
- Use any mechanism to provide input (hard coded data within a unit
test is ok)
- Fulfill at least the scenarios provided in the example above
