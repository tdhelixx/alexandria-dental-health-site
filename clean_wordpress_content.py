#!/usr/bin/env python3
"""
WordPress Content Cleaner
Removes external CDN references, empty SVG placeholders, and duplicate images from WordPress XML content.
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

def clean_wordpress_content(input_file, output_file, dry_run=False):
    """Clean WordPress XML content by removing external references and duplicates."""
    
    mode = "DRY RUN" if dry_run else "PRODUCTION"
    print(f"[{mode}] Reading WordPress XML file: {input_file}")
    
    # Read the XML content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content  # Keep original for dry run
    
    # Keep track of changes
    changes = {
        'empty_svg_removed': 0,
        'external_cdn_removed': 0,
        'duplicate_images_removed': 0
    }
    
    # Keep track of found issues for reporting
    issues_found = {
        'empty_svg_blocks': [],
        'external_cdn_blocks': [],
        'duplicate_image_blocks': []
    }
    
    # 1. Find and handle empty SVG placeholders
    print(f"[{mode}] Identifying empty SVG placeholders...")
    empty_svg_pattern = r'<!-- wp:image -->\s*<figure class="wp-block-image"><img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www\.w3\.org/2000/svg%22%20viewBox=%220%200%20%20%22%3E%3C/svg%3E"[^>]*></figure>\s*<!-- /wp:image -->'
    
    def handle_empty_svg(match):
        changes['empty_svg_removed'] += 1
        issues_found['empty_svg_blocks'].append(match.group(0)[:100] + "...")  # Store first 100 chars for reporting
        return '' if not dry_run else match.group(0)
    
    content = re.sub(empty_svg_pattern, handle_empty_svg, content, flags=re.DOTALL)
    
    # 2. Find and handle external CDN image references
    print(f"[{mode}] Identifying external CDN image references...")
    external_cdn_pattern = r'<!-- wp:image -->\s*<figure class="wp-block-image"><img src="http://www\.dental\.inceptionimages\.com/[^"]*"[^>]*></figure>\s*<!-- /wp:image -->'
    
    def handle_external_cdn(match):
        changes['external_cdn_removed'] += 1
        issues_found['external_cdn_blocks'].append(match.group(0)[:100] + "...")  # Store first 100 chars for reporting
        return '' if not dry_run else match.group(0)
    
    content = re.sub(external_cdn_pattern, handle_external_cdn, content, flags=re.DOTALL)
    
    # 3. Find and handle duplicate consecutive images (same src)
    print(f"[{mode}] Identifying duplicate consecutive images...")
    duplicate_pattern = r'(<!-- wp:image -->\s*<figure class="wp-block-image"><img src="([^"]*)"[^>]*></figure>\s*<!-- /wp:image -->)\s*(?=<!-- wp:image -->\s*<figure class="wp-block-image"><img src="\2"[^>]*></figure>\s*<!-- /wp:image -->)'
    
    def handle_duplicate(match):
        changes['duplicate_images_removed'] += 1
        src = match.group(2)
        issues_found['duplicate_image_blocks'].append(f"Duplicate image: {src}")
        return '' if not dry_run else match.group(0)
    
    content = re.sub(duplicate_pattern, handle_duplicate, content, flags=re.DOTALL)
    
    # 4. Clean up any remaining external CDN references in regular img tags
    if not dry_run:
        print(f"[{mode}] Cleaning up remaining external CDN references...")
        content = re.sub(r'http://www\.dental\.inceptionimages\.com/', '../', content)
        
        # 5. Remove any remaining empty image blocks
        empty_image_pattern = r'<!-- wp:image -->\s*<figure class="wp-block-image"></figure>\s*<!-- /wp:image -->'
        content = re.sub(empty_image_pattern, '', content, flags=re.DOTALL)
    
    # Write the cleaned content (only in production mode)
    if not dry_run:
        print(f"[{mode}] Writing cleaned content to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print(f"[{mode}] No file written (dry run mode)")
    
    # Report changes
    print(f"\n[{mode}] Cleaning Summary:")
    print(f"Empty SVG placeholders found: {changes['empty_svg_removed']}")
    print(f"External CDN images found: {changes['external_cdn_removed']}")
    print(f"Duplicate images found: {changes['duplicate_images_removed']}")
    print(f"Total issues found: {sum(changes.values())}")
    
    # Show detailed findings if any issues found
    if sum(changes.values()) > 0:
        print(f"\n[{mode}] Detailed Findings:")
        
        if issues_found['empty_svg_blocks']:
            print(f"\nEmpty SVG placeholders ({len(issues_found['empty_svg_blocks'])}):")
            for i, block in enumerate(issues_found['empty_svg_blocks'][:5], 1):  # Show first 5
                print(f"  {i}. {block}")
            if len(issues_found['empty_svg_blocks']) > 5:
                print(f"  ... and {len(issues_found['empty_svg_blocks']) - 5} more")
        
        if issues_found['external_cdn_blocks']:
            print(f"\nExternal CDN images ({len(issues_found['external_cdn_blocks'])}):")
            for i, block in enumerate(issues_found['external_cdn_blocks'][:5], 1):  # Show first 5
                print(f"  {i}. {block}")
            if len(issues_found['external_cdn_blocks']) > 5:
                print(f"  ... and {len(issues_found['external_cdn_blocks']) - 5} more")
        
        if issues_found['duplicate_image_blocks']:
            print(f"\nDuplicate images ({len(issues_found['duplicate_image_blocks'])}):")
            for i, block in enumerate(issues_found['duplicate_image_blocks'][:5], 1):  # Show first 5
                print(f"  {i}. {block}")
            if len(issues_found['duplicate_image_blocks']) > 5:
                print(f"  ... and {len(issues_found['duplicate_image_blocks']) - 5} more")
    
    return changes, issues_found

def main():
    import sys
    
    # Define file paths
    input_file = "alexandriadentalhealthcom.WordPress.2025-07-06.xml"
    output_file = "alexandriadentalhealthcom.WordPress.2025-07-06-CLEANED.xml"
    
    # Check for dry run argument
    dry_run = len(sys.argv) > 1 and sys.argv[1].lower() in ['--dry-run', '-d', 'dry-run']
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found!")
        return
    
    try:
        # Clean the WordPress content
        changes, issues_found = clean_wordpress_content(input_file, output_file, dry_run)
        
        mode = "DRY RUN" if dry_run else "PRODUCTION"
        print(f"\n[{mode}] Content cleaning completed successfully!")
        print(f"Original file: {input_file}")
        
        if not dry_run:
            print(f"Cleaned file: {output_file}")
            
            # Show file sizes
            original_size = Path(input_file).stat().st_size
            cleaned_size = Path(output_file).stat().st_size
            size_reduction = original_size - cleaned_size
            
            print(f"\nFile size comparison:")
            print(f"Original: {original_size:,} bytes")
            print(f"Cleaned: {cleaned_size:,} bytes")
            print(f"Reduction: {size_reduction:,} bytes ({size_reduction/original_size*100:.1f}%)")
        else:
            print(f"Cleaned file: {output_file} (would be created)")
            print(f"\nTo perform actual cleaning, run: python clean_wordpress_content.py")
            print(f"Current mode: DRY RUN (no files modified)")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main() 