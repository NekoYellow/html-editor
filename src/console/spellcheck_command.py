import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command
from model.myhtml import Html


class EditidCommand(Command):
    """Do spell check on texts of elements in html"""

    def __init__(self, html):
        self.html = html
        
    def execute(self):
        self.html.spell_check()
