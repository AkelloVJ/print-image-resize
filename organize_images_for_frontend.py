#!/usr/bin/env python3
"""
Organize processed images for frontend print services
Moves images to appropriate product folders and updates references
"""

import os
import shutil
from pathlib import Path
import re

# Base paths
FRONTEND_PUBLIC = Path("/home/victor/Music/brandingstudiopublicfrontend/public")
PRINT_IMAGES_SOURCE = FRONTEND_PUBLIC / "print images"
PRINT_SERVICES_APP = Path("/home/victor/Music/brandingstudiopublicfrontend/src/app/print-services")

# Image mapping based on filename prefixes to product categories
IMAGE_MAPPING = {
    # Banners & Large Format
    'backdrop_banners': {
        'category': 'banners-large-format',
        'subcategory': 'backdrop-banners',
        'path': 'banners-large-format/backdrop-banners',
        'images': []
    },
    'vinyl_banners': {
        'category': 'banners-large-format',
        'subcategory': 'vinyl-banners',
        'path': 'banners-large-format/vinyl-banners',
        'images': []
    },
    'roll_up_banners': {
        'category': 'banners-large-format',
        'subcategory': 'roll-up-banners',
        'path': 'banners-large-format/roll-up-banners',
        'images': []
    },
    'custom_flags': {
        'category': 'banners-large-format',
        'subcategory': 'custom-flags',
        'path': 'banners-large-format/custom-flags',
        'images': []
    },
    
    # Business Stationery
    'standard_business_cards': {
        'category': 'business-stationery',
        'subcategory': 'business-cards-standard',
        'path': 'business-stationery/business-cards/standard',
        'images': []
    },
    'folded_business_cards': {
        'category': 'business-stationery',
        'subcategory': 'business-cards-folded',
        'path': 'business-stationery/business-cards/folded',
        'images': []
    },
    'spot_uv_business_cards': {
        'category': 'business-stationery',
        'subcategory': 'business-cards-spot-uv',
        'path': 'business-stationery/business-cards/spot-uv',
        'images': []
    },
    'custom_envelopes': {
        'category': 'business-stationery',
        'subcategory': 'envelopes',
        'path': 'business-stationery/envelopes',
        'images': []
    },
    'letterheads': {
        'category': 'business-stationery',
        'subcategory': 'letterheads',
        'path': 'business-stationery/letterheads',
        'images': []
    },
    'presentation_folders': {
        'category': 'business-stationery',
        'subcategory': 'presentation-folders',
        'path': 'business-stationery/presentation-folders',
        'images': []
    },
    
    # Marketing & Promotional Materials
    'a3__posters': {
        'category': 'marketing-promotional',
        'subcategory': 'posters-a3',
        'path': 'marketing-promotional/posters/a3',
        'images': []
    },
    'a4_flyers': {
        'category': 'marketing-promotional',
        'subcategory': 'flyers-a4',
        'path': 'marketing-promotional/flyers/a4',
        'images': []
    },
    'trifold_bronchures': {
        'category': 'marketing-promotional',
        'subcategory': 'brochures-tri-fold',
        'path': 'marketing-promotional/brochures/tri-fold',
        'images': []
    },
    'custom_notebooks': {
        'category': 'marketing-promotional',
        'subcategory': 'notebooks-custom',
        'path': 'marketing-promotional/notebooks/custom',
        'images': []
    },
    
    # Photo & Specialty
    'canvas_prints': {
        'category': 'photo-specialty',
        'subcategory': 'canvas-prints',
        'path': 'photo-specialty/canvas-prints',
        'images': []
    },
    'mounted_photos': {
        'category': 'photo-specialty',
        'subcategory': 'mounted-photos',
        'path': 'photo-specialty/mounted-photos',
        'images': []
    },
    'photo_calenders': {
        'category': 'marketing-promotional',
        'subcategory': 'calendars-2025',
        'path': 'marketing-promotional/calendars/2025',
        'images': []
    },
    'acrylic_paints': {
        'category': 'photo-specialty',
        'subcategory': 'acrylic-paints',
        'path': 'photo-specialty/acrylic-paints',
        'images': []
    },
    
    # Promotional Products
    'custom_mugs_': {
        'category': 'promotional-products',
        'subcategory': 'mugs',
        'path': 'promotional-products/mugs',
        'images': []
    },
    'custom_pens': {
        'category': 'promotional-products',
        'subcategory': 'pens',
        'path': 'promotional-products/pens',
        'images': []
    },
    'custom_t-shirts': {
        'category': 'promotional-products',
        'subcategory': 't-shirts',
        'path': 'promotional-products/t-shirts',
        'images': []
    },
    'water_bottles': {
        'category': 'promotional-products',
        'subcategory': 'water-bottles',
        'path': 'promotional-products/water-bottles',
        'images': []
    },
    
    # Stickers & Labels
    'car_decals_': {
        'category': 'stickers-labels',
        'subcategory': 'car-decals',
        'path': 'stickers-labels/car-decals',
        'images': []
    },
    'vinyl_stickers': {
        'category': 'stickers-labels',
        'subcategory': 'vinyl-stickers',
        'path': 'stickers-labels/vinyl-stickers',
        'images': []
    },
    'window_decals_': {
        'category': 'stickers-labels',
        'subcategory': 'window-decals',
        'path': 'stickers-labels/window-decals',
        'images': []
    },
    'product_labels': {
        'category': 'stickers-labels',
        'subcategory': 'product-labels',
        'path': 'stickers-labels/product-labels',
        'images': []
    }
}

