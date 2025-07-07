#!/usr/bin/env python3
"""
MINIMAL FIX SCRIPT - Only fixes canonical URL
Avoiding risky SVG and asset changes that could break layout
"""
import re
import shutil
from pathlib import Path

def minimal_fix():
    test_file = Path('gum-disease-symptoms-TEST/index.html')
    backup_file = Path('gum-disease-symptoms-TEST/index.html.minimal_backup')
    
    print("🔧 MINIMAL FIX - CANONICAL URL ONLY")
    print("="*40)
    
    # Read original
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    shutil.copy2(test_file, backup_file)
    print(f"💾 Backup created: {backup_file}")
    
    original_content = content
    
    # ONLY Fix canonical URL
    print("\n🎯 Fixing canonical URL...")
    canonical_pattern = r'(<link\s+rel=["\']canonical["\']\s+href=["\'])([^"\']*)(["\']\s*[^>]*>)'
    
    def fix_canonical(match):
        prefix, url, suffix = match.groups()
        if url == 'index.html':
            print(f"   ✅ Fixed: '{url}' → '/gum-disease-symptoms/'")
            return f"{prefix}/gum-disease-symptoms/{suffix}"
        return match.group(0)
    
    content = re.sub(canonical_pattern, fix_canonical, content, flags=re.IGNORECASE)
    
    # Count changes
    changes = len(re.findall(canonical_pattern, original_content, re.IGNORECASE))
    
    if content != original_content:
        # Write fixed content
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed {changes} canonical URL(s)")
        print(f"📄 File updated: {test_file}")
    else:
        print("ℹ️  No changes needed")
    
    print("\n🧪 TEST INSTRUCTIONS:")
    print("1. Open gum-disease-symptoms-TEST/index.html in browser")
    print("2. Check if Special Offers button displays correctly")
    print("3. Check if glyph icons display correctly")
    print("4. If issues persist, restore backup and investigate further")
    print(f"   Restore command: copy \"{backup_file}\" \"{test_file}\"")

if __name__ == "__main__":
    minimal_fix() 