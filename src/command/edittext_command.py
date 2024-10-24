import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command, UndoableCommand
from model.myhtml import Html


class EdittextCommand(UndoableCommand):
    """Update text of specified element with given id"""

    def __init__(self, html, id, text=""):
        self.html = html
        self.id = id
        self.oldtext = ""
        self.newtext = text
        
    def execute(self):
        self.oldtext = self.html.get_text_of(self.id)
        self.html.update_text(self.id, self.newtext)
    
    def undo(self):
        self.newtext = self.html.get_text_of(self.id)
        self.html.update_text(self.id, self.oldtext)
