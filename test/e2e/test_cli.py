import subprocess
from dataclasses import dataclass
from inspect import cleandoc

import pytest


entrypoint_test_cases = pytest.mark.parametrize('entrypoint', [
    'receipt'
])

help_option_test_cases = pytest.mark.parametrize('help_opt', [
    '--help',
    '-h',
])

file_input_option_test_cases = pytest.mark.parametrize('file_input_opt', [
    '--input',
    '-i',
])

verbosity_option_test_cases = pytest.mark.parametrize('verbosity', [
    '',
    '-v',
    '-vv',
])


@dataclass
class CliTestCase:
    input: str
    expected: str

    def __post_init__(self):
        self.input = cleandoc(self.input)
        self.expected = cleandoc(self.expected) + '\n'  # print to stdout adds a newline


TEST_CASES = {
    'single food article': CliTestCase(
        input="""
            1 chocolate bar at 0.85
        """,
        expected="""
            1 chocolate bar: 0.85
            Sales Taxes: 0.00
            Total: 0.85
        """
    ),
    'single medical article': CliTestCase(
        input="""
            1 packet of headache pills at 9.75
        """,
        expected="""
            1 packet of headache pills: 9.75
            Sales Taxes: 0.00
            Total: 9.75
        """
    ),
    'single book': CliTestCase(
        input="""
            1 book at 12.49
        """,
        expected="""
            1 book: 12.49
            Sales Taxes: 0.00
            Total: 12.49
        """
    ),
    'multple food articles': CliTestCase(
        input="""
            3 chocolate bar at 0.85
        """,
        expected="""
            3 chocolate bar: 2.55
            Sales Taxes: 0.00
            Total: 2.55
        """
    ),
    'multiple medical articles': CliTestCase(
        input="""
            4 packet of headache pills at 9.75
        """,
        expected="""
            4 packet of headache pills: 39.00
            Sales Taxes: 0.00
            Total: 39.00
        """
    ),
    'multiple books': CliTestCase(
        input="""
            5 book at 12.49
        """,
        expected="""
            5 book: 62.45
            Sales Taxes: 0.00
            Total: 62.45
        """
    ),
    'single tax-free, non imported articles': CliTestCase(
        input="""
            1 packet of headache pills at 9.75
            1 book at 12.49
            1 chocolate bar at 0.85
        """,
        expected="""
            1 packet of headache pills: 9.75
            1 book: 12.49
            1 chocolate bar: 0.85
            Sales Taxes: 0.00
            Total: 23.09
        """
    ),
    'multiple tax-free, non imported articles': CliTestCase(
        input="""
            5 book at 12.49
            3 chocolate bar at 0.85
            4 packet of headache pills at 9.75
        """,
        expected="""
            5 book: 62.45
            3 chocolate bar: 2.55
            4 packet of headache pills: 39.00
            Sales Taxes: 0.00
            Total: 104.00
        """
    ),
    'multiple tax-free, imported articles': CliTestCase(
        input="""
            5 imported book at 12.49
            3 imported chocolate bar at 0.85
            4 imported packet of headache pills at 9.75
        """,
        expected="""
            5 imported book: 65.70
            3 imported chocolate bar: 2.70
            4 imported packet of headache pills: 41.00
            Sales Taxes: 5.40
            Total: 109.40
        """
    ),
    'non imported articles, exempt and non-exempt': CliTestCase(
        input="""
            1 book at 12.49
            1 music CD at 14.99
            1 chocolate bar at 0.85
        """,
        expected="""
            1 book: 12.49
            1 music CD: 16.49
            1 chocolate bar: 0.85
            Sales Taxes: 1.50
            Total: 29.83
        """
    ),
    'imported articles, exempt and non-exempt': CliTestCase(
        input="""
            1 imported box of chocolates at 10.00
            1 imported bottle of perfume at 47.50
        """,
        expected="""
            1 imported box of chocolates: 10.50
            1 imported bottle of perfume: 54.65
            Sales Taxes: 7.65
            Total: 65.15
        """
    ),
    'imported articles (interleaved imported label)': CliTestCase(
        input="""
            1 imported bottle of perfume at 27.99
            1 bottle of perfume at 18.99
            1 packet of headache pills at 9.75
            1 imported box of chocolates at 11.25
        """,
        expected="""
            1 imported bottle of perfume: 32.19
            1 bottle of perfume: 20.89
            1 packet of headache pills: 9.75
            1 imported box of chocolates: 11.85
            Sales Taxes: 6.70
            Total: 74.68
        """
    ),
    'imported articles, exempt and non-exempt': CliTestCase(
        input="""
            1 imported bottle of perfume at 27.99
            1 bottle of perfume at 18.99
            1 packet of headache pills at 9.75
            3 box of imported chocolates at 11.25
        """,
        expected="""
            1 imported bottle of perfume: 32.19
            1 bottle of perfume: 20.89
            1 packet of headache pills: 9.75
            3 imported box of chocolates: 35.55
            Sales Taxes: 7.90
            Total: 98.38
        """
    ),
}



cli_test_cases = pytest.mark.parametrize(
    'case',
    [pytest.param(case, id=id) for id, case in TEST_CASES.items()],
)


SUCCESS_STATUS = 0


@verbosity_option_test_cases
@help_option_test_cases
@entrypoint_test_cases
def test_command_returns_success_status_when_called_with_help_option(
    entrypoint,
    help_opt,
    verbosity,
):
    command = [entrypoint, help_opt, verbosity]
    result = subprocess.run(command, capture_output=True, encoding='utf-8')
    assert SUCCESS_STATUS == result.returncode



@verbosity_option_test_cases
@help_option_test_cases
@entrypoint_test_cases
def test_command_prints_help_text_to_stdout_when_called_with_help_option(
    entrypoint,
    help_opt,
    verbosity,
):
    command = [entrypoint, help_opt, verbosity]
    result = subprocess.run(command, capture_output=True, encoding='utf-8')
    expected = 'usage: receipt [-h] -i BASKET [-v]'
    assert result.stdout.startswith(expected)


@verbosity_option_test_cases
@entrypoint_test_cases
def test_command_exits_with_error_if_input_options_is_not_set(
    entrypoint,
    verbosity,
):
    command = [entrypoint, verbosity]
    result = subprocess.run(command, capture_output=True, encoding='utf-8')
    expected = (
        'usage: receipt [-h] -i BASKET [-v]\n',
        'error: receipt: error: the following arguments are required: -i/--input\n',
    )
    assert SUCCESS_STATUS != result.returncode
    assert result.stderr.startswith(expected)


@cli_test_cases
@verbosity_option_test_cases
@file_input_option_test_cases
@entrypoint_test_cases
def test_command_prints_receipt_to_stdout_when_basket_is_submitted_as_file(
    entrypoint,
    file_input_opt,
    verbosity,
    case,
    tmp_path,
):
    basket_path = tmp_path / "basket.txt"
    basket_path.write_text(case.input)
    if verbosity:
        command = [entrypoint, file_input_opt, basket_path, verbosity]
    else:
        command = [entrypoint, file_input_opt, basket_path]
    result = subprocess.run(command, capture_output=True, encoding='utf-8')

    assert SUCCESS_STATUS == result.returncode
    assert result.stdout.endswith(case.expected)
