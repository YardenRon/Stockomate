from .config import COMMANDS

class Menu:

    def execute(self, command_number):
        COMMANDS[command_number]["action"]()