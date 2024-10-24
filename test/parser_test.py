import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from model.myhtml import Html
from interact.parser import CommandParser, InvalidCommandError
from command.insert_command import InsertCommand
from command.append_command import AppendCommand
from command.editid_command import EditidCommand
from command.edittext_command import EdittextCommand
from command.delete_command import DeleteCommand
from interact.show_command import ShowCommand
from interact.spellcheck_command import SpellCheckCommand
from file.read_command import ReadCommand
from file.save_command import SaveCommand


class CommandParserTestCase(unittest.TestCase):
    html = Html()

    def testParseInsert(self):
        parser = CommandParser(self.html)
        self.assertRaises(InvalidCommandError, lambda : parser.parse("insert a b"))
        self.assertIsInstance(parser.parse("insert a b c"), InsertCommand)
        self.assertIsInstance(parser.parse("insert a b c d"), InsertCommand)
    
    def testParseAppend(self):
        parser = CommandParser(self.html)
        self.assertRaises(InvalidCommandError, lambda : parser.parse("append a b"))
        self.assertIsInstance(parser.parse("append a b c"), AppendCommand)
        self.assertIsInstance(parser.parse("append a b c d"), AppendCommand)
    
    def testParseEditId(self):
        parser = CommandParser(self.html)
        self.assertRaises(InvalidCommandError, lambda : parser.parse("edit-id a"))
        self.assertIsInstance(parser.parse("edit-id a b"), EditidCommand)
    
    def testParseEditText(self):
        parser = CommandParser(self.html)
        self.assertRaises(InvalidCommandError, lambda : parser.parse("edit-text"))
        self.assertIsInstance(parser.parse("edit-text a"), EdittextCommand)
        self.assertIsInstance(parser.parse("edit-text a b"), EdittextCommand)
    
    def testDelete(self):
        parser = CommandParser(self.html)
        self.assertRaises(InvalidCommandError, lambda : parser.parse("delete"))
        self.assertIsInstance(parser.parse("delete a"), DeleteCommand)

    def testShow(self):
        parser = CommandParser(self.html)
        self.assertRaises(InvalidCommandError, lambda : parser.parse("print-indent a"))
        self.assertIsInstance(parser.parse("print-indent"), ShowCommand)
        self.assertIsInstance(parser.parse("print-indent 10"), ShowCommand)
        self.assertRaises(InvalidCommandError, lambda : parser.parse("print-tree 2"))
        self.assertIsInstance(parser.parse("print-tree"), ShowCommand)

    def testSpellCheck(self):
        parser = CommandParser(self.html)
        self.assertRaises(InvalidCommandError, lambda : parser.parse("spell-check a"))
        self.assertIsInstance(parser.parse("spell-check"), SpellCheckCommand)
    
    def testRead(self):
        parser = CommandParser(self.html)
        self.assertRaises(InvalidCommandError, lambda : parser.parse("read"))
        self.assertIsInstance(parser.parse("read a"), ReadCommand)
        
    def testSave(self):
        parser = CommandParser(self.html)
        self.assertRaises(InvalidCommandError, lambda : parser.parse("save"))
        self.assertIsInstance(parser.parse("save a"), SaveCommand)
    
    def testUnknown(self):
        parser = CommandParser(self.html)
        self.assertRaises(InvalidCommandError, lambda : parser.parse("aaa"))


if __name__ == "__main__":
    unittest.main()
