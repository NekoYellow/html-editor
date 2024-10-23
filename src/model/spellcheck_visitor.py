from textblob import TextBlob
from difflib import Differ
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.visitor import Visitor


class SpellcheckVisitor(Visitor):
    """Concrete Visitor that performs spell checking on the contents inside html"""
    
    def __init__(self):
        self.s = ""

    def visit(self, node, indent=0, is_last=True, mask=0):
        prefix = ""
        if indent > 0:
            for i in range(indent-1):
                prefix += "    " if (mask >> i) & 1 else "│   "
            prefix += ("└── " if is_last else "├── ")
        self.s += prefix
        
        if node.is_text:
            original = node.tag
            corrected = str(TextBlob(original).correct())
            differ = Differ()
            diff = differ.compare(original.split(), corrected.split())
            for d in diff:
                self.s += " " + d.replace('\n', '')
        else:
            self.s += str(node)
        
        self.s += "\n"

        for i, ch in enumerate(node.children):
            last = (i == len(node.children) - 1)
            ch.accept(self, indent + 1, last, mask | ((1 << indent) * last))

    def get_content(self):
        return self.s
