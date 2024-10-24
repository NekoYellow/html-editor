import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from command.command import Command, UndoableCommand
from command.invoker import CommandInvoker, UndoError, RedoError
from command.undo_command import UndoCommand
from command.redo_command import RedoCommand


# for testing

buf = []

class ClearCommand(Command):
    def __init__(self):
        pass

    def execute(self):
        global buf
        buf = []

class AppendCommand(UndoableCommand):
    def __init__(self, element):
        self.element = element
    
    def execute(self):
        buf.append(self.element)
    
    def undo(self):
        buf.pop()


class CommandInvokerTestCase(unittest.TestCase):
    def testStoreAndExecute(self):
        invoker = CommandInvoker()
        invoker.store_and_execute(ClearCommand())
        self.assertEqual(buf, [])
        self.assertEqual(invoker.done, [])
        self.assertEqual(invoker.undone, [])

        ac = AppendCommand('a')
        invoker.store_and_execute(ac)
        self.assertEqual(buf, ['a'])
        self.assertEqual(invoker.done, [ac])
        self.assertEqual(invoker.undone, [])
    
    def testUndo(self):
        invoker = CommandInvoker()
        invoker.store_and_execute(ClearCommand())
        self.assertEqual(buf, [])
        self.assertRaises(UndoError, lambda : invoker.undo_last())
        
        ac = AppendCommand('b')
        invoker.store_and_execute(ac)
        self.assertEqual(buf, ['b'])
        self.assertEqual(invoker.done, [ac])
        self.assertEqual(invoker.undone, [])
        
        invoker.undo_last()
        self.assertEqual(buf, [])
        self.assertEqual(invoker.done, [])
        self.assertEqual(invoker.undone, [ac])
    
    def testRedo(self):
        invoker = CommandInvoker()
        invoker.store_and_execute(ClearCommand())
        self.assertEqual(buf, [])
        self.assertRaises(RedoError, lambda : invoker.redo_last())

        ac = AppendCommand('c')
        invoker.store_and_execute(ac)
        self.assertRaises(RedoError, lambda : invoker.redo_last())
        self.assertEqual(buf, ['c'])
        self.assertEqual(invoker.done, [ac])
        self.assertEqual(invoker.undone, [])

        invoker.undo_last()
        self.assertEqual(buf, [])
        self.assertEqual(invoker.done, [])
        self.assertEqual(invoker.undone, [ac])

        invoker.redo_last()
        self.assertEqual(buf, ['c'])
        self.assertEqual(invoker.done, [ac])
        self.assertEqual(invoker.undone, [])

    def testHandle(self):
        invoker = CommandInvoker()
        invoker.handle(ClearCommand())
        self.assertEqual(buf, [])

        ac = AppendCommand('c')
        invoker.handle(ac)
        self.assertEqual(buf, ['c'])
        self.assertEqual(invoker.done, [ac])
        self.assertEqual(invoker.undone, [])

        invoker.handle(UndoCommand())
        self.assertEqual(buf, [])
        self.assertEqual(invoker.done, [])
        self.assertEqual(invoker.undone, [ac])

        invoker.handle(RedoCommand())
        self.assertEqual(buf, ['c'])
        self.assertEqual(invoker.done, [ac])
        self.assertEqual(invoker.undone, [])
        
        invoker.handle(ClearCommand())
        self.assertEqual(buf, [])
    
    def testComprehensive(self):
        invoker = CommandInvoker()
        invoker.handle(ClearCommand())
        self.assertEqual(buf, [])

        invoker.handle(AppendCommand('a'))
        self.assertEqual(buf, ['a'])
        invoker.handle(AppendCommand('b'))
        self.assertEqual(buf, ['a', 'b'])
        invoker.handle(UndoCommand())
        self.assertEqual(buf, ['a'])
        invoker.handle(AppendCommand('c'))
        self.assertEqual(buf, ['a', 'c'])
        self.assertRaises(RedoError, lambda : invoker.handle(RedoCommand()))
        invoker.handle(UndoCommand())
        self.assertEqual(buf, ['a'])
        invoker.handle(RedoCommand())
        self.assertEqual(buf, ['a', 'c'])


if __name__ == '__main__':  
    unittest.main()
