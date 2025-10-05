#!/usr/bin/env python3
"""
Utility functions for folder structure management and image discovery
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple
import config

class FolderUtils:
    def __init__(self):
        self.source_dir = Path(config.SOURCE_DIR)
        
    def discover_images(self) -> Dict[str, List[Path]]:
        """Discover all images in the source directory structure"""
        images_by_folder = {}
        
        if not self.source_dir.exists():
            print(f"Source directory does not exist: {self.source_dir}")
            return images_by_folder
        
        for root, dirs, files in os.walk(self.source_dir):
            folder_path = Path(root)
            folder_name = folder_path.name
            
            # Find all image files in this folder
            image_files = []
            for file in files:
                file_path = folder_path / file
                if file_path.suffix.lower() in config.SUPPORTED_FORMATS:
                    image_files.append(file_path)
            
            if image_files:
                images_by_folder[folder_name] = image_files
        
        return images_by_folder
    
    def get_folder_stats(self) -> Dict[str, Dict]:
        """Get statistics about folders and images"""
        stats = {}
        images_by_folder = self.discover_images()
        
        for folder_name, image_files in images_by_folder.items():
            folder_stats = {
                'image_count': len(image_files),
                'formats': {},
                'total_size': 0,
                'files': []
            }
            
            for image_file in image_files:
                # Get file size
                try:
                    file_size = image_file.stat().st_size
                    folder_stats['total_size'] += file_size
                except OSError:
                    file_size = 0
                
                # Count formats
                ext = image_file.suffix.lower()
                folder_stats['formats'][ext] = folder_stats['formats'].get(ext, 0) + 1
                
                # Store file info
                folder_stats['files'].append({
                    'name': image_file.name,
                    'size': file_size,
                    'format': ext
                })
            
            stats[folder_name] = folder_stats
        
        return stats
    
    def print_discovery_report(self) -> None:
        """Print a detailed report of discovered images"""
        stats = self.get_folder_stats()
        
        print("=" * 80)
        print("IMAGE DISCOVERY REPORT")
        print("=" * 80)
        print(f"Source Directory: {self.source_dir}")
        print()
        
        total_images = 0
        total_size = 0
        
        for folder_name, folder_stats in stats.items():
            print(f"📁 {folder_name}")
            print(f"   Images: {folder_stats['image_count']}")
            print(f"   Size: {self.format_size(folder_stats['total_size'])}")
            print(f"   Formats: {', '.join(folder_stats['formats'].keys())}")
            
            # Show format breakdown
            for format_name, count in folder_stats['formats'].items():
                print(f"     {format_name}: {count} files")
            
            print()
            total_images += folder_stats['image_count']
            total_size += folder_stats['total_size']
        
        print("=" * 80)
        print(f"TOTAL: {total_images} images, {self.format_size(total_size)}")
        print("=" * 80)
    
    def format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def check_destination_folders(self) -> List[Path]:
        """Check which destination folders already exist"""
        existing_destinations = []
        
        for item in self.source_dir.iterdir():
            if item.is_dir():
                dest_folder = item.parent / f"{item.name}{config.DESTINATION_SUFFIX}"
                if dest_folder.exists():
                    existing_destinations.append(dest_folder)
        
        return existing_destinations
    
    def cleanup_destination_folders(self) -> None:
        """Remove existing destination folders (use with caution!)"""
        existing = self.check_destination_folders()
        
        if not existing:
            print("No destination folders found to clean up.")
            return
        
        print(f"Found {len(existing)} existing destination folders:")
        for folder in existing:
            print(f"  - {folder}")
        
        response = input("\nDo you want to delete these folders? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            for folder in existing:
                import shutil
                shutil.rmtree(folder)
                print(f"Deleted: {folder}")
        else:
            print("Cleanup cancelled.")

def main():
    """Main function for utility operations"""
    utils = FolderUtils()
    
    print("Image Processing Utility")
    print("1. Discover images")
    print("2. Show folder statistics")
    print("3. Check destination folders")
    print("4. Cleanup destination folders")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        utils.print_discovery_report()
    elif choice == "2":
        utils.print_discovery_report()
    elif choice == "3":
        existing = utils.check_destination_folders()
        if existing:
            print("Existing destination folders:")
            for folder in existing:
                print(f"  - {folder}")
        else:
            print("No existing destination folders found.")
    elif choice == "4":
        utils.cleanup_destination_folders()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
