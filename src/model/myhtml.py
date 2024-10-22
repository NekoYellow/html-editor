from hashlib import sha512

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.parser import MyHtmlParser
from model.node import HtmlNode
from model.tree_visitor import TreeVisitor
from model.html_visitor import HtmlVisitor


class Html:
    def __init__(self, init_str=""):
        if init_str == "":
            self.root = HtmlNode("html", None,
                            HtmlNode("head", None,
                                HtmlNode("title", None)
                            ),
                            HtmlNode("body", None)
                        )
        else:
            parser = MyHtmlParser()
            parser.feed(init_str)
            self.root = parser.get_tree()
        # id -> node mapping
        self.id2node = {}
        def dfs(u):
            self.id2node[u.id if u.id != None else self._tag2id(u.tag)] = u
            for v in u.children:
                dfs(v)
        dfs(self.root)
    
    def insert(self, tag, id, text, target):
        ...
    
    def as_tree(self):
        visitor = TreeVisitor()
        self.root.accept(visitor)
        return visitor.get_content()
    
    def as_text(self):
        visitor = HtmlVisitor()
        self.root.accept(visitor)
        return visitor.get_content()
    
    def _tag2id(self, t):
        return sha512(t.encode()).hexdigest()


if __name__ == "__main__":
    ht = Html("sample.html")
    print(ht.as_tree())
    print(ht.as_text())
