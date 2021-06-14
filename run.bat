IF "%~1"=="" (
    ECHO Please give a log file to display
    EXIT /B 1
    )

python -m logtools "%~1"
