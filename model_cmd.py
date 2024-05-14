from typing import List
from globals import cmd_set


class Cmd:
    cmd_name: str
    args: List[str]

    def __init__(self, cmd_name: str, args: List[str]):
        if cmd_name in cmd_set:
            self.cmd_name = cmd_name
        else:
            raise Exception(f"'{cmd_name}' is not a valid command")

        if args is not None and any(args):
            self.args = args
        else:
            raise Exception("a command must have at least one argument")

    def __repr__(self):
        return f"{self.cmd_name}({', '.join(self.args)})"
