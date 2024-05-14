from helpers import prompt
from globals import editor_options, quit_option, view_str, create_str, delete_str

import menu_bot_viewer
import menu_bot_creator
import menu_bot_deleter


def init():
    print("This is the bot editor.")

    start_message = "How would you like to manage your bots?"
    user_editor_option = prompt(start_message, editor_options)

    while user_editor_option != quit_option:
        start_editor(user_editor_option)
        user_editor_option = prompt(start_message, editor_options)

    print("\nBack to the main menu ...")


def start_editor(editor_option: int) -> None:
    print()
    if editor_option == editor_options[view_str]:
        menu_bot_viewer.init()
    elif editor_option == editor_options[create_str]:
        menu_bot_creator.init()
    elif editor_option == editor_options[delete_str]:
        menu_bot_deleter.init()
