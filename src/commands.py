from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        ...

class UndoableCommand(Command):
    @abstractmethod
    def undo(self):
        ...


