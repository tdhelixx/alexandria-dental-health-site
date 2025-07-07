#!/usr/bin/env python3
"""
Conservative WordPress-to-Static Fix Script
Only fixes validated critical issues: canonicals, SVG data URIs, hardcoded domains
"""
import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import argparse

class ConservativeFixer:
    def __init__(self, site_root, backup_dir="backups"):
        self.site_root = Path(site_root)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.changes_made = {
            'canonical_fixes': 0,
            'svg_fixes': 0,
            'domain_fixes': 0,
            'files_processed': 0
        }
        
    def backup_file(self, file_path):
        """Create backup of file before modification"""
        rel_path = file_path.relative_to(self.site_root)
        backup_path = self.backup_dir / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def get_proper_canonical(self, file_path):
        """Generate proper canonical URL for a file"""
        rel_path = file_path.relative_to(self.site_root)
        path_parts = rel_path.parts
        
        if rel_path.name == 'index.html':
            if len(path_parts) == 1:
                return '/'
            else:
                return '/' + '/'.join(path_parts[:-1]) + '/'
        else:
            return '/' + str(rel_path).replace('\\', '/')
    
    def fix_canonical_urls(self, content, file_path):
        """Fix canonical URL issues"""
        changes = 0
        
        # Pattern to find canonical links
        canonical_pattern = r'(<link\s+rel=["\']canonical["\']\s+href=["\'])([^"\']*)(["\']\s*[^>]*>)'
        
        def replace_canonical(match):
            nonlocal changes
            prefix, current_url, suffix = match.groups()
            
            # Only fix if it's clearly wrong
            if current_url in ['index.html', '', '../index.html'] or current_url.startswith('index.html'):
                proper_url = self.get_proper_canonical(file_path)
                changes += 1
                print(f"   • Canonical: '{current_url}' → '{proper_url}'")
                return prefix + proper_url + suffix
            
            return match.group(0)
        
        fixed_content = re.sub(canonical_pattern, replace_canonical, content, flags=re.IGNORECASE)
        return fixed_content, changes
    
    def fix_svg_data_uris(self, content, file_path):
        """Fix corrupted SVG data URIs"""
        changes = 0
        
        # Pattern to find SVG data URIs
        svg_pattern = r'(data:image/svg\+xml[^"\']*)'
        
        def fix_svg(match):
            nonlocal changes
            svg_data = match.group(1)
            original_svg = svg_data
            fixed = False
            
            # Fix 1: Remove concatenated file paths
            if 'wp-content' in svg_data or '/plugins/' in svg_data:
                # Find where the SVG ends and the file path begins
                svg_end_pattern = r'(%3E%3C/svg%3E)'
                svg_end_match = re.search(svg_end_pattern, svg_data)
                if svg_end_match:
                    svg_data = svg_data[:svg_end_match.end()]
                    fixed = True
            
            # Fix 2: Fix empty viewBox
            if 'viewBox=%220%200%20%20%22' in svg_data:
                svg_data = svg_data.replace('viewBox=%220%200%20%20%22', 'viewBox=%220%200%20100%20100%22')
                fixed = True
            
            if fixed:
                changes += 1
                print(f"   • SVG: Fixed corrupted data URI")
                return svg_data
            
            return original_svg
        
        fixed_content = re.sub(svg_pattern, fix_svg, content)
        return fixed_content, changes
    
    def fix_hardcoded_domains(self, content, file_path):
        """Fix hardcoded domain references"""
        changes = 0
        
        # Patterns for hardcoded domains
        domain_patterns = [
            (r'https://www\.alexandriadentalhealth\.com/', './'),
            (r'http://www\.alexandriadentalhealth\.com/', './'),
            (r'https://www\.alexandriadentalhealth\.com', '.'),
            (r'http://www\.alexandriadentalhealth\.com', '.')
        ]
        
        fixed_content = content
        for pattern, replacement in domain_patterns:
            matches = len(re.findall(pattern, fixed_content, re.IGNORECASE))
            if matches > 0:
                fixed_content = re.sub(pattern, replacement, fixed_content, flags=re.IGNORECASE)
                changes += matches
                print(f"   • Domain: Fixed {matches} hardcoded domain references")
        
        return fixed_content, changes
    
    def process_file(self, file_path, create_backup=True):
        """Process a single HTML file"""
        print(f"\n📄 Processing: {file_path.relative_to(self.site_root)}")
        
        # Read file
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                original_content = f.read()
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
            return False
        
        # Create backup if requested
        if create_backup:
            backup_path = self.backup_file(file_path)
            print(f"   💾 Backup created: {backup_path}")
        
        # Apply fixes
        content = original_content
        total_changes = 0
        
        # 1. Fix canonical URLs
        content, canonical_changes = self.fix_canonical_urls(content, file_path)
        total_changes += canonical_changes
        self.changes_made['canonical_fixes'] += canonical_changes
        
        # 2. Fix SVG data URIs
        content, svg_changes = self.fix_svg_data_uris(content, file_path)
        total_changes += svg_changes
        self.changes_made['svg_fixes'] += svg_changes
        
        # 3. Fix hardcoded domains
        content, domain_changes = self.fix_hardcoded_domains(content, file_path)
        total_changes += domain_changes
        self.changes_made['domain_fixes'] += domain_changes
        
        # Write file if changes were made
        if total_changes > 0:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ {total_changes} fixes applied successfully")
                self.changes_made['files_processed'] += 1
                return True
            except Exception as e:
                print(f"   ❌ Error writing file: {e}")
                return False
        else:
            print(f"   ℹ️  No issues found - file unchanged")
            return True
    
    def validate_before_after(self, file_path):
        """Validate fixes by comparing before/after"""
        backup_path = None
        for backup_file in self.backup_dir.rglob("*"):
            if backup_file.name == file_path.name:
                backup_path = backup_file
                break
        
        if not backup_path:
            print("   ⚠️  No backup found for validation")
            return
        
        print(f"\n🔍 Validation Report for {file_path.name}")
        print("=" * 50)
        
        # Read both files
        with open(backup_path, 'r', encoding='utf-8', errors='ignore') as f:
            original = f.read()
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            fixed = f.read()
        
        # Check canonical URLs
        orig_canonical = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']', original, re.IGNORECASE)
        fixed_canonical = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']', fixed, re.IGNORECASE)
        
        if orig_canonical != fixed_canonical:
            print("📍 Canonical URL Changes:")
            for i, (orig, new) in enumerate(zip(orig_canonical + [''] * 10, fixed_canonical + [''] * 10)):
                if orig != new and (orig or new):
                    print(f"   Before: {orig}")
                    print(f"   After:  {new}")
        
        # Check domain references
        orig_domains = len(re.findall(r'https://www\.alexandriadentalhealth\.com', original, re.IGNORECASE))
        fixed_domains = len(re.findall(r'https://www\.alexandriadentalhealth\.com', fixed, re.IGNORECASE))
        
        if orig_domains != fixed_domains:
            print(f"🌐 Domain References: {orig_domains} → {fixed_domains}")
        
        # Check SVG count
        orig_svgs = len(re.findall(r'data:image/svg\+xml', original))
        fixed_svgs = len(re.findall(r'data:image/svg\+xml', fixed))
        
        print(f"🎨 SVG Data URIs: {orig_svgs} found, {fixed_svgs} after processing")
        
        print("✅ Validation complete\n")
    
    def print_summary(self):
        """Print summary of all changes made"""
        print("\n" + "="*60)
        print("SUMMARY OF CHANGES")
        print("="*60)
        print(f"Files processed: {self.changes_made['files_processed']}")
        print(f"Canonical URLs fixed: {self.changes_made['canonical_fixes']}")
        print(f"SVG data URIs fixed: {self.changes_made['svg_fixes']}")
        print(f"Domain references fixed: {self.changes_made['domain_fixes']}")
        total_fixes = sum([self.changes_made['canonical_fixes'], 
                          self.changes_made['svg_fixes'], 
                          self.changes_made['domain_fixes']])
        print(f"Total fixes applied: {total_fixes}")
        
        if total_fixes > 0:
            print(f"\n✅ Success! All backups saved in: {self.backup_dir}")
        else:
            print(f"\nℹ️  No issues found that needed fixing")

def main():
    parser = argparse.ArgumentParser(description='Conservative WordPress-to-static site fixer')
    parser.add_argument('--file', help='Process single file (test mode)')
    parser.add_argument('--site-root', default='.', help='Site root directory')
    parser.add_argument('--backup-dir', default='backups', help='Backup directory')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backups')
    parser.add_argument('--validate', help='Validate specific file after processing')
    
    args = parser.parse_args()
    
    fixer = ConservativeFixer(args.site_root, args.backup_dir)
    
    if args.file:
        # Single file mode (testing)
        file_path = Path(args.site_root) / args.file
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return
        
        print(f"🧪 TEST MODE: Processing single file")
        success = fixer.process_file(file_path, create_backup=not args.no_backup)
        
        if success and args.validate:
            fixer.validate_before_after(file_path)
        
    else:
        # Full site mode
        html_files = list(Path(args.site_root).rglob("*.html"))
        print(f"🌐 FULL SITE MODE: Processing {len(html_files)} HTML files")
        
        confirm = input("This will modify all HTML files. Continue? (y/N): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return
        
        for file_path in html_files:
            fixer.process_file(file_path, create_backup=not args.no_backup)
    
    fixer.print_summary()

if __name__ == "__main__":
    main() 