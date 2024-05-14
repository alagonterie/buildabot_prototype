from typing import Dict

run_str: str = "Run"
editor_str: str = "Editor"

view_str: str = "View"
create_str: str = "Create"
delete_str: str = "Delete"

yes_str: str = "Yes"

quit_str: str = "Quit"
back_str: str = "Go Back"
quit_option: int = 0

cmd_bot = "bot"
cmd_sleep = "sleep"
cmd_press = "press"
cmd_multi_press = "pressmulti"
cmd_keydown = "keydown"
cmd_keyup = "keyup"
cmd_hotkey = "hotkey"
cmd_loop_start = "loopstart"
cmd_loop_end = "loopend"
cmd_ui_click = "ui"
cmd_image_click = "img"
cmd_image_multi_click = "imgmulti"

cmd_set = {
    cmd_bot,
    cmd_sleep,
    cmd_press,
    cmd_multi_press,
    cmd_keydown,
    cmd_keyup,
    cmd_hotkey,
    cmd_loop_start,
    cmd_loop_end,
    cmd_ui_click,
    cmd_image_click,
    cmd_image_multi_click
}

key_set = {
    '\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
    ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
    'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
    'browserback', 'browserfavorites', 'browserforward', 'browserhome',
    'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
    'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
    'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
    'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
    'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
    'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
    'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
    'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
    'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
    'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
    'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
    'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
    'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
    'command', 'option', 'optionleft', 'optionright'
}

re_bot_name = "[A-Za-z0-9 /_.]+"
re_cmd_name = f"({'|'.join([f'({cmd})' for cmd in cmd_set])})"
re_file_path = "([^<>:\"|?*/]+/?)+.[A-Za-z0-9]+"

start_options: Dict[str, int] = {run_str: 1, editor_str: 2}
editor_options: Dict[str, int] = {view_str: 1, create_str: 2, delete_str: 3}

confirm_options: Dict[str, int] = {yes_str: 1}
