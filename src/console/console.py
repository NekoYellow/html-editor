import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.tree import HtmlTree


if __name__ == "__main__":
    html = HtmlTree()
    invoker = CommandInvoker()
    while True:
        print("Enter Command: ")
        cmd_str = input().strip()
        if cmd_str == "exit":
            break
        try:
            cmd = Parser.parse(cmd_str)
            invoker.store_and_execute(cmd)
        except InvalidCommandException as e:
            print(e)