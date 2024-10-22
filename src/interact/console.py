import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.myhtml import Html
from command.invoker import CommandInvoker
from interact.parser import CommandParser


if __name__ == "__main__":
    html = Html()
    parser = CommandParser(html)
    invoker = CommandInvoker()
    while True:
        print("Enter Command: ")
        cmd_str = input().strip()
        if cmd_str == "exit":
            break
        try:
            cmd = parser.parse(cmd_str)
            invoker.store_and_execute(cmd)
        except ValueError as e:
            print(e)
