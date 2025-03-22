@echo off
setlocal

REM Check if PYTHON_CMD is already set
if not defined PYTHON_CMD (
    REM Try python3 first
    where python3 >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set "PYTHON_CMD=python3"
    ) else (
        REM Try python if python3 not found
        where python >nul 2>&1
        if %ERRORLEVEL% EQU 0 (
            set "PYTHON_CMD=python"
        ) else (
            echo Python not found >&2
            exit /b 1
        )
    )
)

endlocal & set "PYTHON_CMD=%PYTHON_CMD%" 