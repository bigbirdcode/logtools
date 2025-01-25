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
from textwrap import dedent
from typing import Any, NoReturn

import wx

from logtools.gui_main_frame import MainFrame
from logtools.log_data import LogData
from logtools.log_patterns import LogPatterns


DEFAULT_PATTERNS_YML = "logtools_default_patterns.yml"

FOLDER_HELP = """
    If pattern_file is not provided then logtools will try to read the file
    'logtools_default_patterns.yml' from the following possible locations:
    1. actual folder 2. user's home folder 3. user's Documents folder
"""


def error_message(msg: str) -> NoReturn:
    """
    Print out error messages either to the console or to a dialog box then exit

    When there is a problem in argparse parameters or provided files do not exist
    then we can still show these to the user however the app was  started.
    """
    if sys.executable.endswith("pythonw.exe"):
        app = wx.App()
        dlg = wx.MessageDialog(None, msg, "LogTools Error", wx.OK | wx.ICON_ERROR)
        dlg.Center()
        dlg.ShowModal()
        dlg.Destroy()
        app.Destroy()
    else:
        print(msg)  # noqa: T201 - print ok here
    sys.exit(1)


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
    parser.add_argument(
        "-p", "--pattern_file", type=pathlib.Path, help="pattern file in strict YAML format"
    )
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


def read_patterns(args: Any) -> LogPatterns:
    """
    Locate and check the pattern file
    """
    pattern_file = pathlib.Path(DEFAULT_PATTERNS_YML)  # initial value, it will be overwritten
    if args.pattern_file:
        pattern_file = args.pattern_file
        if not pattern_file.is_file():
            error_message(f"{pattern_file} pattern file not found!")
    else:
        default_pattern_file = pattern_file
        if default_pattern_file.is_file():
            pattern_file = default_pattern_file
        elif (pathlib.Path.home() / default_pattern_file).is_file():
            pattern_file = pathlib.Path.home() / default_pattern_file
        elif (pathlib.Path.home() / "Documents" / default_pattern_file).is_file():
            pattern_file = pathlib.Path.home() / "Documents" / default_pattern_file
        else:
            error_message("Pattern file not found!\n" + dedent(FOLDER_HELP))
    log_patterns = LogPatterns(pattern_file)
    return log_patterns


def app_main() -> None:
    """
    Main function, starting point as usual
    """
    args = parse_arguments()
    check_logfiles(args.log_files)
    log_patterns = read_patterns(args)
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
        error_message(repr(exc))


if __name__ == "__main__":
    main()
