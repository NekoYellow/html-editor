import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.visitor import Node


class HtmlNode(Node):
    def __init__(self, tag, id=None, *children):
        self._tag = tag
        self._id = id
        self._text = ""
        self._children = list(children)
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
    
    @property
    def tag(self):
        return self._tag
    
    @property
    def id(self):
        return self._id
    
    @property
    def children(self):
        return self._children
    
    def add_child(self, child):
        self._children.append(child)
    
    def del_child(self, child):
        try:
            self.children.remove(child)
        except ValueError as e:
            print(e)
    
    def accept(self, visitor, indent=0, is_last=True, mask=0):
        visitor.visit(self, indent, is_last, mask)
        for i, ch in enumerate(self.children):
            last = (i == len(self.children) - 1)
            ch.accept(visitor, indent + 1, last, mask | ((1 << indent) * last))

    def label(self):
        return self.tag + (f"#{self.id}" if self.id else "")

    def content(self):
        return self.text
