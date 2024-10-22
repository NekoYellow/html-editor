import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from command.command import Command
from model.myhtml import Html
from file.io import Loader


class ReadCommand(Command):
    """Read html from file"""
    def __init__(self, html, filename):
        self.html = html
        self.filename = filename
    
    def execute(self):
        self.html.set(Loader.load(self.filename))