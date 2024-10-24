import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command


class UndoCommand(Command):
    """Undo the previous undoable command"""

    def __init__(self):
        pass
    
    def execute(self):
        pass
