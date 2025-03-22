@echo off
setlocal

REM Get the directory of the batch file
set "IDO_DIR=%~dp0"
set "IDO_DIR=%IDO_DIR:~0,-1%"

REM Activate venv
call "%IDO_DIR%\venv\Scripts\activate.bat"

REM Call find_cmds.bat to set PYTHON_CMD
call "%IDO_DIR%\find_cmds.bat"

REM Run app with all arguments passed through
"%PYTHON_CMD%" "%IDO_DIR%\app.py" %*

endlocal 