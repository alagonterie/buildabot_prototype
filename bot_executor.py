import datetime
import re
import time
import autoit
import pyautogui
import pydirectinput
from typing import List

import gmail
from helpers import get_bot_commands
from model_cmd import Cmd
import globals
from model_duration import Duration
from client_socket import log_message


def execute(bot_name: str) -> None:
    print(f'\nExecuting the "{bot_name}" bot commands ...')
    executed_message = f'"{bot_name}" commands executed successfully.'
    is_exception = False

    start_time = time.time()
    curr_cmd = None
    try:
        for i, cmd in enumerate(get_bot_commands(bot_name, unpack_loops=True), start=1):
            curr_cmd = i, cmd
            execute_cmd(cmd)

    except Exception as ex:
        is_exception = True
        i, cmd = curr_cmd
        executed_message = f'The "Command #{i} - {cmd}" of the "{bot_name}" bot failed: "{ex}".'

    finally:
        elapsed_time = time_convert(time.time() - start_time)
        log_message(f"Total time elapsed: {elapsed_time}.\n{executed_message}")

        subject = f"Bot \"{bot_name}\" {'failed' if is_exception else 'completed'} after {elapsed_time}"
        gmail.send_log(executed_message, subject)


def execute_cmd(cmd: Cmd) -> None:
    cmd_name = cmd.cmd_name
    if cmd_name == globals.cmd_sleep:
        execute_cmd_sleep(cmd.args)

    elif cmd_name == globals.cmd_press:
        execute_cmd_press(cmd.args)

    elif cmd_name == globals.cmd_multi_press:
        execute_cmd_multi_press(cmd.args)

    elif cmd_name == globals.cmd_keydown:
        execute_cmd_keydown(cmd.args)

    elif cmd_name == globals.cmd_keyup:
        execute_cmd_keyup(cmd.args)

    elif cmd_name == globals.cmd_hotkey:
        execute_cmd_hotkey(cmd.args)

    elif cmd_name == globals.cmd_ui_click:
        execute_cmd_image_click(cmd.args, is_ui=True)

    elif cmd_name == globals.cmd_image_click:
        execute_cmd_image_click(cmd.args)

    elif cmd_name == globals.cmd_image_multi_click:
        execute_cmd_image_multi_click(cmd.args)


def execute_cmd_sleep(args: List[str]) -> None:
    if args is None or len(args) != 1:
        raise Exception("one unit of time argument is required")

    duration = Duration(args[0])
    print_cmd(f"waiting for {duration}")
    time.sleep(duration.get_seconds())


def execute_cmd_press(args: List[str]) -> None:
    if args is None or len(args) != 1 or args[0] not in globals.key_set:
        raise Exception("one valid key argument is required")

    key = args[0]

    print_cmd(f"pressing the {key} key")
    pydirectinput.press(key)


def execute_cmd_multi_press(args: List[str]) -> None:
    if args is None or len(args) != 3 or args[0] not in globals.key_set or not args[1].isnumeric() or int(args[1]) <= 1:
        raise Exception("A valid key, number of presses greater than one, and interval time arguments are required")

    key = args[0]
    count_intervals = int(args[1])
    interval_duration = Duration(args[2])

    print_cmd(f"starting {count_intervals} presses of the {key} key with an interval of {interval_duration}")
    pydirectinput.press(key)

    for i_interval in range(count_intervals - 1):
        print_cmd(f"waiting for {interval_duration}")
        time.sleep(interval_duration.get_seconds())

        print_cmd(f"pressing the {key} key")
        pydirectinput.press(key)


def execute_cmd_hotkey(args: List[str]) -> None:
    if args is None or len(args) < 1 or not all([arg in globals.key_set for arg in args]):
        raise Exception("one or more valid key arguments are required")

    print_cmd(f"using the {'+'.join(args)} hotkey")
    use_hotkey(args)


def execute_cmd_keydown(args: List[str]) -> None:
    if args is None or len(args) != 1 or args[0] not in globals.key_set:
        raise Exception("one valid key argument is required")

    key = args[0]

    print_cmd(f"holding down the {key} key")
    pydirectinput.keyDown(key)


