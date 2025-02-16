"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

import pathlib
import shutil

import platformdirs
import strictyaml as sy

from logtools.log_patterns import LogPatterns
from logtools.utils import error_message


SCHEMA = sy.MapPattern(
    sy.Str(),  # name of the pattern file
    sy.Seq(sy.Str()),  # list of file globs
)


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


def get_exact_patterns(user_folder: pathlib.Path, patterns: str) -> LogPatterns:
    """
    When user provided a patterns file name then return that one.
    """
    if not patterns.lower().endswith(".yml"):
        patterns += ".yml"
    patterns_file = user_folder / patterns
    if not patterns_file.is_file():
        error_message(f"Pattern file {patterns} not found in {user_folder}")
    return LogPatterns(patterns_file)


def get_patterns_from_rules(
    user_folder: pathlib.Path, log_files: list[pathlib.Path]
) -> LogPatterns:
    """
    When user has multiple patterns files then select the right one based on rules.
    """
    rules_file = user_folder / "rules.yml"
    rules = sy.load(rules_file.read_text(), SCHEMA).data
    for patterns_file, globs in rules.items():
        for glob in globs:
            for log_file in log_files:
                if log_file.match(glob):
                    return LogPatterns(user_folder / patterns_file)
    error_message(f"No patterns file found for {log_files}")


def get_patterns(
    patterns: str | None, log_files: list[pathlib.Path], user_folder: pathlib.Path | None = None
) -> LogPatterns:
    """
    Get the pattern files matching the arguments
    """
    if user_folder is None:
        user_folder = get_or_create_user_folder()
    if patterns:
        return get_exact_patterns(user_folder, patterns)
    yaml_files = list(user_folder.glob("*.yml"))
    if not yaml_files:
        error_message(f"No pattern files found in {user_folder}")
    if len(yaml_files) == 1:
        yaml_file = yaml_files[0]
        if yaml_file.name == "rules.yml":
            error_message("Only rules.yml found, please create a patterns file")
        return LogPatterns(yaml_file)
    if "rules.yml" not in [y.name for y in yaml_files]:
        error_message("Multiple pattern files found, but no rules.yml")
    return get_patterns_from_rules(user_folder, log_files)
