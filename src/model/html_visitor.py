import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.visitor import Visitor


class HtmlVisitor(Visitor):
    def __init__(self, indent):
        self.s = ""
        self.pf = " " * indent

    def visit(self, node, indent=0, is_last=True, mask=0):
        self.s += self.pf * indent
        if node.is_text:
            self.s += node.tag + "\n"
        else:
            self.s += "<" + node.tag + (" id=\"" + node.id + "\"" if node.id != None else "") + ">\n"
        for child in node.children:
            child.accept(self, indent + 1)
        if not node.is_text:
            self.s += self.pf * indent
            self.s += "<\\" + node.tag + ">\n"
    
    def get_content(self):
        return self.s