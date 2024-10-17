from html.parser import HTMLParser
from node import HtmlNode


class MyHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = HtmlNode("", "")
        self.stack = [self.root]
        self.ids = set()
    
    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        key = None
        for k, v in attrs:
            if k == "id":
                key = v
        self.ids.add(key if key != None else tag)
        curr = HtmlNode(tag, key)
        self.stack[-1].add_child(curr)
        self.stack.append(curr)

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        self.stack.pop()

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        self.stack[-1].add_child(HtmlNode(data, None))
        # self.stack[-1].text = data
    
    def get_tree(self):
        return self.root.children[0]

    def get_ids(self):
        return self.ids

