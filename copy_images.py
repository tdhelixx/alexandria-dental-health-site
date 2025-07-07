#!/usr/bin/env python3
"""
Image Copy Script for Alexandria Dental Health
Copies all images from wp-content/uploads/ to flat images/ directory
"""

import os
import shutil
from pathlib import Path
import argparse

def copy_images():
    """Copy all images from wp-content/uploads to images/ directory"""
    
    # Source and destination directories
    source_dir = Path("wp-content/uploads")
    dest_dir = Path("images")
    
    # Create destination directory if it doesn't exist
    dest_dir.mkdir(exist_ok=True)
    
    # Image extensions to copy
    image_extensions = {'.webp', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico'}
    
    print(f"🚀 Starting image copy from {source_dir} to {dest_dir}")
    print("="*60)
    
    if not source_dir.exists():
        print(f"❌ Source directory {source_dir} does not exist!")
        print("Make sure you're running this from the project root directory.")
        return
    
    copied_count = 0
    skipped_count = 0
    error_count = 0
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            file_ext = file_path.suffix.lower()
            
            # Only copy image files
            if file_ext in image_extensions:
                dest_file = dest_dir / file
                
                try:
                    # Check if file already exists
                    if dest_file.exists():
                        print(f"⚠️  Skipping {file} (already exists)")
                        skipped_count += 1
                        continue
                    
                    # Copy the file
                    shutil.copy2(file_path, dest_file)
                    print(f"✅ Copied: {file}")
                    copied_count += 1
                    
                except Exception as e:
                    print(f"❌ Error copying {file}: {e}")
                    error_count += 1
    
    print("="*60)
    print(f"🎉 Copy complete!")
    print(f"✅ Files copied: {copied_count}")
    print(f"⚠️  Files skipped: {skipped_count}")
    print(f"❌ Errors: {error_count}")
    
    if copied_count > 0:
        print(f"\n📁 All images are now in the {dest_dir} directory")
        print("🚀 Ready to commit and deploy to CloudCannon!")
    
    # List some example files
    image_files = list(dest_dir.glob("*.webp"))[:5]
    if image_files:
        print(f"\n📋 Example files in {dest_dir}:")
        for img in image_files:
            print(f"   - {img.name}")
        if len(list(dest_dir.glob("*"))) > 5:
            print(f"   ... and {len(list(dest_dir.glob('*'))) - 5} more files")

def main():
    parser = argparse.ArgumentParser(description='Copy all images from wp-content/uploads to images/ directory')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be copied without actually copying')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files')
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be copied")
        dry_run_preview()
    else:
        copy_images()

def dry_run_preview():
    """Preview what files would be copied"""
    source_dir = Path("wp-content/uploads")
    dest_dir = Path("images")
    
    if not source_dir.exists():
        print(f"❌ Source directory {source_dir} does not exist!")
        return
    
    image_extensions = {'.webp', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico'}
    files_to_copy = []
    
    # Find all image files
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in image_extensions:
                files_to_copy.append(file)
    
    print(f"📊 Found {len(files_to_copy)} image files to copy:")
    for i, file in enumerate(files_to_copy[:10]):  # Show first 10
        print(f"   {i+1}. {file}")
    
    if len(files_to_copy) > 10:
        print(f"   ... and {len(files_to_copy) - 10} more files")
    
    print(f"\n🎯 These files would be copied to: {dest_dir}/")
    print("Run without --dry-run to actually copy the files")

if __name__ == "__main__":
    main() 