def execute_cmd_keyup(args: List[str]) -> None:
    if args is None or len(args) != 1 or args[0] not in globals.key_set:
        raise Exception("one valid key argument is required")

    key = args[0]

    print_cmd(f"releasing the {key} key")
    pydirectinput.keyUp(key)


def execute_cmd_image_click(args: List[str], is_ui=False) -> None:
    if args is None or len(args) != 2 or re.fullmatch(globals.re_file_path, args[0]) is None:
        raise Exception("a path argument for a provided image and timeout duration are required")

    img = args[0]
    img_path = f"bot_assets/{img}"
    timeout_duration = Duration(args[1])
    img_location = try_find_image(img_path)
    click_item = "image" if not is_ui else "ui element"

    if img_location is not None:
        print_cmd(f"clicking the {img} {click_item}")
        time.sleep(0.75)  # TODO: replace 0.75 with click delay config value
        click_found_image(img_location, is_ui)
        return

    print_cmd(f"waiting for at most {timeout_duration} to see the {img} {click_item}")
    wait_total_seconds = 0
    wait_increment_seconds = 250 / 1000  # TODO: replace 250 with reaction time config value
    while wait_total_seconds < timeout_duration.get_seconds() and img_location is None:
        start_time = time.time()
        img_location = try_find_image(img_path)
        img_find_seconds = time.time() - start_time

        wait_seconds = wait_increment_seconds - img_find_seconds
        if wait_seconds > 0:
            time.sleep(wait_seconds)

        wait_total_seconds += max(wait_increment_seconds, img_find_seconds)

    if img_location is None:
        raise pyautogui.ImageNotFoundException(f"{img} image not found before {timeout_duration} timeout.")

    print_cmd(f"clicking the {img} {click_item}")
    time.sleep(0.75)  # TODO: replace 0.75 with click delay config value
    click_found_image(img_location, is_ui)


def execute_cmd_image_multi_click(args: List[str]) -> None:
    if args is None or len(args) != 4 or not args[2].isnumeric() or int(args[2]) <= 1:
        raise Exception("the third argument must be a number greater than 1")

    img = args[0]
    count_clicks = args[2]
    single_click_args = args[:2:]
    count_intervals = int(count_clicks)
    interval_duration = Duration(args[3])

    print_cmd(f"starting {count_clicks} clicks on the {img} image with an interval of {interval_duration}")
    execute_cmd_image_click(single_click_args)

    for i_interval in range(count_intervals - 1):
        print_cmd(f"waiting for {interval_duration}")
        time.sleep(interval_duration.get_seconds())

        print_cmd(f"clicking the {img} image")
        click_at_mouse_location()


def click_found_image(img_location, is_ui=False):
    img_point = pyautogui.center(img_location)
    img_x, img_y = img_point
    pyautogui.moveTo(img_x, img_y)
    click_at_mouse_location(is_ui)


def click_at_mouse_location(is_ui=False):
    autoit.mouse_click()

    # clicking "harder" when done in a slower ui like in-game
    if is_ui:
        time.sleep(0.005)
        autoit.mouse_click()
        time.sleep(0.005)
        autoit.mouse_click()


def try_find_image(image_path: str):
    try:
        # TODO: replace 0.9 with vision accuracy config value
        img_location = pyautogui.locateOnScreen(image_path, confidence=0.9)
    except pyautogui.ImageNotFoundException:
        return None

    return img_location


def use_hotkey(keys: List[str]) -> None:
    for key in keys:
        if key == 'win':
            pyautogui.keyDown(key)
        else:
            pydirectinput.keyDown(key)
    for key in keys[::-1]:
        if key == 'win':
            pyautogui.keyUp(key)
        else:
            pydirectinput.keyUp(key)


def print_cmd(msg: str) -> None:
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%m-%d-%Y %H:%M:%S')
    print_str = f"[{timestamp}] >>> {msg}"
    log_message(print_str)


def time_convert(seconds: float) -> str:
    minutes = seconds // 60
    seconds %= 60
    hours = minutes // 60
    minutes %= 60
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
