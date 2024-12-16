@ECHO OFF
SET CHECK_FAILURE=False

ruff format --check .
IF %ERRORLEVEL% NEQ 0 (SET CHECK_FAILURE=True)

ruff check .
IF %ERRORLEVEL% NEQ 0 (SET CHECK_FAILURE=True)

mypy .
IF %ERRORLEVEL% NEQ 0 (SET CHECK_FAILURE=True)

IF %CHECK_FAILURE% == True (
ECHO.
ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ECHO ! WARNING  Problems detected in code!  WARNING !
ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
EXIT /B 1
)
ECHO.
ECHO ALL OK :-)
