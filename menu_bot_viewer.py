from globals import quit_option
from helpers import prompt, get_bot_options, get_bot_commands, is_valid_bots_file


def init():
    if not is_valid_bots_file():
        print('The "bots.txt" file is invalid. Ensure correct formatting/syntax and unique bot names.', end="")
    else:
        print("These are your created bots.")

        view_message = "Choose a bot to view its details."
        bots_by_int, bots_by_str = get_bot_options()
        user_view_option = prompt(view_message, bots_by_str)

        while user_view_option != quit_option:
            show_bot_view(bots_by_int[user_view_option])
            user_view_option = prompt(view_message, bots_by_str)

    print("\nBack to the editor ...")


def show_bot_view(bot_option: str) -> None:
    bot_commands = "\n".join([f"Command #{i} - {c}" for i, c in enumerate(get_bot_commands(bot_option), start=1)])
    view_message = f'These are the commands for the "{bot_option}" bot ...\n{bot_commands}'
    user_view_option = prompt(view_message)

    while user_view_option != quit_option:
        user_view_option = prompt(view_message)

    print("\nBack to your created bots ...")
