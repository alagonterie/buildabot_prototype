from helpers import prompt
from globals import start_options, quit_option, run_str, editor_str

import menu_bot_runner
import menu_bot_editor


def init():
    print("Welcome to Build-a-Bot!")

    start_message = "What do you want to do?"
    user_start_option = prompt(start_message, start_options, True)

    while user_start_option != quit_option:
        user_start(user_start_option)
        user_start_option = prompt(start_message, start_options, True)

    print("\nQuitting ...")


def user_start(start_option: int) -> None:
    print()
    if start_option == start_options[run_str]:
        menu_bot_runner.init()
    elif start_option == start_options[editor_str]:
        menu_bot_editor.init()
