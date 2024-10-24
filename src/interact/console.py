import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.myhtml import Html
from command.invoker import CommandInvoker
from interact.parser import CommandParser


"""A console accepting input from command line"""

if __name__ == "__main__":
    html = Html()
    parser = CommandParser(html)
    invoker = CommandInvoker()
    while True:
        print("Enter Command: ")
        cmd_str = input().strip()
        if cmd_str == "exit":
            break
        elif cmd_str == "init":
            html = Html()
            continue
        try:
            cmd = parser.parse(cmd_str)
            invoker.handle(cmd)
        except ValueError as e:
            print(e)
