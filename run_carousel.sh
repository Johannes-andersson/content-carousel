#!/bin/zsh

PROJECT="/Users/johan/Documents/Claude/Code-projects/carousel-generator"
cd "$PROJECT"

source venv/bin/activate
python carousel.py
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "--- Script exited with an error (code $EXIT_CODE) ---"
    echo "Press any key to close this window."
    read -k 1
fi

# Close the Terminal window cleanly on success (or after error is acknowledged)
osascript -e 'tell application "Terminal" to close front window' 2>/dev/null
