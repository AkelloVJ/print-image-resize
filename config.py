"""
Configuration file for image processing
"""
import os

# Source and destination paths
SOURCE_DIR = "/home/victor/Music/print pictures"
DESTINATION_SUFFIX = "_resized"

# Image processing settings
TARGET_FORMAT = "WEBP"
QUALITY = 85
MAX_WIDTH = 1920
MAX_HEIGHT = 1080

# Supported image formats
SUPPORTED_FORMATS = {
    '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', 
    '.gif', '.webp', '.ico', '.ppm', '.pgm', '.pbm'
}

# File naming patterns
FOLDER_NAME_MAPPING = {
    "banners and large formats": "banners",
    "business cards": "business_cards", 
    "marketing and promotional materials": "marketing",
    "photo and speciality": "photo_specialty",
    "promotional products and giveaways": "promotional",
    "stickers and labels": "stickers"
}

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FILE = "image_processing.log"
