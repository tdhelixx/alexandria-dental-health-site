#!/usr/bin/env python3
"""
Script to download missing font files for the Alexandria Dental Health website.
This addresses the HTTrack issue where some fonts weren't captured AND the critical
Bootstrap Glyphicons issue where font files were converted to HTML redirects.
"""

import os
import re
import requests
import time
from pathlib import Path
from urllib.parse import urlparse, unquote

# Base directory for the scraped site
BASE_DIR = Path(__file__).parent

# Google Font URLs that need to be downloaded
GOOGLE_FONT_URLS = [
    # Google Fonts - Raleway
    "https://fonts.gstatic.com/s/raleway/v36/1Ptug8zYS_SKggPNyCAIT5lu.woff2",
    "https://fonts.gstatic.com/s/raleway/v36/1Ptug8zYS_SKggPNyCkIT5lu.woff2", 
    "https://fonts.gstatic.com/s/raleway/v36/1Ptug8zYS_SKggPNyCIIT5lu.woff2",
    "https://fonts.gstatic.com/s/raleway/v36/1Ptug8zYS_SKggPNyCMIT5lu.woff2",
    "https://fonts.gstatic.com/s/raleway/v36/1Ptug8zYS_SKggPNyC0ITw.woff2",
    "https://fonts.gstatic.com/s/raleway/v34/1Ptxg8zYS_SKggPN4iEgvnHyvveLxVtapbCIPrE.woff2",
    
    # Google Fonts - Nunito  
    "https://fonts.gstatic.com/s/nunito/v31/XRXI3I6Li01BKofiOc5wtlZ2di8HDLshdTk3j77e.woff2",
    "https://fonts.gstatic.com/s/nunito/v31/XRXI3I6Li01BKofiOc5wtlZ2di8HDLshdTA3j77e.woff2",
    "https://fonts.gstatic.com/s/nunito/v31/XRXI3I6Li01BKofiOc5wtlZ2di8HDLshdTs3j77e.woff2",
    "https://fonts.gstatic.com/s/nunito/v31/XRXI3I6Li01BKofiOc5wtlZ2di8HDLshdTo3j77e.woff2",
    "https://fonts.gstatic.com/s/nunito/v31/XRXI3I6Li01BKofiOc5wtlZ2di8HDLshdTQ3jw.woff2",
    "https://fonts.gstatic.com/s/nunito/v26/XRXI3I6Li01BKofiOc5wtlZ2di8HDLshdTQ3jw.woff2",
    
    # Additional Google fonts
    "https://fonts.gstatic.com/s/audiowide/v21/l7gdbjpo0cum0ckerWCdmA_OIxo.woff2",
    "https://fonts.gstatic.com/s/audiowide/v21/l7gdbjpo0cum0ckerWCdlg_O.woff2",
    "https://fonts.gstatic.com/s/oxygen/v15/2sDcZG1Wl4LcnbuCJW8zaGW5.woff2",
    "https://fonts.gstatic.com/s/oxygen/v15/2sDcZG1Wl4LcnbuCNWgzZmW5O7w.woff2",
    "https://fonts.gstatic.com/s/oxygen/v15/2sDcZG1Wl4LcnbuCNWgzaGW5.woff2",
    "https://fonts.gstatic.com/s/inter/v19/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuGKYAZJhiI2B.woff2",
    "https://fonts.gstatic.com/s/inter/v19/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuGKYAZthiI2B.woff2",
    "https://fonts.gstatic.com/s/inter/v19/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuGKYAZNhiI2B.woff2",
]

# Bootstrap Glyphicons URLs - these are CRITICAL for website icons
BOOTSTRAP_GLYPHICONS_URLS = [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/fonts/glyphicons-halflings-regular.eot",
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/fonts/glyphicons-halflings-regular.woff2", 
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/fonts/glyphicons-halflings-regular.woff",
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/fonts/glyphicons-halflings-regular.ttf",
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/fonts/glyphicons-halflings-regular.svg",
]

def create_directory_structure(file_path):
    """Create directory structure for the given file path."""
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

