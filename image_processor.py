#!/usr/bin/env python3
"""
Robust Image Processing Script
Processes images from print pictures folder, resizes them, and converts to WebP format
"""

import os
import sys
import logging
from pathlib import Path
from PIL import Image, ImageOps
from typing import List, Tuple, Optional
import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.source_dir = Path(config.SOURCE_DIR)
        self.processed_count = 0
        self.error_count = 0
        self.supported_formats = config.SUPPORTED_FORMATS
        
    def is_image_file(self, file_path: Path) -> bool:
        """Check if file is a supported image format"""
        return file_path.suffix.lower() in self.supported_formats
    
    def get_image_info(self, image_path: Path) -> Optional[Tuple[int, int, str]]:
        """Get image dimensions and format"""
        try:
            with Image.open(image_path) as img:
                return img.size[0], img.size[1], img.format
        except Exception as e:
            logger.error(f"Error reading image {image_path}: {e}")
            return None
    
    def calculate_new_dimensions(self, width: int, height: int) -> Tuple[int, int]:
        """Calculate new dimensions maintaining aspect ratio"""
        if width <= config.MAX_WIDTH and height <= config.MAX_HEIGHT:
            return width, height
            
        # Calculate scaling factor
        width_ratio = config.MAX_WIDTH / width
        height_ratio = config.MAX_HEIGHT / height
        scale_factor = min(width_ratio, height_ratio)
        
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        return new_width, new_height
    
    def process_image(self, source_path: Path, dest_path: Path) -> bool:
        """Process a single image: resize and convert to WebP"""
        try:
            logger.info(f"Processing: {source_path.name}")
            
            # Get original image info
            img_info = self.get_image_info(source_path)
            if not img_info:
                return False
                
            width, height, format_name = img_info
            logger.info(f"Original: {width}x{height} ({format_name})")
            
            # Open and process image
            with Image.open(source_path) as img:
                # Convert RGBA to RGB if necessary for WebP
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Calculate new dimensions
                new_width, new_height = self.calculate_new_dimensions(width, height)
                logger.info(f"Resizing to: {new_width}x{new_height}")
                
                # Resize image
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Ensure destination directory exists
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save as WebP
                resized_img.save(
                    dest_path,
                    format='WEBP',
                    quality=config.QUALITY,
                    optimize=True
                )
                
                logger.info(f"Saved: {dest_path}")
                return True
                
        except Exception as e:
            logger.error(f"Error processing {source_path}: {e}")
            return False
    
    def get_folder_name_mapping(self, folder_name: str) -> str:
        """Get mapped folder name for renaming"""
        return config.FOLDER_NAME_MAPPING.get(folder_name, folder_name.replace(" ", "_").lower())
    
    def process_folder(self, folder_path: Path) -> None:
        """Process all images in a folder"""
        folder_name = folder_path.name
        mapped_name = self.get_folder_name_mapping(folder_name)
        
        logger.info(f"Processing folder: {folder_name} -> {mapped_name}")
        
        # Create destination folder
        dest_folder = folder_path.parent / f"{folder_name}{config.DESTINATION_SUFFIX}"
        dest_folder.mkdir(exist_ok=True)
        
        # Process all images in the folder
        for file_path in folder_path.iterdir():
            if file_path.is_file() and self.is_image_file(file_path):
                # Create new filename with folder name prefix
                new_filename = f"{mapped_name}_{file_path.stem}.webp"
                dest_path = dest_folder / new_filename
                
                if self.process_image(file_path, dest_path):
                    self.processed_count += 1
                else:
                    self.error_count += 1
            elif file_path.is_dir():
                # Recursively process subdirectories
                self.process_folder(file_path)
    
    def process_all_folders(self) -> None:
        """Process all folders in the source directory"""
        if not self.source_dir.exists():
            logger.error(f"Source directory does not exist: {self.source_dir}")
            return
        
        logger.info(f"Starting image processing from: {self.source_dir}")
        
        # Process each main folder
        for item in self.source_dir.iterdir():
            if item.is_dir():
                self.process_folder(item)
        
        logger.info(f"Processing complete!")
        logger.info(f"Successfully processed: {self.processed_count} images")
        logger.info(f"Errors encountered: {self.error_count} images")

def main():
    """Main function"""
    processor = ImageProcessor()
    processor.process_all_folders()

if __name__ == "__main__":
    main()
