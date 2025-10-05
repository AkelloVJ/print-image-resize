#!/usr/bin/env python3
"""
Fix folder structure v2 - properly organize images by category
"""

import os
import shutil
from pathlib import Path
import config

def fix_folder_structure_v2():
    """Properly organize images by category in separate _resized folders"""
    source_dir = Path(config.SOURCE_DIR)
    all_resized_dir = source_dir / "print pictures_resized"
    
    if not all_resized_dir.exists():
        print("No consolidated _resized folder found!")
        return
    
    print("Reorganizing images by category...")
    print(f"Source directory: {source_dir}")
    print(f"All resized directory: {all_resized_dir}")
    
    # Get all webp files
    webp_files = list(all_resized_dir.glob("*.webp"))
    print(f"Found {len(webp_files)} WebP files to reorganize")
    
    # Create category mapping based on filename prefixes
    categories = {
        'photo_specialty': 'photo and speciality',
        'acrylic_paints': 'photo and speciality',
        'canvas_prints': 'photo and speciality', 
        'mounted_photos': 'photo and speciality',
        'photo_calenders': 'photo and speciality',
        'marketing': 'marketing and promotional materials',
        'a4_flyers': 'marketing and promotional materials',
        'custom_notebooks': 'marketing and promotional materials',
        'trifold_bronchures': 'marketing and promotional materials',
        'a3__posters': 'marketing and promotional materials',
        'promotional': 'promotional products and giveaways',
        'water_bottles': 'promotional products and giveaways',
        'custom_pens': 'promotional products and giveaways',
        'custom_mugs_': 'promotional products and giveaways',
        'custom_t-shirts': 'promotional products and giveaways',
        'stickers': 'stickers and labels',
        'car_decals_': 'stickers and labels',
        'vinyl_stickers': 'stickers and labels',
        'window_decals_': 'stickers and labels',
        'product_labels': 'stickers and labels',
        'banners': 'banners and large formats',
        'backdrop_banners': 'banners and large formats',
        'vinyl_banners': 'banners and large formats',
        'custom_flags': 'banners and large formats',
        'roll_up_banners': 'banners and large formats',
        'business_cards': 'business cards',
        'standard_business_cards': 'business cards',
        'folded_business_cards': 'business cards',
        'custom_envelopes': 'business cards',
        'letterheads': 'business cards',
        'spot_uv_business_cards': 'business cards',
        'presentation_folders': 'business cards'
    }
    
    # Process each webp file
    for webp_file in webp_files:
        filename = webp_file.name
        
        # Find the category based on filename prefix
        category = None
        for prefix, main_category in categories.items():
            if filename.startswith(prefix):
                category = main_category
                break
        
        if not category:
            print(f"  Unknown category for: {filename}")
            continue
        
        # Create category _resized folder
        category_resized_dir = source_dir / f"{category}_resized"
        category_resized_dir.mkdir(exist_ok=True)
        
        # Move file to correct category folder
        dest_file = category_resized_dir / filename
        print(f"  Moving {filename} -> {category}_resized/")
        shutil.move(str(webp_file), str(dest_file))
    
    # Remove the consolidated folder if empty
    try:
        all_resized_dir.rmdir()
        print(f"Removed empty consolidated folder: {all_resized_dir}")
    except OSError:
        print(f"Could not remove consolidated folder (not empty): {all_resized_dir}")
    
    print("\nFolder reorganization completed!")
    
    # Show final structure
    print("\nFinal folder structure:")
    resized_folders = list(source_dir.glob("*_resized"))
    for folder in sorted(resized_folders):
        file_count = len(list(folder.glob("*.webp")))
        print(f"  {folder.name}: {file_count} images")

if __name__ == "__main__":
    fix_folder_structure_v2()
