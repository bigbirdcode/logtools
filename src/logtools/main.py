"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

import argparse
import io
import pathlib
import shutil
import sys
from textwrap import dedent
from typing import Any, NoReturn

import platformdirs
import wx

from logtools.gui_main_frame import MainFrame
from logtools.log_data import LogData
from logtools.log_patterns import LogPatterns


FOLDER_HELP = """
    Patterns are Strict Yaml format files in the user folder with .YML extension.
    Providing the base name is enough for the selection. If pattern is not provided
    then LogTools will try to select the right pattern based on some heuristics,
    or just use the default one.
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


def get_or_create_user_folder() -> pathlib.Path:
    """
    Return the user configuration folder or create one when not found.

    If the folder is empty then function will also copy the sample files there.
    To avoid this behavior, leave at least a placeholder file there,
    for example the 'logtools.txt' file.
    """
    folder = platformdirs.user_data_dir(appname="logtools", appauthor=False, roaming=True)
    folder_path = pathlib.Path(folder)
    try:
        folder_path.mkdir(parents=True, exist_ok=True)
    except OSError:
        msg = f"Cannot create user folder {folder_path}"
        error_message(msg)
    if not any(folder_path.iterdir()):
        # folder is empty
        samples = pathlib.Path(__file__).parent / "samples"
        assert samples.is_dir(), f"Cannot found samples folder {samples}"
        for f in samples.iterdir():
            shutil.copy(f, folder_path)
    return folder_path


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
    parser.add_argument("-p", "--pattern", help="pattern base name")
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


def get_patterns(args: Any) -> list[pathlib.Path]:
    """
    Get the pattern files matching the arguments
    """
    user_folder = get_or_create_user_folder()
    if args.pattern:
        pattern = args.pattern
        if not pattern.lower().endswith(".yml"):
            pattern += ".yml"
    else:
        pattern = "*.yml"
    pattern_files = list(user_folder.glob(pattern))
    if not pattern_files:
        error_message(f"Pattern file {pattern} not found in {user_folder}")
    return pattern_files


def read_patterns(patterns: list[pathlib.Path]) -> LogPatterns:
    """
    Locate and check the pattern file
    """
    # TODO: here there should be some heuristics instead
    pattern_file = patterns[0]
    log_patterns = LogPatterns(pattern_file)
    return log_patterns


def app_main() -> None:
    """
    Main function, starting point as usual
    """
    args = parse_arguments()
    check_logfiles(args.log_files)
    patterns = get_patterns(args)
    log_patterns = read_patterns(patterns)
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
