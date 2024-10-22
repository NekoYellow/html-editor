import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.parser import MyHtmlParser
from model.node import HtmlNode
from model.tree_visitor import TreeVisitor
from model.html_visitor import HtmlVisitor


class Html:
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
    
    def as_tree(self):
        visitor = TreeVisitor()
        self.root.accept(visitor)
        return visitor.get_content()
    
    def as_text(self):
        visitor = HtmlVisitor()
        self.root.accept(visitor)
        return visitor.get_content()


if __name__ == "__main__":
    ht = Html("sample.html")
    print(ht.as_tree())
    print(ht.as_text())
