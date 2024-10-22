import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command, UndoableCommand
from model.myhtml import Html


class EditidCommand(UndoableCommand):
    """Update id of specified element whose id is oldid to newid"""

    def __init__(self, html, oldid, newid):
        self.html = html
        self.oldid = oldid
        self.newid = newid
        
    def execute(self):
        self.html.update_id(self.oldid, self.newid)
    
    def undo(self):
        self.html.update_id(self.newid, self.oldid)
