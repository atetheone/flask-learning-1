#!/bin/bash

# Run tests with coverage reporting
python -m pytest --cov=src --cov-report=term-missing --cov-report=html

# Open coverage report in browser (works on macOS and Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open htmlcov/index.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open htmlcov/index.html
else
    echo "Coverage report generated at htmlcov/index.html"
fi