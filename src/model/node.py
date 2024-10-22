import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.visitor import Node


class HtmlNode(Node):
    def __init__(self, tag, id=None, *children):
        self._tag = tag
        self._id = id
        self._is_text = False
        self._children = list(children)
    
    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        if not isinstance(value, str):
            raise TypeError("tag should be str")
        self._tag = value
    
    @property
    def id(self):
        return self._id
    
    @property
    def is_text(self):
        return self._is_text
    
    @is_text.setter
    def is_text(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_text should be bool")
        self._is_text = value
    
    @property
    def children(self):
        return self._children
    
    def add_child(self, child):
        if not isinstance(child, self.__class__):
            raise TypeError("child added should be HtmlNode")
        self._children.append(child)
    
    def del_child(self, child):
        try:
            self.children.remove(child)
        except ValueError:
            return
    
    def accept(self, visitor, indent=0, is_last=True, mask=0):
        visitor.visit(self, indent, is_last, mask)

    def __str__(self):
        return self.tag + (f"#{self.id}" if self.id else "")
