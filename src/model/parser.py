from html.parser import HTMLParser

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.node import HtmlNode


class MyHtmlParser(HTMLParser):
    """Parses html from string via html.parser.HTMLParser in std"""
    
    def __init__(self):
        super().__init__()
        self.root = HtmlNode("", "") # dummy root
        self.stack = [self.root]
    
    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        key = None
        for k, v in attrs:
            if k == "id":
                key = v
        curr = HtmlNode(tag, key)
        self.stack[-1].add_child(curr)
        self.stack.append(curr)

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        self.stack.pop()

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        curr = HtmlNode(data, None)
        curr.is_text = True
        self.stack[-1].add_child(curr)
    
    def get_tree(self):
        return self.root.children[0]
