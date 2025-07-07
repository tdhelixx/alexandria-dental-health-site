#!/usr/bin/env python3
"""
Fix Critical Broken Links
Targets the most critical issues found by the link checker:
1. Corrupted SVG data URIs with file paths concatenated
2. Missing essential CSS/JS files that exist elsewhere
"""

import os
import re
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).parent

def fix_corrupted_svg_data_uris():
    """Fix corrupted SVG data URIs that have file paths concatenated"""
    print("=== FIXING CORRUPTED SVG DATA URIS ===")
    
    fixed_files = 0
    total_fixes = 0
    
    # Find all HTML files
    html_files = list(BASE_DIR.rglob('*.html'))
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            continue
            
        original_content = content
        
        # Fix pattern: data:image/svg+xml,...wp-content/path
        # This should be just the SVG data URI without the file path
        pattern = r'data:image/svg+xml,[^"\']*?wp-content/[^"\'\s]*'
        matches = re.findall(pattern, content)
        
        if matches:
            # Replace with a clean placeholder SVG
            clean_svg = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"%3E%3C/svg%3E'
            content = re.sub(pattern, clean_svg, content)
            total_fixes += len(matches)
            
            # Write back if changes were made
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_files += 1
            
            print(f"Fixed {len(matches)} corrupted SVG URIs in {html_file.relative_to(BASE_DIR)}")
    
    print(f"✅ Fixed {total_fixes} corrupted SVG data URIs in {fixed_files} files")
    return total_fixes

def fix_missing_css_files():
    """Check for missing CSS files and create fallbacks or find alternatives"""
    print("\n=== CHECKING MISSING CSS FILES ===")
    
    # Look for existing CSS files that might be missing
    wp_includes_css = BASE_DIR / "wp-includes" / "css"
    if not wp_includes_css.exists():
        wp_includes_css.mkdir(parents=True, exist_ok=True)
    
    # Create minimal WordPress main CSS if missing
    wordpress_css = wp_includes_css / "wordpress-main.css"
    if not wordpress_css.exists():
        minimal_css = """
/* Minimal WordPress Core CSS */
.wp-caption { max-width: 100%; }
.wp-caption-text { font-style: italic; }
.alignleft { float: left; margin-right: 1em; }
.alignright { float: right; margin-left: 1em; }
.aligncenter { display: block; margin: 0 auto; }
.clear { clear: both; }
"""
        with open(wordpress_css, 'w') as f:
            f.write(minimal_css)
        print(f"✅ Created minimal WordPress CSS: {wordpress_css.relative_to(BASE_DIR)}")
        return 1
    
    return 0

def check_missing_js_files():
    """Report on missing JavaScript files"""
    print("\n=== CHECKING MISSING JAVASCRIPT FILES ===")
    
    js_dirs = [
        BASE_DIR / "wp-includes" / "js",
        BASE_DIR / "wp-content" / "themes" / "bb-theme" / "js",
        BASE_DIR / "wp-content" / "plugins"
    ]
    
    missing_count = 0
    for js_dir in js_dirs:
        if not js_dir.exists():
            print(f"⚠️  Missing directory: {js_dir.relative_to(BASE_DIR)}")
            missing_count += 1
        else:
            print(f"✅ Found: {js_dir.relative_to(BASE_DIR)}")
    
    return missing_count

def create_missing_critical_files():
    """Create missing critical files that are commonly needed"""
    print("\n=== CREATING MISSING CRITICAL FILES ===")
    
    created_files = 0
    
    # Create robots.txt if missing
    robots_txt = BASE_DIR / "robots.txt"
    if not robots_txt.exists():
        robots_content = """User-agent: *
Allow: /

# Sitemap
Sitemap: /sitemap.xml
"""
        with open(robots_txt, 'w') as f:
            f.write(robots_content)
        print(f"✅ Created robots.txt")
        created_files += 1
    
    # Create minimal sitemap.xml if missing
    sitemap_xml = BASE_DIR / "sitemap.xml"
    if not sitemap_xml.exists():
        sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://alexandriadentalhealth.com/</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
"""
        with open(sitemap_xml, 'w') as f:
            f.write(sitemap_content)
        print(f"✅ Created sitemap.xml")
        created_files += 1
    
    return created_files

def main():
    print("🔧 FIXING CRITICAL BROKEN LINKS")
    print("=" * 50)
    
    total_fixes = 0
    
    # Fix corrupted SVG data URIs
    total_fixes += fix_corrupted_svg_data_uris()
    
    # Fix missing CSS files
    total_fixes += fix_missing_css_files()
    
    # Check JS files (report only)
    missing_js = check_missing_js_files()
    
    # Create missing critical files
    total_fixes += create_missing_critical_files()
    
    print(f"\n📊 SUMMARY:")
    print(f"✅ Total fixes applied: {total_fixes}")
    print(f"⚠️  JavaScript directories missing: {missing_js}")
    print(f"\n💡 Note: Many 'broken links' are WordPress system files")
    print(f"   that aren't needed for a static site (wp-json/, xmlrpc.php, etc.)")
    
    if total_fixes > 0:
        print(f"\n🎯 Critical issues fixed! Run the link checker again to see improvement.")
    
    return total_fixes

if __name__ == "__main__":
    main() 