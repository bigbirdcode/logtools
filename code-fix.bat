@ECHO OFF
REM https://docs.astral.sh/ruff/formatter/#sorting-imports
ruff check --select I --fix .
ruff format .
