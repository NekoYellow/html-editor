import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.visitor import Visitor


class TreeVisitor(Visitor):
    """Concrete Visitor that gets the html content in tree format"""
    
    def __init__(self):
        self.s = ""

    def visit(self, node, indent=0, is_last=True, mask=0):
        # print(indent, is_last, mask)
        prefix = ""
        if indent > 0:
            for i in range(indent-1):
                prefix += "    " if (mask >> i) & 1 else "│   "
            prefix += ("└── " if is_last else "├── ")
        self.s += prefix + str(node) + "\n"

        for i, ch in enumerate(node.children):
            last = (i == len(node.children) - 1)
            ch.accept(self, indent + 1, last, mask | ((1 << indent) * last))

    def get_content(self):
        return self.s
