import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command, UndoableCommand
from model.myhtml import Html


class InsertCommand(UndoableCommand):
    """Insert given element(tag, id) before specified element whose id is target"""

    def __init__(self, html, tag, id, target, text=""):
        self.html = html
        # self.node = HtmlNode(tag, id)
        # if text != "":
        #     text_node = HtmlNode(text)
        #     text_node.is_text = True
        #     self.node.add_child(text_node)
        self.tag = tag
        self.id = id
        self.target = target
        self.text = text
    
    def execute(self):
        self.html.insert(self.tag, self.id, self.text, self.target)
    
    def undo(self):
        self.html.remove(self.id)
