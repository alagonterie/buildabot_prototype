from globals import quit_option, confirm_options
from helpers import prompt, get_bot_options, is_valid_bots_file

import bot_executor


def init():
    if not is_valid_bots_file():
        print('The "bots.txt" file is invalid. Ensure correct formatting/syntax and unique bot names.', end="")
    else:
        print("These are your created bots.")

        run_message = "Choose a bot to run."
        bots_by_int, bots_by_str = get_bot_options()
        user_run_option = prompt(run_message, bots_by_str)

        while user_run_option != quit_option:
            confirm_bot_run(bots_by_int[user_run_option])
            user_run_option = prompt(run_message, bots_by_str)

    print("\nBack to the main menu ...")


def confirm_bot_run(bot_option: str) -> None:
    view_message = f'Do you want to run the "{bot_option}" bot now?'
    user_view_option = prompt(view_message, confirm_options)

    while user_view_option != quit_option:
        bot_executor.execute(bot_option)
        user_view_option = prompt(view_message.replace("now", "again"), confirm_options)

    print("\nBack to your created bots ...")
