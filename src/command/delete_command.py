import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command, UndoableCommand
from model.myhtml import Html


class DeleteCommand(UndoableCommand):
    """Delete specified element"""

    def __init__(self, html, id):
        self.html = html
        self.id = id

    def execute(self):
        self.node, self.parent = self.html.find(self.id)
        self.html.remove(self.id)

    def undo(self):
        self.html.append(self.node, self.parent)
