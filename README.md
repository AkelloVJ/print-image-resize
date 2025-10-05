# Print Image Resize Tool

A robust Python-based image processing tool that automatically resizes and converts images from your print pictures folder to WebP format, organized by folder structure with renamed files.

## Features

- **Multi-format Support**: Handles JPG, PNG, BMP, TIFF, GIF, WebP, ICO, and more
- **Automatic Resizing**: Maintains aspect ratio while resizing to optimal dimensions
- **WebP Conversion**: Converts all images to WebP format for better compression
- **Folder-based Organization**: Creates resized folders with `_resized` suffix
- **Smart Naming**: Renames files based on folder names for better organization
- **Batch Processing**: Process all folders or specific folders
- **Dry Run Mode**: Preview what will be processed without making changes
- **Comprehensive Logging**: Detailed logs of all processing activities

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Make scripts executable:
```bash
chmod +x *.py
```

## Configuration

Edit `config.py` to customize settings:

- `SOURCE_DIR`: Path to your print pictures folder
- `TARGET_FORMAT`: Output format (default: WEBP)
- `QUALITY`: WebP quality (1-100, default: 85)
- `MAX_WIDTH`/`MAX_HEIGHT`: Maximum dimensions for resizing
- `FOLDER_NAME_MAPPING`: Custom folder name mappings

## Usage

### Quick Start

Process all images in all folders:
```bash
python3 batch_processor.py
```

### Interactive Mode

For guided processing:
```bash
python3 batch_processor.py --interactive
```

### Discover Images

See what images will be processed:
```bash
python3 batch_processor.py --discover
```

### Dry Run

Preview processing without making changes:
```bash
python3 batch_processor.py --dry-run
```

### Process Specific Folder

Process only a specific folder:
```bash
python3 batch_processor.py --folder "business cards"
```

### Process Specific Format

Process only certain file types:
```bash
python3 batch_processor.py --format .png
```

### Utility Functions

Check folder statistics and manage destination folders:
```bash
python3 folder_utils.py
```

## File Organization

### Input Structure
```
print pictures/
├── business cards/
│   ├── standard business cards/
│   │   ├── image1.png
│   │   └── image2.jpg
│   └── folded business cards/
│       └── image3.png
└── banners and large formats/
    └── backdrop banners/
        └── image4.png
```

### Output Structure
```
print pictures/
├── business cards/
├── business cards_resized/
│   ├── business_cards_image1.webp
│   └── business_cards_image2.webp
├── business cards/folded business cards/
├── business cards/folded business cards_resized/
│   └── business_cards_folded_business_cards_image3.webp
├── banners and large formats/
├── banners and large formats_resized/
└── banners and large formats/backdrop banners/
    └── backdrop banners_resized/
        └── banners_backdrop_banners_image4.webp
```

## Scripts Overview

- **`image_processor.py`**: Core image processing functionality
- **`batch_processor.py`**: Main script for batch processing with various options
- **`folder_utils.py`**: Utility functions for folder management and discovery
- **`config.py`**: Configuration settings
- **`requirements.txt`**: Python dependencies

## Processing Details

### Image Processing
- Automatically detects image format
- Maintains aspect ratio during resizing
- Converts RGBA/LA/P mode images to RGB with white background
- Optimizes WebP output for best compression

### File Naming
- Files are renamed based on their folder hierarchy
- Example: `business cards/standard business cards/image.png` → `business_cards_standard_business_cards_image.webp`
- Special characters are replaced with underscores

### Error Handling
- Comprehensive error logging
- Continues processing even if individual files fail
- Detailed error reports in log files

## Logging

All processing activities are logged to:
- Console output (real-time)
- `image_processing.log` file (detailed logs)

## Examples

### Process All Images
```bash
python3 batch_processor.py
```

### Check What Will Be Processed
```bash
python3 batch_processor.py --discover
```

### Process Only Business Cards
```bash
python3 batch_processor.py --folder "business cards"
```

### Process Only PNG Files
```bash
python3 batch_processor.py --format .png
```

### Interactive Mode
```bash
python3 batch_processor.py --interactive
```

## Troubleshooting

1. **Permission Errors**: Ensure you have write permissions to the destination folders
2. **Memory Issues**: For very large images, consider reducing `MAX_WIDTH` and `MAX_HEIGHT` in config
3. **Format Not Supported**: Check that the image format is in `SUPPORTED_FORMATS` in config.py
4. **Path Issues**: Verify the `SOURCE_DIR` path in config.py is correct

## Customization

### Adding New Image Formats
Edit `config.py` and add the format to `SUPPORTED_FORMATS`:
```python
SUPPORTED_FORMATS = {
    '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', 
    '.gif', '.webp', '.ico', '.ppm', '.pgm', '.pbm',
    '.your_format'  # Add new format here
}
```

### Changing Output Quality
Modify the `QUALITY` setting in `config.py`:
```python
QUALITY = 90  # Higher quality (larger files)
```

### Custom Folder Mappings
Update `FOLDER_NAME_MAPPING` in `config.py`:
```python
FOLDER_NAME_MAPPING = {
    "your folder name": "your_mapped_name",
    # Add more mappings
}
```