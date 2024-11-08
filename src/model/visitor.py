from abc import ABC, abstractmethod

"""The interface of Visitor pattern"""


class Node(ABC):
    @abstractmethod
    def accept(self, visitor):
        ...
    
    @abstractmethod
    def __str__(self):
        ...


class Visitor(ABC):
    @abstractmethod
    def visit(node):
        ...
