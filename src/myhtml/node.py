from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def accept(self, visitor):
        ...


class HtmlNode(Node):
    def __init__(self, tag, id):
        self.tag = tag
        self.id = id
        self._text = ""
        self.children = []
    
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
    
    def add_children(self, node):
        self.children.append(node)
    
    def del_children(self, node):
        try:
            self.children.remove(node)
        except ValueError as e:
            print(e)
    
    def accept(self, visitor):
        visitor.visit(self)
        for ch in self.children:
            ch.accept(visitor)

    def __str__(self):
        return f"({self.tag}, {self.id}, {self.text})"