import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command


class ShowCommand(Command):
    """Show the html in tree or text format"""

    def __init__(self, string):
        self.string = string
    
    def execute(self):
        print(self.string)
