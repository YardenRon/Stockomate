from .config import COMMANDS

class CLI:

    def run(self):
        print("Please choose a command to execute:")
        for command in COMMANDS:
            print("%d - %s" % (command['number'], command['message']))

        # Get user input
        # Switch case over it
        # For each command create a method