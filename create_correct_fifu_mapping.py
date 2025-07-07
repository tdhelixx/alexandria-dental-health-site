#!/usr/bin/env python3
"""
Create Correct FIFU Mapping
This script reads the WordPress XML file to get the correct post IDs and creates 
a proper FIFU report with the right post IDs for the WordPress plugin.
"""

import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_wordpress_xml(xml_file):
    """Parse WordPress XML file to extract post ID to slug mappings"""
    print(f"Parsing WordPress XML file: {xml_file}")
    
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Find channel element
    channel = root.find('channel')
    if channel is None:
        print("No channel found in XML")
        return {}
    
    # Extract post mappings
    post_mappings = {}
    
    # Find all items (posts/pages)
    for item in channel.findall('item'):
        try:
            # Get post ID
            post_id_elem = item.find('{http://wordpress.org/export/1.2/}post_id')
            if post_id_elem is None:
                continue
            post_id = post_id_elem.text
            
            # Get post name (slug)
            post_name_elem = item.find('{http://wordpress.org/export/1.2/}post_name')
            if post_name_elem is None:
                continue
            post_name = post_name_elem.text
            
            # Get title
            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else 'Unknown'
            
            # Get post type
            post_type_elem = item.find('{http://wordpress.org/export/1.2/}post_type')
            post_type = post_type_elem.text if post_type_elem is not None else 'unknown'
            
            # Store mapping
            if post_name:
                # Clean up slug - remove index.html and other suffixes
                clean_slug = post_name.replace('-index-html', '').replace('blog-', '')
                post_mappings[clean_slug] = {
                    'post_id': post_id,
                    'title': title,
                    'post_type': post_type,
                    'original_slug': post_name
                }
                
                # Also map with original slug for exact matches
                post_mappings[post_name] = {
                    'post_id': post_id,
                    'title': title,
                    'post_type': post_type,
                    'original_slug': post_name
                }
                
        except Exception as e:
            print(f"Error processing item: {e}")
            continue
    
    print(f"Found {len(post_mappings)} post mappings")
    return post_mappings

def parse_original_fifu_report(report_file):
    """Parse the original FIFU report to extract folder names and image URLs"""
    print(f"Parsing original FIFU report: {report_file}")
    
    image_mappings = []
    
    with open(report_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        # Skip header lines and separators
        if 'post_id=' not in line:
            continue
        
        # Parse line format: folder_name - post_id="ID" - attachment_id="ID" - src="URL"
        match = re.search(r'^(.+?)\s*-\s*post_id="(\d+)"\s*-\s*attachment_id="([^"]+)"\s*-\s*src="([^"]+)"', line)
        if match:
            folder_name = match.group(1).strip()
            old_post_id = match.group(2)
            attachment_id = match.group(3)
            image_url = match.group(4)
            
            # Skip external URLs - only keep local WordPress URLs
            if image_url.startswith('http://') or image_url.startswith('https://'):
                continue
            
            # Extract filename from URL
            image_filename = os.path.basename(image_url)
            image_filename = re.sub(r'\?.*', '', image_filename)  # Remove query parameters
            
            image_mappings.append({
                'folder_name': folder_name,
                'old_post_id': old_post_id,
                'attachment_id': attachment_id,
                'image_url': image_url,
                'image_filename': image_filename
            })
    
    print(f"Found {len(image_mappings)} image mappings")
    return image_mappings

def create_corrected_fifu_report(post_mappings, image_mappings, output_file):
    """Create a corrected FIFU report with proper WordPress post IDs"""
    print(f"Creating corrected FIFU report: {output_file}")
    
    matched_count = 0
    unmatched_count = 0
    matched_images = []
    
    for image_data in image_mappings:
        folder_name = image_data['folder_name']
        
        # Try to find matching post by folder name
        matched_post = None
        
        # Try exact match first
        if folder_name in post_mappings:
            matched_post = post_mappings[folder_name]
        else:
            # Try variations
            variations = [
                folder_name.replace('blog-', ''),
                f"blog-{folder_name}",
                f"{folder_name}-index-html",
                f"blog-{folder_name}-index-html"
            ]
            
            for variation in variations:
                if variation in post_mappings:
                    matched_post = post_mappings[variation]
                    break
        
        if matched_post:
            matched_images.append({
                'folder_name': folder_name,
                'post_id': matched_post['post_id'],
                'post_title': matched_post['title'],
                'post_type': matched_post['post_type'],
                'image_filename': image_data['image_filename'],
                'image_url': image_data['image_url']
            })
            matched_count += 1
        else:
            print(f"No match found for folder: {folder_name}")
            unmatched_count += 1
    
    # Remove duplicates based on post_id + filename combination
    unique_images = {}
    for image in matched_images:
        key = f"{image['post_id']}_{image['image_filename']}"
        if key not in unique_images:
            unique_images[key] = image
    
    deduplicated_images = list(unique_images.values())
    
    # Write corrected report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("CORRECTED FIFU-FEATURED IMAGE REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Source: WordPress XML mapping\n")
        f.write(f"Total Images Matched: {matched_count}\n")
        f.write(f"Total Images After Deduplication: {len(deduplicated_images)}\n")
        f.write(f"Total Images Unmatched: {unmatched_count}\n")
        f.write(f"Total Images Found: {len(image_mappings)}\n\n")
        
        f.write("RESULTS:\n")
        f.write("-" * 50 + "\n")
        f.write('Format: folder_name - post_id="ID" - attachment_id="N/A" - src="FILENAME"\n')
        f.write("-" * 50 + "\n")
        
        for image in deduplicated_images:
            f.write(f'{image["folder_name"]} - post_id="{image["post_id"]}" - attachment_id="N/A" - src="{image["image_filename"]}"\n')
    
    print(f"Report created successfully!")
    print(f"Matched: {matched_count} images")
    print(f"After deduplication: {len(deduplicated_images)} images")
    print(f"Unmatched: {unmatched_count} images")
    print(f"Total: {len(image_mappings)} images")
    
    return deduplicated_images

def main():
    # File paths
    xml_file = "alexandriadentalhealthcom.WordPress.2025-07-06.xml"
    original_report = "fifu_featured_images_report.txt"
    corrected_report = "corrected_fifu_featured_images_report.txt"
    
    # Check if files exist
    if not os.path.exists(xml_file):
        print(f"Error: WordPress XML file not found: {xml_file}")
        return
    
    if not os.path.exists(original_report):
        print(f"Error: Original FIFU report not found: {original_report}")
        return
    
    # Parse files
    post_mappings = parse_wordpress_xml(xml_file)
    image_mappings = parse_original_fifu_report(original_report)
    
    # Create corrected report
    matched_images = create_corrected_fifu_report(post_mappings, image_mappings, corrected_report)
    
    print(f"\nCorrected FIFU report created: {corrected_report}")
    print("Copy this file to your WordPress plugin directory!")

if __name__ == "__main__":
    main() 