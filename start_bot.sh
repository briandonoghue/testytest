#!/bin/bash

echo "🚀 Starting Trading Bot..."
# Activate the virtual environment (if used)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the bot
python main.py

echo "✅ Trading Bot Stopped."
