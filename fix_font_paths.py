#!/usr/bin/env python3
"""
Font Path Fix Script
Fixes inconsistent Font Awesome paths in CSS - safe and targeted fix
"""
import re
import shutil
from pathlib import Path

def fix_font_paths():
    test_file = Path('gum-disease-symptoms-TEST/index.html')
    backup_file = Path('gum-disease-symptoms-TEST/index.html.font_backup')
    
    print("🔧 FONT PATH FIX - Correcting wp-content paths")
    print("="*50)
    
    # Read original
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    shutil.copy2(test_file, backup_file)
    print(f"💾 Backup created: {backup_file}")
    
    original_content = content
    fixes_applied = 0
    
    # Fix: Change "wp-content/plugins/bb-plugin/fonts" to "../wp-content/plugins/bb-plugin/fonts"
    # But ONLY when it doesn't already have ../
    print("\n🎯 Fixing font paths...")
    
    # Pattern: url( followed by wp-content (but not ../wp-content)
    font_pattern = r'url\(([^)]*?)wp-content/plugins/bb-plugin/fonts'
    
    def fix_font_path(match):
        nonlocal fixes_applied
        full_match = match.group(0)
        path_start = match.group(1)
        
        # Only fix if it doesn't already have ../
        if '../' not in path_start:
            fixes_applied += 1
            print(f"   ✅ Fixed: wp-content/... → ../wp-content/...")
            return full_match.replace('wp-content/plugins/bb-plugin/fonts', '../wp-content/plugins/bb-plugin/fonts')
        
        return full_match
    
    content = re.sub(font_pattern, fix_font_path, content)
    
    if content != original_content:
        # Write fixed content
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed {fixes_applied} font path(s)")
        print(f"📄 File updated: {test_file}")
    else:
        print("ℹ️  No font path changes needed")
    
    print("\n🧪 TEST INSTRUCTIONS:")
    print("1. Open gum-disease-symptoms-TEST/index.html in browser")
    print("2. Hard refresh (Ctrl+F5) to clear cached fonts")
    print("3. Check if glyph icons now display correctly")
    print("4. Look for the scroll-to-top arrow in bottom right")
    print(f"   Restore command if needed: copy \"{backup_file}\" \"{test_file}\"")

if __name__ == "__main__":
    fix_font_paths() 