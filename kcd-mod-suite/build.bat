@echo off

REM Define paths and variables
set "UPX_DIR=..\resources\upx-4.2.4-win64"
set "ICON_PATH=.\kcd_mod_suite\resources\icon.ico"
set "OUTPUT_NAME=kcd-mod-suite-v0.1.1"
set "MAIN_PY=.\main.py"

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in the system path.
    if not defined CI pause
    exit /b 1
)
echo Python detected.

REM Check if pip is installed
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: pip is not installed or not in the system path.
    if not defined CI pause
    exit /b 1
)

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller not found.
    :prompt
    set "installPyInstaller="
    set /p installPyInstaller="PyInstaller is not installed. Would you like to install it now? (Y/N): "
    if /I "%installPyInstaller%"=="Y" goto pyinstaller
    if /I "%installPyInstaller%"=="N" goto abort
    echo Invalid input. Please enter Y or N.
    goto prompt
	
	:abort
    echo Installation aborted.
    if not defined CI pause
    exit /b 1

    :pyinstaller
    echo Attempting to install PyInstaller...
    pip install pyinstaller
    pyinstaller --version >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install PyInstaller. Please check your Python and pip setup.
        if not defined CI pause
        exit /b 1
    )
    echo PyInstaller successfully installed.
)
echo PyInstaller detected.

REM Validate main.py existence
if not exist "%MAIN_PY%" (
    echo Error: %MAIN_PY% not found.
    if not defined CI pause
    exit /b 1
)

REM Validate icon file existence
if not exist "%ICON_PATH%" (
    echo Error: Icon file %ICON_PATH% not found.
    if not defined CI pause
    exit /b 1
)

REM Run the PyInstaller command
pyinstaller ^
    --noupx ^
    -F --noconsole --clean ^
    -n %OUTPUT_NAME% ^
    --upx-dir=%UPX_DIR% ^
    --paths ..\kcd-mod-generator ^
    --paths ..\kcd-pak-builder ^
    --paths ..\kcd-asset-finder ^
    --paths ..\kcd-core ^
    --icon=%ICON_PATH% ^
    %MAIN_PY%
if %ERRORLEVEL% NEQ 0 (
    echo Error: PyInstaller compilation failed.
    if not defined CI pause
    exit /b 1
)

echo Compilation complete.
if not defined CI pause
exit /b 0