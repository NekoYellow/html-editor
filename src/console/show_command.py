import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command
from model.myhtml import HtmlTree


class ShowCommand(Command):
    def __init__(self, html, type):
        self.html = html
        self.type = type
        
    def execute(self):
        if self.type == "tree":
            print(self.html.as_tree())
        else:
            print(self.html.as_text())
