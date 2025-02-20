@echo off
echo 🚀 Starting Trading Bot...

:: Activate the virtual environment (if used)
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

:: Run the bot
python C:\TradingBot\core\main.py

echo ✅ Trading Bot Stopped.
pause
