#!/bin/bash

# Remove virtual environment if it exists
if [ -d "venv" ]; then
    echo "Removing virtual environment..."
    rm -rf venv
fi

# Remove output/*.csv files
if [ -d "output" ]; then
    echo "Removing output/*.csv files..."
    rm -rf output/*.csv
fi

# Remove any Python cache files
echo "Cleaning Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

echo "Reset completed successfully!"
echo "You may now re-run 'python3 scripts/process.py' to regenerate output."
