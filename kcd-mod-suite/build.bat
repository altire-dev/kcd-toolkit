@echo off

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in the system path.
    pause
    exit /b 1
)

echo Python detected.

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: PyInstaller is not installed.
    echo You can install it using the command: pip install pyinstaller
    pause
    exit /b 1
)

echo PyInstaller detected.

REM Run the PyInstaller command
pyinstaller ^
    --noupx ^
    -F --noconsole --clean ^
    -n kcd-mod-suite-v0.1.1 ^
    --upx-dir=..\resources\upx-4.2.4-win64 ^
    --paths ..\kcd-mod-generator ^
    --paths ..\kcd-pak-builder ^
    --paths ..\kcd-asset-finder ^
    --paths ..\kcd-core ^
    --icon=.\kcd_mod_suite\resources\icon.ico ^
    .\main.py

echo Compilation complete.
pause
