import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.visitor import Node


class HtmlNode(Node):
    def __init__(self, tag, id=None, *children):
        self._tag = tag
        self._id = id
        self._children = list(children)
    
    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value
    
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

    def __str__(self):
        return self.tag + (f"#{self.id}" if self.id else "")
