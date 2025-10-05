#!/usr/bin/env python3
"""
Batch processing script for all image folders
Provides different processing modes and options
"""

import sys
import argparse
from pathlib import Path
from image_processor import ImageProcessor
from folder_utils import FolderUtils
import config

class BatchProcessor:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.folder_utils = FolderUtils()
    
    def process_single_folder(self, folder_name: str) -> None:
        """Process a single folder by name"""
        source_path = Path(config.SOURCE_DIR) / folder_name
        
        if not source_path.exists():
            print(f"Folder not found: {folder_name}")
            return
        
        print(f"Processing single folder: {folder_name}")
        self.image_processor.process_folder(source_path)
    
    def process_all_folders(self) -> None:
        """Process all folders in the source directory"""
        print("Processing all folders...")
        self.image_processor.process_all_folders()
    
    def process_by_format(self, format_ext: str) -> None:
        """Process only images of a specific format"""
        print(f"Processing only {format_ext} files...")
        
        # Override the supported formats temporarily
        original_formats = self.image_processor.supported_formats
        self.image_processor.supported_formats = {format_ext.lower()}
        
        try:
            self.image_processor.process_all_folders()
        finally:
            # Restore original formats
            self.image_processor.supported_formats = original_formats
    
    def dry_run(self) -> None:
        """Show what would be processed without actually processing"""
        print("DRY RUN - No files will be modified")
        print("=" * 50)
        
        stats = self.folder_utils.get_folder_stats()
        total_images = 0
        
        for folder_name, folder_stats in stats.items():
            print(f"📁 {folder_name}")
            print(f"   Would process: {folder_stats['image_count']} images")
            print(f"   Formats: {', '.join(folder_stats['formats'].keys())}")
            
            # Show sample files
            sample_files = folder_stats['files'][:3]  # Show first 3 files
            for file_info in sample_files:
                print(f"     - {file_info['name']} ({file_info['format']})")
            
            if len(folder_stats['files']) > 3:
                print(f"     ... and {len(folder_stats['files']) - 3} more files")
            
            print()
            total_images += folder_stats['image_count']
        
        print("=" * 50)
        print(f"TOTAL: Would process {total_images} images")
        print("=" * 50)
    
    def interactive_mode(self) -> None:
        """Interactive mode for selective processing"""
        print("Interactive Image Processing Mode")
        print("=" * 40)
        
        # Show available folders
        stats = self.folder_utils.get_folder_stats()
        folder_names = list(stats.keys())
        
        print("Available folders:")
        for i, folder_name in enumerate(folder_names, 1):
            image_count = stats[folder_name]['image_count']
            print(f"  {i}. {folder_name} ({image_count} images)")
        
        print(f"  {len(folder_names) + 1}. Process all folders")
        print(f"  {len(folder_names) + 2}. Dry run (show what would be processed)")
        print("  0. Exit")
        
        while True:
            try:
                choice = input(f"\nSelect option (0-{len(folder_names) + 2}): ")
                choice_num = int(choice)
                
                if choice_num == 0:
                    print("Exiting...")
                    break
                elif choice_num == len(folder_names) + 1:
                    self.process_all_folders()
                    break
                elif choice_num == len(folder_names) + 2:
                    self.dry_run()
                    break
                elif 1 <= choice_num <= len(folder_names):
                    selected_folder = folder_names[choice_num - 1]
                    self.process_single_folder(selected_folder)
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description="Batch Image Processing Tool")
    parser.add_argument("--folder", "-f", help="Process specific folder by name")
    parser.add_argument("--format", help="Process only specific format (e.g., .png, .jpg)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed without processing")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--discover", "-d", action="store_true", help="Discover and show image statistics")
    
    args = parser.parse_args()
    
    processor = BatchProcessor()
    
    if args.discover:
        processor.folder_utils.print_discovery_report()
    elif args.dry_run:
        processor.dry_run()
    elif args.interactive:
        processor.interactive_mode()
    elif args.folder:
        processor.process_single_folder(args.folder)
    elif args.format:
        processor.process_by_format(args.format)
    else:
        # Default: process all folders
        processor.process_all_folders()

if __name__ == "__main__":
    main()
