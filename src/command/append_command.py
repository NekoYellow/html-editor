import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command, UndoableCommand
from model.myhtml import Html


class AppendCommand(UndoableCommand):
    """Insert given element(tag, id) below specified element whose id is parent"""

    def __init__(self, html, tag, id, parent, text=""):
        self.html = html
        self.tag = tag
        self.id = id
        self.parent = parent
        self.text = text
    
    def execute(self):
        self.html.insert(self.tag, self.id, self.text, self.parent)
    
    def undo(self):
        self.html.remove(self.id)
