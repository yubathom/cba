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
$PYTHON_CMD process.py

# Open the output directory in the browser
npx http-server ./output -o -p 8080


