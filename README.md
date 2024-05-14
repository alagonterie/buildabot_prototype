# Build-a-Bot Prototype

This application is a simple bot builder, intended to provide an interface for users to craft and execute custom bot scripts. The program can handle numerous operations such as key presses, managing windows, handling delays, and more.

## Features

* Run: Allows you to run pre-created bots.
* Editor: Lets you manage your bots with further options like:
    * View: Examine bot details.
    * Create: Set up a new bot.
    * Delete: Remove an existing bot.

## Code Overview

The program runs with a command-line interface, facilitated by Python. The application's functionality as explained above is spread across numerous Python scripts. A brief overview of these scripts is provided below:

* `main.py`: Serves as the application entry point, initiating the whole system.

* `menu_app_start.py`, `menu_bot_runner.py`, `menu_bot_editor.py`, and other "menu_" scripts: Handle the user interface of the application and manage options that users can select.

* `helpers.py`: Accommodates helper methods used across the application like getting all bot names, checking file validity, validating loops, etc.

* 'model_' scripts (i.e., `model_cmd.py`, `model_duration.py`, `model_index_and_count.py`): Represent the model layer of the application where bot commands, duration, and index-count handling is programmed.

* `bot_executor.py`: Manages bot execution functionality, including commands like keypress, sleep, looping, etc.

* `client_socket.py`: Manages socket connection with server for logging.

* `globals.py`: All global constants are placed here.

* `gmail.py`: Facilitates emailing logs.

## Frameworks and Libraries

The bot utilizes several powerful Python libraries to support various functionalities:

* `pyautogui`: A module used for programmatically controlling the mouse and keyboard.
* `socketio.Client`: Manages socket connection with a server.
* `googleapiclient`: Facilitates emailing logs.

## Installation

Before first-time usage, make sure the application has access to your system's mouse and keyboard control. Please note, depending on your Operating System, you might need to allow accessibility controls for the terminal in which you are running the scripts. 

With Python installed, you can install all required libraries with pip:

```shell
pip install pyautogui python-socketio google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client gmail
```