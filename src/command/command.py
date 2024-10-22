from abc import ABC, abstractmethod

"""Interface of Command pattern"""


class Command(ABC):
    @abstractmethod
    def execute(self):
        ...

class UndoableCommand(Command):
    @abstractmethod
    def undo(self):
        ...


