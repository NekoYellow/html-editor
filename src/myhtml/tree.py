from parser import MyHtmlParser
from node import HtmlNode


class HtmlTree:
    PRIMARY_TAGS = ("html", "head", "title", "body")

    @staticmethod
    def _default():
        return HtmlNode("html", "html", "",
                    HtmlNode("head", "head", "",
                        HtmlNode("title", "title", "")
                    ),
                    HtmlNode("body", "body", "")
                )
    
    def __init__(self):
        self.root = self._default()
        self.ids = set(self.PRIMARY_TAGS)

    def __init__(self, filename):
        # self.root = HtmlParser.parse(filename)
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

