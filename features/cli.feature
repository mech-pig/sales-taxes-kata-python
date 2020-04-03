Feature: CLI entry point
  In order to add taxes to a receipt
  As a shell user
  I want a to call a CLI command to execute the calculations
  So that I don't have to switch application for doing the calculations

  Scenario Outline: Command is called without argument
    Given the program has been installed by the user
     When the user types "<command_entrypoint>" in the shell
      And the user doesn't provide any arguments or options
      And the user executes the command
     Then a help message is displayed on standard output
        """
        usage: receipt [-h]

        Add taxes to purchased items and prints the receipt.

        optional arguments:
          -h, --help  show this help message and exit

        """
      And the command exits with a success status

    Examples: Command entrypoints
      | command_entrypoint  |
      | receipt             |

  Scenario Outline: Command is called with "help" flag
    Given the program has been installed by the user
     When the user types "<command_entrypoint>" in the shell
      And the user provides the "<help_option>" option
      And the user executes the command
     Then a help message is displayed on standard output
        """
        usage: receipt [-h]

        Add taxes to purchased items and prints the receipt.

        optional arguments:
          -h, --help  show this help message and exit

        """
      And the command exits with a success status

    Examples: Command
      | command_entrypoint  | help_option |
      | receipt             | --help      |
      | receipt             | -h          |
