import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.myhtml import Html
from command.invoker import Invoker
from console.parser import Parser


if __name__ == "__main__":
    html = Html()
    invoker = Invoker()
    while True:
        print("Enter Command: ")
        cmd_str = input().strip()
        if cmd_str == "exit":
            break
        try:
            cmd = Parser.parse(cmd_str)
            invoker.store_and_execute(cmd)
        except ValueError as e:
            print(e)