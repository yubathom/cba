# Check if venv exists and activate it
if [ -d "venv" ]; then
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        source venv/Scripts/activate
    else
        # Unix-like (macOS/Linux)
        source venv/bin/activate
    fi
else
    echo "Error: Python virtual environment (venv) not found!"
    echo "Run 'bash setup.sh' to create the virtual environment."
    exit 1
fi

# Find Python 3 interpreter
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python 3 is not installed!"
    exit 1
fi

# Check Python version is 3.x
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(sys.version_info[0])')
if [ "$PYTHON_VERSION" != "3" ]; then
    echo "Error: Python 3 is required! Found $($PYTHON_CMD --version)"
    exit 1
fi

# Run the Python script
$PYTHON_CMD scripts/process.py

# Open a new terminal and activate virtual environment
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate && echo \"Available Python scripts:\" && echo *.py"'
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd '$(pwd)' && source venv/bin/activate; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -e "cd '$(pwd)' && source venv/bin/activate; exec bash" &
    else
        echo "Warning: Could not open new terminal. Please manually activate the virtual environment."
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    start cmd.exe /k "cd /d '$(pwd)' && venv\Scripts\activate"
else
    echo "Warning: Unsupported OS. Please manually activate the virtual environment."
fi


# Check if npx is installed
if ! command -v npx &> /dev/null; then
    echo "Error: npx is not installed!"
    exit 1
fi

# Open the output directory in the browser
npx http-server ./output -o -p 8080


