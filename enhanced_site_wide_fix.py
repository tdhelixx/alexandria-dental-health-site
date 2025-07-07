#!/usr/bin/env python3
"""
Enhanced Site-Wide Fix Script
Fixes: canonical URLs, font paths, AND navigation links
Based on discovered issues: canonical, fonts, and relative navigation paths
"""
import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import argparse

class EnhancedSiteWideFixer:
    def __init__(self, site_root, backup_dir="backups_enhanced"):
        self.site_root = Path(site_root)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.stats = {
            'files_processed': 0,
            'canonical_fixes': 0,
            'font_path_fixes': 0,
            'navigation_fixes': 0,
            'errors': 0,
            'skipped_files': []
        }
        
        # Navigation links that need fixing from relative to proper relative paths
        self.nav_links_to_fix = [
            'about/', 'services/', 'blog/', 'contact-us/', 'testimonials/',
            'office-tour/', 'smile-gallery/', 'advanced-technology/',
            'dental-insurance-accepted/', 'patient-information/',
            'general-dentistry-services/', 'cosmetic-restorative/',
            'preventative/', 'restorative/', 'concerns/', 'emergency-dentistry/',
            'cosmetic-dentistry/', 'invisalign/', 'veneers/', 'dental-implants/',
            'dentures/', 'dental-crowns/', 'dental-bridges/', 'root-canal-therapy/',
            'teeth-whitening/', 'tooth-bonding/', 'dental-cleanings/',
            'dental-exams/', 'dental-fillings/', 'tmj-treatment/',
            'tooth-extractions/', 'periodontal-therapy/', 'sedation-dentistry/',
            'sleep-apnea/', 'six-month-smiles/', 'snap-on-smile/',
            'invisalign-teen/', 'getting-veneers/', 'lumineers/',
            'about-dental-implants/', 'implant-supported-dentures/',
            'full-mouth-reconstruction/', 'mouth-guards/', 'emergency-dental-information/',
            'chipped-tooth-repair/', 'crooked-teeth/', 'dental-anxiety/',
            'gum-disease-symptoms/', 'gum-disease-treatment/', 'jaw-pain/',
            'missing-teeth/', 'teeth-grinding/', 'tooth-pain/',
            'functional-orthodontics/', 'dental-gingivitis-prevention/',
            'dental-cavities-solutions/', 'dental-crowns-faqs/',
            'dental-implant-benefits/', 'dentures-cleaning-and-care/',
            'importance-of-baby-teeth/', 'root-canal-symptoms/',
            'root-canal-recovery/', 'special/'
        ]
        
    def get_canonical_path(self, file_path):
        """Generate correct canonical path based on file location"""
        rel_path = file_path.relative_to(self.site_root)
        
        if rel_path.name == 'index.html':
            if rel_path.parent == Path('.'):
                return '/'
            else:
                return f'/{rel_path.parent.as_posix()}/'
        else:
            return f'/{rel_path.with_suffix("").as_posix()}/'
    
    def get_relative_path_depth(self, file_path):
        """Calculate how many '../' needed to reach site root"""
        rel_path = file_path.relative_to(self.site_root)
        depth = len(rel_path.parent.parts)
        return '../' * depth if depth > 0 else ''
    
    def backup_file(self, file_path):
        """Create backup of file before modification"""
        rel_path = file_path.relative_to(self.site_root)
        backup_path = self.backup_dir / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def fix_canonical_urls(self, content, file_path):
        """Fix canonical URL for this file"""
        correct_canonical = self.get_canonical_path(file_path)
        fixes = 0
        
        canonical_pattern = r'(<link\s+rel=["\']canonical["\']\s+href=["\'])([^"\']*)(["\']\s*[^>]*>)'
        
        def fix_canonical(match):
            nonlocal fixes
            prefix, current_url, suffix = match.groups()
            
            if current_url == 'index.html' or not current_url.startswith('/'):
                fixes += 1
                return f"{prefix}{correct_canonical}{suffix}"
            
            return match.group(0)
        
        new_content = re.sub(canonical_pattern, fix_canonical, content, flags=re.IGNORECASE)
        return new_content, fixes
    
    def fix_font_paths(self, content, file_path):
        """Fix Font Awesome paths for this file"""
        fixes = 0
        relative_prefix = self.get_relative_path_depth(file_path)
        
        font_pattern = r'url\(([^)]*?)wp-content/plugins/bb-plugin/fonts'
        
        def fix_font_path(match):
            nonlocal fixes
            full_match = match.group(0)
            path_start = match.group(1)
            
            expected_prefix = relative_prefix
            if expected_prefix not in path_start:
                fixes += 1
                return full_match.replace('wp-content/plugins/bb-plugin/fonts', 
                                        f'{expected_prefix}wp-content/plugins/bb-plugin/fonts')
            
            return full_match
        
        new_content = re.sub(font_pattern, fix_font_path, content)
        return new_content, fixes
    
    def fix_navigation_links(self, content, file_path):
        """Fix navigation links from relative to proper relative paths"""
        fixes = 0
        relative_prefix = self.get_relative_path_depth(file_path)
        
        # Only fix navigation links on pages that are in subdirectories
        if not relative_prefix:  # Root level pages don't need fixing
            return content, 0
        
        for nav_link in self.nav_links_to_fix:
            # Pattern: href="navlink/" but not href="../navlink/" or href="/navlink/"
            pattern = rf'(href=["\'])({re.escape(nav_link)})(["\'])'
            
            def fix_nav_link(match):
                nonlocal fixes
                prefix, link, suffix = match.groups()
                
                # Only fix if it doesn't already have ../ or /
                if not link.startswith('../') and not link.startswith('/'):
                    fixes += 1
                    return f"{prefix}{relative_prefix}{link}{suffix}"
                
                return match.group(0)
            
            content = re.sub(pattern, fix_nav_link, content)
        
        return content, fixes
    
    def process_file(self, file_path):
        """Process a single HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            
            # Apply all fixes
            content, canonical_fixes = self.fix_canonical_urls(content, file_path)
            content, font_fixes = self.fix_font_paths(content, file_path)
            content, nav_fixes = self.fix_navigation_links(content, file_path)
            
            total_fixes = canonical_fixes + font_fixes + nav_fixes
            
            # If changes were made, backup and save
            if content != original_content:
                backup_path = self.backup_file(file_path)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.stats['canonical_fixes'] += canonical_fixes
                self.stats['font_path_fixes'] += font_fixes
                self.stats['navigation_fixes'] += nav_fixes
                
                rel_path = file_path.relative_to(self.site_root)
                print(f"✅ {rel_path}: {canonical_fixes}canonical + {font_fixes}font + {nav_fixes}nav fixes")
            
            self.stats['files_processed'] += 1
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            self.stats['errors'] += 1
            self.stats['skipped_files'].append(str(file_path))
    
    def find_html_files(self):
        """Find all HTML files in the site"""
        html_files = []
        skip_dirs = {'backups', 'backups_sitewide', 'backups_enhanced', 'hts-cache', '.git'}
        
        for file_path in self.site_root.rglob('*.html'):
            if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                continue
            html_files.append(file_path)
        
        return sorted(html_files)
    
    def run(self, dry_run=False):
        """Run the enhanced site-wide fix"""
        print("🚀 ENHANCED SITE-WIDE FIX - WordPress to Static Conversion")
        print("="*70)
        print(f"📁 Site root: {self.site_root}")
        print(f"💾 Backup dir: {self.backup_dir}")
        print("🔧 Fixes: Canonical URLs + Font Paths + Navigation Links")
        
        if dry_run:
            print("🧪 DRY RUN MODE - No files will be modified")
        
        html_files = self.find_html_files()
        print(f"📄 Found {len(html_files)} HTML files")
        
        if not dry_run:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            print(f"⏰ Backup timestamp: {timestamp}")
        
        print("\n🔧 Processing files...")
        print("-" * 50)
        
        for i, file_path in enumerate(html_files, 1):
            if dry_run:
                rel_path = file_path.relative_to(self.site_root)
                print(f"[{i:3d}/{len(html_files)}] Would process: {rel_path}")
            else:
                self.process_file(file_path)
            
            if i % 25 == 0:
                print(f"   ... processed {i}/{len(html_files)} files")
        
        print("\n📊 SUMMARY:")
        print("-" * 30)
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Canonical fixes: {self.stats['canonical_fixes']}")
        print(f"Font path fixes: {self.stats['font_path_fixes']}")
        print(f"Navigation fixes: {self.stats['navigation_fixes']}")
        print(f"Total fixes: {self.stats['canonical_fixes'] + self.stats['font_path_fixes'] + self.stats['navigation_fixes']}")
        print(f"Errors: {self.stats['errors']}")
        
        if self.stats['errors'] > 0:
            print(f"\n⚠️  Files with errors:")
            for error_file in self.stats['skipped_files']:
                print(f"   {error_file}")
        
        if not dry_run:
            print(f"\n✅ Enhanced site-wide fix complete!")
            print(f"💾 Backups stored in: {self.backup_dir}")
            print("\n🧪 TEST RECOMMENDATIONS:")
            print("1. Test navigation on pages like /tooth-bonding/")
            print("2. Verify Font Awesome icons display correctly")
            print("3. Check canonical URLs in page source")
        else:
            print(f"\n🧪 Dry run complete - no changes made")

def main():
    parser = argparse.ArgumentParser(description='Enhanced site-wide WordPress to Static fix')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--site-root', default='.', help='Site root directory (default: current directory)')
    
    args = parser.parse_args()
    
    fixer = EnhancedSiteWideFixer(args.site_root)
    fixer.run(dry_run=args.dry_run)

if __name__ == "__main__":
    main() 