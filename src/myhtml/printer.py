from abc import ABC, abstractmethod


class Visitor(ABC):
    @abstractmethod
    def visit(node):
        ...


class HtmlVisitor(Visitor):
    def __init__(self):
        ...
    
    def visit(self, node):
        print(node)