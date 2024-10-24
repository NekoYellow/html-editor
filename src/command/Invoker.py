import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command, UndoableCommand
from command.undo_command import UndoCommand
from command.redo_command import RedoCommand


class UndoError(ValueError):
    pass

class RedoError(ValueError):
    pass


class CommandInvoker:
    def __init__(self):
        self.done = []
        self.undone = []
    
    def handle(self, command):
        if isinstance(command, UndoCommand):
            self.undo_last()
        elif isinstance(command, RedoCommand):
            self.redo_last()
        else:
            self.store_and_execute(command)
    
    def store_and_execute(self, command):
        command.execute()
        if isinstance(command, UndoableCommand):
            self.done.append(command)
            self.undone.clear()
    
    def undo_last(self):
        if self.done == []:
            raise UndoError("no command to undo")
        cmd = self.done.pop()
        cmd.undo()
        self.undone.append(cmd)
        
    def redo_last(self):
        if self.undone == []:
            raise RedoError("no command to redo")
        cmd = self.undone.pop()
        cmd.execute()
        self.done.append(cmd)
