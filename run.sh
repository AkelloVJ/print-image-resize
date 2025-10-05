#!/bin/bash

# Print Image Resize Tool - Main Runner Script
# This script provides an easy way to run the image processing tool

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if Python 3 is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    print_success "Python 3 found: $(python3 --version)"
}

# Activate virtual environment
activate_venv() {
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        print_success "Virtual environment activated"
    else
        print_error "Virtual environment not found. Please run setup first."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed. Please install pip3 first."
        exit 1
    fi
    print_success "pip3 found"
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    if pip3 install -r requirements.txt; then
        print_success "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        exit 1
    fi
}

# Check if dependencies are installed
check_dependencies() {
    if ! python3 -c "import PIL" &> /dev/null; then
        print_warning "PIL (Pillow) not found. Installing dependencies..."
        install_dependencies
    else
        print_success "Dependencies are already installed"
    fi
}

# Main menu
show_menu() {
    echo
    echo "=========================================="
    echo "    Print Image Resize Tool"
    echo "=========================================="
    echo "1. Discover images (show what will be processed)"
    echo "2. Dry run (preview without processing)"
    echo "3. Process all images"
    echo "4. Process specific folder"
    echo "5. Process specific format"
    echo "6. Interactive mode"
    echo "7. Check folder statistics"
    echo "8. Cleanup destination folders"
    echo "9. Exit"
    echo "=========================================="
}

# Process user choice
process_choice() {
    read -p "Enter your choice (1-9): " choice
    
    case $choice in
        1)
            print_status "Discovering images..."
            python3 batch_processor.py --discover
            ;;
        2)
            print_status "Running dry run..."
            python3 batch_processor.py --dry-run
            ;;
        3)
            print_warning "This will process ALL images. Continue? (y/N)"
            read -p "> " confirm
            if [[ $confirm =~ ^[Yy]$ ]]; then
                print_status "Processing all images..."
                python3 batch_processor.py
            else
                print_status "Cancelled"
            fi
            ;;
        4)
            echo "Available folders:"
            python3 -c "
from folder_utils import FolderUtils
utils = FolderUtils()
stats = utils.get_folder_stats()
for folder_name, folder_stats in stats.items():
    print(f'  - {folder_name} ({folder_stats[\"image_count\"]} images)')
"
            read -p "Enter folder name: " folder_name
            if [ ! -z "$folder_name" ]; then
                print_status "Processing folder: $folder_name"
                python3 batch_processor.py --folder "$folder_name"
            else
                print_error "No folder name provided"
            fi
            ;;
        5)
            read -p "Enter format (e.g., .png, .jpg): " format
            if [ ! -z "$format" ]; then
                print_status "Processing format: $format"
                python3 batch_processor.py --format "$format"
            else
                print_error "No format provided"
            fi
            ;;
        6)
            print_status "Starting interactive mode..."
            python3 batch_processor.py --interactive
            ;;
        7)
            print_status "Checking folder statistics..."
            python3 folder_utils.py
            ;;
        8)
            print_warning "This will delete existing resized folders. Continue? (y/N)"
            read -p "> " confirm
            if [[ $confirm =~ ^[Yy]$ ]]; then
                python3 -c "
from folder_utils import FolderUtils
utils = FolderUtils()
utils.cleanup_destination_folders()
"
            else
                print_status "Cancelled"
            fi
            ;;
        9)
            print_status "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid choice. Please try again."
            ;;
    esac
}

# Main function
main() {
    print_status "Starting Print Image Resize Tool..."
    
    # Check prerequisites
    check_python
    check_pip
    activate_venv
    check_dependencies
    
    # Show menu and process choices
    while true; do
        show_menu
        process_choice
        echo
        read -p "Press Enter to continue..."
    done
}

# Run main function
main
