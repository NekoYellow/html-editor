import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from visitor import Visitor


class PrintVisitor(Visitor):
    def visit(self, node, indent=0, is_last=True, mask=0):
        prefix, label_prefix = "", ""
        if indent > 0:
            for i in range(indent-1):
                prefix += "    " if (mask >> i) & 1 else "│   "
            label_prefix = prefix + ("└── " if is_last else "├── ")
        print(label_prefix + node.label())
        prefix += "    " if (mask >> indent) & 1 else "│   "
        if node.content():
            print(prefix + f"└── {node.content()}")


class TreeShow:
    def __init__(self, tree_root):
        self.root = tree_root
        self.pv = PrintVisitor()
    
    def print(self):
        self.root.accept(self.pv)