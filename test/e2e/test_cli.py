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

}

cli_test_cases = pytest.mark.parametrize(
    'case',
    [pytest.param(case, id=id) for id, case in TEST_CASES.items()],
)


SUCCESS_STATUS = 0


@help_option_test_cases
@entrypoint_test_cases
def test_command_returns_success_status_when_called_with_help_option(entrypoint, help_opt):
    result = subprocess.run([entrypoint, help_opt], capture_output=True, encoding='utf-8')
    assert SUCCESS_STATUS == result.returncode


@help_option_test_cases
@entrypoint_test_cases
def test_command_prints_help_text_to_stdout_when_called_with_help_option(entrypoint, help_opt):
    result = subprocess.run([entrypoint, help_opt], capture_output=True, encoding='utf-8')
    expected = 'usage: receipt [-h] [-i BASKET]'
    assert result.stdout.startswith(expected)


@cli_test_cases
@file_input_option_test_cases
@entrypoint_test_cases
def test_command_prints_receipt_to_stdout_when_basket_is_submitted_as_file(
    entrypoint,
    file_input_opt,
    case,
    tmp_path,
):
    basket_path = tmp_path / "basket.txt"
    basket_path.write_text(case.input)
    command = [entrypoint, file_input_opt, basket_path]
    result = subprocess.run(command, capture_output=True, encoding='utf-8')

    assert SUCCESS_STATUS == result.returncode
    assert case.expected == result.stdout