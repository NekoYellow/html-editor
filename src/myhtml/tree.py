from parser import MyHtmlParser
from node import HtmlNode

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.treeshow import TreeShow
from util.visitor import Visitor


class HtmlTree:
    PRIMARY_TAGS = ("html", "head", "title", "body")

    @staticmethod
    def _default():
        return HtmlNode("html", "html",
                    HtmlNode("head", "head",
                        HtmlNode("title", "title")
                    ),
                    HtmlNode("body", "body")
                )
    
    def __init__(self):
        self.root = self._default()
        self.ids = set(self.PRIMARY_TAGS)

    def __init__(self, filename):
        try:
            with open(filename, 'r') as f:
                html_str = ""
                for line in f.readlines():
                    html_str += line.strip()
        except FileNotFoundError as e:
            print(e)
            return
        parser = MyHtmlParser()
        parser.feed(html_str)
        
        self.root = parser.get_tree()
        self.ids = parser.get_ids()
    
    def show_as_tree(self):
        TreeShow(self.root).print()
    
    def show_as_text(self):
        tv = TextVisitor()
        tv.visit(self.root)
        print(tv.get_text())


class TextVisitor(Visitor):
    def __init__(self):
        self.s = ""

    def visit(self, node, indent=0, is_last=True, mask=0):
        self.s += "  " * indent
        if node.is_text:
            self.s += node.tag + "\n"
        else:
            self.s += "<" + node.tag + (" id=\"" + node.id + "\"" if node.id != None else "") + ">\n"
        for child in node.children:
            self.visit(child, indent + 1)
        if not node.is_text:
            self.s += "  " * indent
            self.s += "<\\" + node.tag + ">\n"
    
    def get_text(self):
        return self.s


ht = HtmlTree("sample.html")
ht.show_as_tree()
ht.show_as_text()