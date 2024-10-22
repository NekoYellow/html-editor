import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from myhtml.parser import MyHtmlParser
from myhtml.node import HtmlNode
from util.tree_visitor import TreeVisitor
from util.html_visitor import HtmlVisitor


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
        visitor = TreeVisitor()
        self.root.accept(visitor)
        print(visitor.get_content())
    
    def show_as_text(self):
        visitor = HtmlVisitor()
        self.root.accept(visitor)
        print(visitor.get_content())


if __name__ == "__main__":
    ht = HtmlTree("sample.html")
    ht.show_as_tree()
    ht.show_as_text()
