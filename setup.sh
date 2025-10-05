#!/bin/bash

# Setup script for Print Image Resize Tool
# This script sets up the virtual environment and installs dependencies

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Setting up Print Image Resize Tool..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi
print_success "Python 3 found: $(python3 --version)"

# Check if virtual environment already exists
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv venv
print_success "Virtual environment created"

# Activate virtual environment and install dependencies
print_status "Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
print_success "Dependencies installed"

# Make scripts executable
print_status "Making scripts executable..."
chmod +x *.py
chmod +x *.sh
print_success "Scripts made executable"

# Test the setup
print_status "Testing setup..."
python3 batch_processor.py --discover > /dev/null
if [ $? -eq 0 ]; then
    print_success "Setup test passed!"
else
    print_error "Setup test failed!"
    exit 1
fi

echo
print_success "Setup completed successfully!"
echo
echo "You can now run the tool using:"
echo "  ./run.sh"
echo
echo "Or directly with:"
echo "  source venv/bin/activate && python3 batch_processor.py --discover"
