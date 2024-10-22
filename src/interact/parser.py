import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.myhtml import Html
from command.command import Command
from command.insert_command import InsertCommand
from command.append_command import AppendCommand
from command.editid_command import EditidCommand
from command.edittext_command import EdittextCommand
from command.delete_command import DeleteCommand
from interact.show_command import ShowCommand
from interact.spellcheck_command import SpellCheckCommand


class CommandParser:
    def __init__(self, html):
        self.html = html

    def parse(self, command_str):
        parts = command_str.split()
        cmd, args = parts[0].lower(), [self.html] + parts[1:]
        if cmd == "insert":
            if len(parts) < 4 or len(args) > 5:
                raise ValueError("insert tagName idValue insertLocation [textContent]")
            return InsertCommand(*args)
        elif cmd == "append":
            if len(parts) < 4 or len(parts) > 5:
                raise ValueError("append tagName idValue parentElement [textContent]")
            return AppendCommand(*args)
        elif cmd == "edit-id":
            if len(parts) != 3:
                raise ValueError("edit-id oldId newId")
            return EditidCommand(*args)
        elif cmd == "edit-text":
            if len(parts) < 2 or len(parts) > 3:
                raise ValueError("edit-text element [newTextContent]")
            return EdittextCommand(*args)
        elif cmd == "delete":
            if len(parts) != 2:
                raise ValueError("delete element")
            return DeleteCommand(*args)
        elif cmd == "print-indent":
            if len(parts) != 1:
                raise ValueError("print-indent")
            return ShowCommand(self.html, "text")
        elif cmd == "print-tree":
            if len(parts) != 1:
                raise ValueError("print-tree")
            return ShowCommand(self.html, "tree")
        elif cmd == "spell-check":
            if len(parts) != 1:
                raise ValueError("spell-check")
            return SpellCheckCommand(self.html)
        else:
            raise ValueError(" ".join(["unknown command:", *parts]))