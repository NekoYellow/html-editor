import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from visitor import Visitor


class PrintVisitor(Visitor):
    def visit(self, node, indent=0, is_last=True, mask=0):
        # print(indent, is_last, mask)
        prefix = ""
        if indent > 0:
            for i in range(indent-1):
                prefix += "    " if (mask >> i) & 1 else "│   "
            prefix += ("└── " if is_last else "├── ")
        print(prefix + str(node))

        for i, ch in enumerate(node.children):
            last = (i == len(node.children) - 1)
            ch.accept(self, indent + 1, last, mask | ((1 << indent) * last))


class TreeShow:
    def __init__(self, tree_root):
        self.root = tree_root
        self.pv = PrintVisitor()
    
    def print(self):
        self.root.accept(self.pv)