import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command


class RedoCommand(Command):
    """Redo the previous undone command"""

    def __init__(self):
        pass
    
    def execute(self):
        pass
