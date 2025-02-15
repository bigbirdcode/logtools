"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

import sys
from typing import NoReturn

import wx


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
