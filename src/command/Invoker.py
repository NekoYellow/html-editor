import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command, UndoableCommand

class CommandInvoker:
    def __init__(self):
        self.done = []
        self.undone = []
    
    def store_and_execute(self, command):
        command.execute()
        if isinstance(command, UndoableCommand):
            self.done.append(command)
            self.undone.clear()
    
    def undo_last(self):
        if self.done == []:
            return
        cmd = self.done.pop()
        if not isinstance(cmd, UndoableCommand):
            return
        cmd.undo()
        self.undone.append(cmd)
        
    def redo_last(self):
        if self.undone == []:
            return
        cmd = self.undone.pop()
        cmd.execute()
        self.done.append(cmd)