def download_font(url, local_path):
    """Download a font file from URL to local path."""
    try:
        print(f"Downloading: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        create_directory_structure(local_path)
        
        # Write the font file
        with open(local_path, 'wb') as f:
            f.write(response.content)
            
        print(f"✓ Downloaded: {local_path}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False

def get_local_font_path(url):
    """Convert a Google Fonts URL to local file path."""
    parsed = urlparse(url)
    
    if 'fonts.gstatic.com' in parsed.netloc:
        # Extract path after /s/
        path_parts = parsed.path.split('/')
        if len(path_parts) >= 3 and path_parts[1] == 's':
            font_family = path_parts[2]  # e.g., 'raleway'
            version = path_parts[3] if len(path_parts) > 3 else 'v1'  # e.g., 'v36'
            filename = os.path.basename(parsed.path)
            
            return f"s/{font_family}/{version}/{filename}"
    
    # Fallback: use the full path
    return parsed.path.lstrip('/')

def download_bootstrap_glyphicons():
    """Download Bootstrap Glyphicons fonts to the correct location."""
    print("\n" + "="*70)
    print("FIXING CRITICAL BOOTSTRAP GLYPHICONS ISSUE")
    print("="*70)
    
    glyphicons_dir = BASE_DIR / "wp-content" / "themes" / "bb-theme" / "fonts"
    downloaded = 0
    failed = 0
    
    for url in BOOTSTRAP_GLYPHICONS_URLS:
        filename = os.path.basename(url)
        local_path = glyphicons_dir / filename
        
        # Skip if file already exists
        if local_path.exists():
            print(f"⚠ Already exists: {local_path}")
            continue
        
        if download_font(url, str(local_path)):
            downloaded += 1
            time.sleep(0.5)  # Be nice to the server
        else:
            failed += 1
    
    print(f"\nBootstrap Glyphicons: Downloaded {downloaded}, Failed {failed}")
    return downloaded, failed

def fix_bootstrap_glyphicons_css():
    """Fix CSS files that reference .html files instead of font files."""
    print("\nFixing Bootstrap Glyphicons CSS references...")
    
    css_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('.css'):
                css_files.append(os.path.join(root, file))
    
    fixed_count = 0
    for css_file in css_files:
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix Bootstrap Glyphicons HTML file references
            # glyphicons-halflings-regular.html -> glyphicons-halflings-regular.eot
            content = re.sub(
                r'glyphicons-halflings-regular\.html',
                'glyphicons-halflings-regular.eot',
                content
            )
            
            # glyphicons-halflings-regular-2.html -> glyphicons-halflings-regular.woff2
            content = re.sub(
                r'glyphicons-halflings-regular-2\.html',
                'glyphicons-halflings-regular.woff2',
                content
            )
            
            # glyphicons-halflings-regular-3.html -> glyphicons-halflings-regular.woff
            content = re.sub(
                r'glyphicons-halflings-regular-3\.html',
                'glyphicons-halflings-regular.woff',
                content
            )
            
            # glyphicons-halflings-regular-4.html -> glyphicons-halflings-regular.ttf
            content = re.sub(
                r'glyphicons-halflings-regular-4\.html',
                'glyphicons-halflings-regular.ttf',
                content
            )
            
            # glyphicons-halflings-regular-5.html -> glyphicons-halflings-regular.svg
            content = re.sub(
                r'glyphicons-halflings-regular-5\.html',
                'glyphicons-halflings-regular.svg',
                content
            )
            
            if content != original_content:
                with open(css_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"✓ Fixed Bootstrap Glyphicons in: {css_file}")
                
        except Exception as e:
            print(f"✗ Error fixing {css_file}: {e}")
    
    print(f"Fixed Bootstrap Glyphicons in {fixed_count} CSS files")
    return fixed_count

def fix_external_redirects():
    """Fix external.html redirects in CSS files."""
    print("\nFixing external.html redirects in CSS files...")
    
    css_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('.css'):
                css_files.append(os.path.join(root, file))
    
    fixed_count = 0
    for css_file in css_files:
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix external.html?link= redirects
            content = re.sub(
                r'external\.html\?link=(https?://[^)]+)',
                r'\1',
                content
            )
            
            # Fix specific Google Fonts references
            content = re.sub(
                r'url\(external\.html\?link=([^)]+)\)',
                r'url(\1)',
                content
            )
            
            if content != original_content:
                with open(css_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"✓ Fixed external redirects in: {css_file}")
                
        except Exception as e:
            print(f"✗ Error fixing {css_file}: {e}")
    
    print(f"Fixed external redirects in {fixed_count} CSS files")
    return fixed_count

def main():
    """Main function to download missing fonts."""
    print("ALEXANDRIA DENTAL HEALTH - FONT RECOVERY SCRIPT")
    print("=" * 70)
    print("Fixing HTTrack font download issues...")
    
    # 1. Download Google Fonts
    print("\n1. Downloading Google Fonts...")
    google_downloaded = 0
    google_failed = 0
    
    for url in GOOGLE_FONT_URLS:
        local_path = get_local_font_path(url)
        full_local_path = BASE_DIR / local_path
        
        # Skip if file already exists
        if full_local_path.exists():
            print(f"⚠ Already exists: {local_path}")
            continue
        
        if download_font(url, str(full_local_path)):
            google_downloaded += 1
            time.sleep(0.5)  # Be nice to the server
        else:
            google_failed += 1
    
    # 2. Download Bootstrap Glyphicons (CRITICAL)
    bootstrap_downloaded, bootstrap_failed = download_bootstrap_glyphicons()
    
    # 3. Fix CSS files
    print("\n" + "="*70)
    print("FIXING CSS FILES")
    print("="*70)
    
    bootstrap_css_fixed = fix_bootstrap_glyphicons_css()
    external_css_fixed = fix_external_redirects()
    
    # Summary
    print("\n" + "="*70)
    print("RECOVERY SUMMARY")
    print("="*70)
    print(f"Google Fonts - Downloaded: {google_downloaded}, Failed: {google_failed}")
    print(f"Bootstrap Glyphicons - Downloaded: {bootstrap_downloaded}, Failed: {bootstrap_failed}")
    print(f"CSS Files Fixed - Bootstrap: {bootstrap_css_fixed}, External Links: {external_css_fixed}")
    
    if bootstrap_downloaded > 0 or bootstrap_css_fixed > 0:
        print("\n🎉 CRITICAL ISSUE FIXED!")
        print("   Bootstrap Glyphicons icons should now display correctly!")
    
    print("\nFont recovery completed!")
    print("Your website should now display all fonts and icons correctly.")

if __name__ == "__main__":
    main() 