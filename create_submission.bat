@echo off
REM Script to create submission zip file for Windows
REM Usage: create_submission.bat your_name

if "%1"=="" (
    echo Usage: create_submission.bat your_name
    echo Example: create_submission.bat john_doe
    exit /b 1
)

set NAME=%1
set ZIP_NAME=%NAME%_binance_bot.zip

echo Creating submission package: %ZIP_NAME%
echo ================================

echo Checking required files...

if not exist "src\cli.py" (
    echo Missing: src\cli.py
    exit /b 1
)
if not exist "src\market_orders.py" (
    echo Missing: src\market_orders.py
    exit /b 1
)
if not exist "bot.log" (
    echo Missing: bot.log
    exit /b 1
)
if not exist "README.md" (
    echo Missing: README.md
    exit /b 1
)

echo All required files found!

if not exist "report.pdf" (
    echo WARNING: report.pdf not found!
    echo You need to create report.pdf before submission.
    pause
)

echo.
echo Creating zip file...
echo Please use a zip tool to create: %ZIP_NAME%
echo.
echo Include these folders/files:
echo - src/
echo - bot.log
echo - README.md
echo - requirements.txt
echo - report.pdf
echo.
echo ================================
pause
