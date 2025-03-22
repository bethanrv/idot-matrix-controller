@echo off
setlocal

REM Get the directory of the batch file
set "IDO_DIR=%~dp0"
set "IDO_DIR=%IDO_DIR:~0,-1%"

REM Call find_cmds.bat to set PYTHON_CMD
call "%IDO_DIR%\find_cmds.bat"

REM Create venv
"%PYTHON_CMD%" -m venv "%IDO_DIR%\venv"

REM Enable venv
call "%IDO_DIR%\venv\Scripts\activate.bat"

REM Install dependencies from pyproject.toml
"%PYTHON_CMD%" -m pip install "%IDO_DIR%"

endlocal 