#!/bin/bash
# Setup script for General Conference PDF Generator

echo "=================================="
echo "General Conference PDF Generator"
echo "Setup Script"
echo "=================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Error installing dependencies"
    exit 1
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "To use the script:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the script (note the quotes around the URL):"
echo "     python generate_conference_pdf.py \"<conference_url>\""
echo ""
echo "Example:"
echo "  python generate_conference_pdf.py \"https://www.churchofjesuschrist.org/study/general-conference/2025/04?lang=eng\""
echo ""
echo "IMPORTANT: Always wrap the URL in quotes!"
echo ""

