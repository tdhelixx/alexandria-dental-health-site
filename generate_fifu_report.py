import os
import re
from datetime import datetime

def extract_fifu_images(backups_enhanced_path):
    """Extract img tags with fifu-featured="1", their src attributes, post_id, and attachment_id."""
    results = set()  # Use set to avoid duplicates
    
    # Walk through all HTML files in backups_enhanced directory
    for root, dirs, files in os.walk(backups_enhanced_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Find img tags with fifu-featured="1" and extract attributes
                        # More comprehensive pattern to capture post-id, attachment-id, and src
                        pattern = r'<img[^>]*fifu-featured="1"[^>]*?>'
                        img_matches = re.findall(pattern, content, re.IGNORECASE)
                        
                        # Also try the reverse order (src before fifu-featured)
                        pattern2 = r'<img[^>]*src="[^"]*"[^>]*fifu-featured="1"[^>]*>'
                        img_matches2 = re.findall(pattern2, content, re.IGNORECASE)
                        
                        all_img_tags = img_matches + img_matches2
                        
                        if all_img_tags:
                            # Get folder name from path
                            folder_name = os.path.basename(root)
                            
                            for img_tag in all_img_tags:
                                # Extract src attribute
                                src_match = re.search(r'src="([^"]*)"', img_tag, re.IGNORECASE)
                                src = src_match.group(1) if src_match else "N/A"
                                
                                # Extract post-id attribute
                                post_id_match = re.search(r'post-id="([^"]*)"', img_tag, re.IGNORECASE)
                                post_id = post_id_match.group(1) if post_id_match else "N/A"
                                
                                # Extract attachment-id attribute (if present)
                                attachment_id_match = re.search(r'attachment-id="([^"]*)"', img_tag, re.IGNORECASE)
                                attachment_id = attachment_id_match.group(1) if attachment_id_match else "N/A"
                                
                                # Format output with post_id and attachment_id
                                result = f'{folder_name} - post_id="{post_id}" - attachment_id="{attachment_id}" - src="{src}"'
                                results.add(result)
                                
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return sorted(list(results))

def generate_report(output_file):
    """Generate the report and save to txt file."""
    # Path to backups_enhanced directory
    backups_enhanced_path = r"C:\python-scripts\rescue-projects\alexandriadentalhealth-scrape-production - WP\backups_enhanced"
    
    # Extract the results
    results = extract_fifu_images(backups_enhanced_path)
    
    # Generate report content
    report_content = []
    report_content.append("FIFU-FEATURED IMAGE REPORT")
    report_content.append("=" * 50)
    report_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_content.append(f"Source Directory: {backups_enhanced_path}")
    report_content.append(f"Total Images Found: {len(results)}")
    report_content.append("")
    report_content.append("RESULTS:")
    report_content.append("-" * 50)
    report_content.append("Format: folder_name - post_id=\"ID\" - attachment_id=\"ID\" - src=\"URL\"")
    report_content.append("-" * 50)
    
    # Add all results
    for result in results:
        report_content.append(result)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_content))
    
    print(f"Report generated successfully: {output_file}")
    print(f"Total images found: {len(results)}")

if __name__ == "__main__":
    output_file = "fifu_featured_images_report.txt"
    generate_report(output_file) 