def organize_images():
    """Organize images into appropriate product folders"""
    print("Organizing images for frontend print services...")
    
    # Process each category folder
    for category_folder in PRINT_IMAGES_SOURCE.iterdir():
        if not category_folder.is_dir() or not category_folder.name.endswith('_resized'):
            continue
            
        print(f"\nProcessing category: {category_folder.name}")
        
        # Get all webp files in this category
        webp_files = list(category_folder.glob("*.webp"))
        print(f"  Found {len(webp_files)} images")
        
        # Categorize images by prefix
        for webp_file in webp_files:
            filename = webp_file.name
            
            # Find matching category
            matched = False
            for prefix, mapping in IMAGE_MAPPING.items():
                if filename.startswith(prefix):
                    mapping['images'].append(webp_file)
                    matched = True
                    break
            
            if not matched:
                print(f"    No mapping found for: {filename}")
    
    # Create product image folders and move images
    for prefix, mapping in IMAGE_MAPPING.items():
        if not mapping['images']:
            continue
            
        print(f"\nProcessing {prefix}: {len(mapping['images'])} images")
        
        # Create product image folder
        product_images_dir = FRONTEND_PUBLIC / "images" / "products" / mapping['subcategory']
        product_images_dir.mkdir(parents=True, exist_ok=True)
        
        # Move and rename images
        for i, image_file in enumerate(mapping['images'][:4], 1):  # Limit to 4 images per product
            new_filename = f"{mapping['subcategory']}-{i}.webp"
            dest_path = product_images_dir / new_filename
            
            print(f"  Moving: {image_file.name} -> {new_filename}")
            shutil.copy2(str(image_file), str(dest_path))
    
    print("\nImage organization completed!")

def update_product_pages():
    """Update product pages with new image references"""
    print("\nUpdating product pages with new image references...")
    
    for prefix, mapping in IMAGE_MAPPING.items():
        if not mapping['images']:
            continue
            
        page_path = PRINT_SERVICES_APP / f"{mapping['path']}/page.tsx"
        
        if not page_path.exists():
            print(f"  Page not found: {page_path}")
            continue
            
        print(f"  Updating: {page_path}")
        
        # Read current page content
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate new image array
        image_count = min(len(mapping['images']), 4)
        new_images = []
        for i in range(1, image_count + 1):
            new_images.append(f"      '/images/products/{mapping['subcategory']}-{i}.webp'")
        
        # Replace images array
        images_pattern = r"images:\s*\[[^\]]*\]"
        new_images_text = f"images: [\n{',\n'.join(new_images)}\n    ]"
        
        updated_content = re.sub(images_pattern, new_images_text, content, flags=re.MULTILINE | re.DOTALL)
        
        # Write updated content
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"    Updated with {image_count} images")

def main():
    """Main function"""
    print("Starting image organization for frontend...")
    
    # Organize images
    organize_images()
    
    # Update product pages
    update_product_pages()
    
    print("\nFrontend image organization completed!")
    print("\nSummary:")
    for prefix, mapping in IMAGE_MAPPING.items():
        if mapping['images']:
            image_count = min(len(mapping['images']), 4)
            print(f"  {mapping['subcategory']}: {image_count} images")

if __name__ == "__main__":
    main()
