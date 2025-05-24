#!/bin/bash

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

# Find pip for the selected Python
if command -v pip3 &> /dev/null && $PYTHON_CMD -m pip --version &> /dev/null; then
    PIP_CMD=pip3
elif command -v pip &> /dev/null && $PYTHON_CMD -m pip --version &> /dev/null; then
    PIP_CMD=pip
else
    echo "Error: pip for Python 3 is not installed!"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix-like (macOS/Linux)
    source venv/bin/activate
fi

# Install required packages
echo "Installing required packages..."
$PIP_CMD install pandas numpy openpyxl

echo "Setup completed successfully!"
echo "Run 'bash start.sh' to run and preview the processed data."

