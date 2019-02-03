from .config import *
from .menu import Menu

class CLI:

    def __init__(self):
        self.menu = Menu()

    def run(self):
        chose_exit = False
        while not chose_exit:
            self.__print_commands_definitions()
            chosen_command_string = input()
            chosen_command = int(chosen_command_string)
            chose_exit = self.__execute_command(chosen_command)

    def __print_commands_definitions(self):
        print("Please choose a command to execute:")
        for number, command in COMMANDS.items():
            print("%d - %s" % (number, command['definition']))

    def __execute_command(self, command):
        is_valid_command = isinstance(command, int) and \
                           command in range(1, len(COMMANDS) + 1)
        if is_valid_command:
            if command == EXIT_COMMAND:
                print("Exiting...")
                return True
            else:
                self.menu.execute(command)

        return False