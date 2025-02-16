"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

import argparse
import io
import pathlib
import sys
from typing import Any

import wx

from logtools import user_files
from logtools.gui_main_frame import MainFrame
from logtools.log_data import LogData
from logtools.utils import error_message


FOLDER_HELP = """
    Patterns are Strict Yaml format files in the user folder with '.yml' extension.
    Providing the base name is enough for the selection. If patterns are not provided
    then LogTools will try to select the right pattern based on defined rules in the
    'rules.yml' file.
"""


def parse_arguments() -> Any:
    """
    Parse command line arguments and checks for errors

    Note: argparse do not handle well non-CLI usage
    the newly added exit_on_error=False parameter is buggy!
    it can also throw various types of exceptions...
    the only option is to redirect output and capture SystemExit
    ugly as hell, sorry
    """
    parser = argparse.ArgumentParser(
        description="Log file viewer.",
        epilog=FOLDER_HELP,
    )
    parser.add_argument("log_files", type=pathlib.Path, nargs="+", help="log files to display")
    parser.add_argument("-p", "--patterns", help="patterns file base name")
    args = None
    was_error = False
    bkp_stdout, bkp_stderr = sys.stdout, sys.stderr
    output = io.StringIO()
    sys.stdout, sys.stderr = output, output
    try:
        args = parser.parse_args()
    except (SystemExit, Exception):
        was_error = True
    finally:
        sys.stdout, sys.stderr = bkp_stdout, bkp_stderr
    if was_error:
        error_message(output.getvalue())
    return args


def check_logfiles(log_files: list[pathlib.Path]) -> None:
    """
    Check the log files
    """
    for log_file in log_files:
        if not log_file.is_file():
            error_message(f"{log_file} log file not found!")


def app_main() -> None:
    """
    Main function, starting point as usual
    """
    args = parse_arguments()
    check_logfiles(args.log_files)
    log_patterns = user_files.get_patterns(args.patterns, args.log_files)
    app_data = LogData(log_patterns, args.log_files)
    # Making GUI
    app = wx.App(0)
    frame = MainFrame(app_data)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()


def main() -> None:
    """
    The usual main function
    """
    try:
        app_main()
    except Exception as exc:  # noqa: BLE001 - blind exception
        error_message(str(exc))


if __name__ == "__main__":
    main()
