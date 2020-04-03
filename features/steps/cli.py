import subprocess

from behave import *


SUCCESS_STATUS = 0


@given('the program has been installed by the user')
def step(context):
    import taxes


@when('the user types "{command_name}" in the shell')
def step(context, command_name):
    context.command_name = command_name.split()


@when('the user doesn\'t provide any arguments or options')
def step(context):
    context.command_args = []


@when('the user provides the "{option}" option')
def step(context, option):
    args_already_set = getattr(context, 'command_args', [])
    context.command_args = [*args_already_set, option]


@when('the user executes the command')
def step(context):
    command = [*context.command_name, *context.command_args]
    context.command_result = subprocess.run(command, capture_output=True, encoding='utf-8')


@then('a help message is displayed on standard output')
def step(context):
    help_message = context.text
    assert help_message == context.command_result.stdout


@then('the command exits with a success status')
def step(context):
    assert SUCCESS_STATUS == context.command_result.returncode
