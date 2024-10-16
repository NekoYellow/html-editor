from my_html import Html

if __name__ == "__main__":
    html = Html()
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