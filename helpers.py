import re
from typing import Dict, List, Tuple
from globals import quit_option, quit_str, back_str, cmd_bot, cmd_loop_start, cmd_loop_end, re_bot_name, re_cmd_name
from model_cmd import Cmd
from model_index_and_count import IndexAndCount


def prompt(message: str, options: Dict[str, int] = None, can_quit: bool = False) -> int:
    if options is None:
        options = {}

    options[quit_str if can_quit else back_str] = quit_option
    options_str = "\n".join(f'{options[x]}: {x}' for x in options.keys()) + "\n> "
    prompt_message = f"\n{message}\n{options_str}"

    user_option = input(prompt_message)
    valid_option = -1
    if user_option.isnumeric() and int(user_option) in options.values():
        valid_option = int(user_option)
    else:
        print(f"\nMust choose one of the given options: {', '.join(str(k) for k in options.values())}", end="")

    return valid_option


def get_all_bot_names() -> List[str]:
    with open("example_forza_game_script.txt") as bots_file:
        re_bot_name_statement = f'(?<={cmd_bot} ){re_bot_name}(?=\n)'
        bot_names = [re.search(re_bot_name_statement, bot)[0] for bot in bots_file.read().strip().split('\n\n')]

        return bot_names


def get_bot_commands(bot_name: str, unpack_loops=False) -> List[Cmd]:
    bot_command_strings = get_bot_command_strings(bot_name)
    bot_command_keywords = [cmd_str.split() for cmd_str in bot_command_strings]
    bot_commands = [Cmd(keywords[0], keywords[1::]) for keywords in bot_command_keywords]

    if unpack_loops:
        bot_commands = get_commands_with_loops(bot_commands)

    return bot_commands


def get_bot_command_strings(bot_name: str) -> List[str]:
    with open("example_forza_game_script.txt") as bots_file:
        re_bot_command = f'(?<={cmd_bot} {bot_name}\n)({re_cmd_name} [A-Za-z0-9 /_.]+\n?)+(?=(\n\n)?)'
        bot_commands_str = re.search(re_bot_command, bots_file.read())[0].strip()
        bot_commands = bot_commands_str.split('\n')
        return bot_commands


def get_commands_with_loops(bot_cmds: List[Cmd]) -> List[Cmd]:
    i_cmd = 0
    loop_count_dict = {}
    bot_cmds_with_loops = []

    while i_cmd < len(bot_cmds):
        curr_cmd = bot_cmds[i_cmd]

        if curr_cmd.cmd_name == cmd_loop_end:
            curr_loop = loop_count_dict[curr_cmd.args[0]]
            curr_loop.count -= 1

            if curr_loop.count == 0:
                i_cmd += 1
            else:
                i_cmd = curr_loop.index + 1

            continue

        if curr_cmd.cmd_name not in {cmd_loop_start, cmd_loop_end}:
            bot_cmds_with_loops.append(curr_cmd)

        if curr_cmd.cmd_name == cmd_loop_start:
            loop_count_dict[curr_cmd.args[0]] = IndexAndCount(i_cmd, int(curr_cmd.args[1]))

        i_cmd += 1

    return bot_cmds_with_loops


def get_bot_options() -> Tuple[Dict[int, str], Dict[str, int]]:
    bot_by_int = {i: v for i, v in enumerate(get_all_bot_names(), start=1)}
    bot_by_str = {v: k for k, v in bot_by_int.items()}
    return bot_by_int, bot_by_str


def is_valid_bots_file() -> bool:
    with open("example_forza_game_script.txt") as bots_file:
        re_valid_bots_file = f'(bot {re_bot_name}\n({re_cmd_name} [A-Za-z0-9 /_.]+\n?)*[\n]*)*'
        is_valid_format = re.fullmatch(re_valid_bots_file, bots_file.read()) is not None

        bot_names = get_all_bot_names()
        is_unique_bot_names = len(set(bot_names)) == len(bot_names)

        is_valid_syntax = True
        for bot_name in bot_names:
            bot_cmds = get_bot_commands(bot_name)
            is_valid_syntax = is_valid_looping(bot_cmds, is_valid_syntax)
            if not is_valid_syntax:
                break

        return is_valid_format and is_valid_syntax and is_unique_bot_names


def is_valid_looping(bot_cmds, is_valid) -> bool:
    loop_checker = {}
    loop_stack = []
    for bot_cmd in bot_cmds:
        if bot_cmd.cmd_name not in {cmd_loop_start, cmd_loop_end}:
            continue

        loop_id = bot_cmd.args[0]
        if bot_cmd.cmd_name == cmd_loop_start:
            loop_stack.append(loop_id)
            if loop_id in loop_checker:
                is_valid = False
                break
            else:
                loop_checker[loop_id] = False

            continue

        if bot_cmd.cmd_name == cmd_loop_end and len(loop_stack) > 0 and loop_stack[-1] == loop_id:
            if loop_id in loop_checker and not loop_checker[loop_id]:
                loop_checker[loop_id] = True
            else:
                is_valid = False
                break

            loop_stack.pop()
        else:
            is_valid = False
            break

    if len(loop_stack) != 0:
        is_valid = False

    return is_valid
