#!/usr/bin/env python3
"""
Fix folder structure - move processed images to main _resized folders
"""

import os
import shutil
from pathlib import Path
import config

def fix_folder_structure():
    """Move all processed images to the correct main _resized folders"""
    source_dir = Path(config.SOURCE_DIR)
    
    print("Fixing folder structure...")
    print(f"Source directory: {source_dir}")
    
    # Find all _resized folders
    resized_folders = []
    for root, dirs, files in os.walk(source_dir):
        for dir_name in dirs:
            if dir_name.endswith('_resized'):
                resized_folders.append(Path(root) / dir_name)
    
    print(f"Found {len(resized_folders)} _resized folders")
    
    # Process each _resized folder
    for resized_folder in resized_folders:
        print(f"\nProcessing: {resized_folder}")
        
        # Find the main category folder (parent of parent)
        main_category = resized_folder.parent.parent
        main_resized_folder = main_category / f"{main_category.name}_resized"
        
        # Create main resized folder if it doesn't exist
        main_resized_folder.mkdir(exist_ok=True)
        
        # Move all webp files from subfolder to main folder
        webp_files = list(resized_folder.glob("*.webp"))
        print(f"  Found {len(webp_files)} WebP files")
        
        for webp_file in webp_files:
            dest_file = main_resized_folder / webp_file.name
            print(f"  Moving: {webp_file.name}")
            shutil.move(str(webp_file), str(dest_file))
        
        # Remove empty subfolder
        try:
            resized_folder.rmdir()
            print(f"  Removed empty folder: {resized_folder}")
        except OSError:
            print(f"  Could not remove folder (not empty): {resized_folder}")
    
    print("\nFolder structure fix completed!")

if __name__ == "__main__":
    fix_folder_structure()
