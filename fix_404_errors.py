#!/usr/bin/env python3
"""
Comprehensive 404 Error Fix Script
Fixes critical broken links found by Screaming Frog
Priority: Critical > High > Medium > Low
"""

import os
import re
import glob
from pathlib import Path

class ComprehensiveLinkFixer:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.fixes_applied = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        self.files_processed = 0
        
    def find_html_files(self):
        """Find all HTML files to process"""
        html_files = []
        for pattern in ["**/*.html", "*.html"]:
            html_files.extend(glob.glob(str(self.root_dir / pattern), recursive=True))
        return html_files
    
    def fix_gtm_script_issues(self, content):
        """🔴 CRITICAL: Fix Google Tag Manager script issues"""
        fixes = 0
        
        # Fix GTM script src with malformed filename
        if "'gtm5445.html'" in content:
            content = content.replace(
                "'gtm5445.html'+i+dl;f.parentNode.insertBefore(j,f);",
                "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);"
            )
            fixes += 1
            print("  ✅ Fixed GTM script URL")
        
        # Fix GTM noscript iframe with relative path issues
        content = re.sub(
            r'src="[\.\/]*https://www\.googletagmanager\.com/ns\.html',
            'src="https://www.googletagmanager.com/ns.html',
            content
        )
        if 'googletagmanager.com' in content and '../https://' not in content:
            fixes += 1
            print("  ✅ Fixed GTM iframe src")
            
        return content, fixes
    
    def fix_malformed_external_urls(self, content):
        """🔴 CRITICAL: Fix malformed external URLs with double protocols"""
        fixes = 0
        
        malformed_patterns = [
            (r'(href|src)="[\.\/]*https://', r'\1="https://'),
            (r'(href|src)="[\.\/]*http://', r'\1="http://'),
        ]
        
        for pattern, replacement in malformed_patterns:
            old_content = content
            content = re.sub(pattern, replacement, content)
            if content != old_content:
                fixes += 1
                print("  ✅ Fixed malformed external URL")
        
        return content, fixes
    
    def fix_missing_image_paths(self, content):
        """🟠 HIGH: Fix missing image path structure"""
        fixes = 0
        
        # Fix smile-gallery images with wrong path structure
        # Pattern: /smile-gallery/wp-content/uploads/
        # Should be: /wp-content/uploads/
        if '/smile-gallery/wp-content/uploads/' in content:
            content = content.replace('/smile-gallery/wp-content/uploads/', '/wp-content/uploads/')
            fixes += 1
            print("  ✅ Fixed smile-gallery image paths")
        
        # Fix blog images with wrong path structure  
        # Pattern: /blog/wp-content/uploads/
        # Should be: /wp-content/uploads/
        if '/blog/wp-content/uploads/' in content:
            content = content.replace('/blog/wp-content/uploads/', '/wp-content/uploads/')
            fixes += 1
            print("  ✅ Fixed blog image paths")
            
        return content, fixes
    
    def fix_font_paths(self, content):
        """🟠 HIGH: Fix FontAwesome and other font paths"""
        fixes = 0
        
        # Fix FontAwesome paths
        # Pattern: /blog/wp-content/plugins/bb-plugin/fonts/
        # Should be: /wp-content/plugins/bb-plugin/fonts/
        if '/blog/wp-content/plugins/bb-plugin/fonts/' in content:
            content = content.replace('/blog/wp-content/plugins/bb-plugin/fonts/', '/wp-content/plugins/bb-plugin/fonts/')
            fixes += 1
            print("  ✅ Fixed FontAwesome font paths")
            
        return content, fixes
    
    def fix_navigation_structure_issues(self, content):
        """🟡 MEDIUM: Fix wrong internal navigation structure"""
        fixes = 0
        
        # These are navigation links that treat pages as subdirectories
        wrong_nav_patterns = [
            ('/crooked-teeth/us/', '/us/'),
            ('/crooked-teeth/privacy-policy/', '/privacy-policy/'),
            ('/crooked-teeth/family-dentist/', '/family-dentist/'),
            ('/crooked-teeth/accessibility/', '/accessibility/'),
            ('/teeth-grinding/privacy-policy/', '/privacy-policy/'),
            ('/teeth-grinding/family-dentist/', '/family-dentist/'),
            ('/teeth-grinding/accessibility/', '/accessibility/'),
            ('/tooth-bonding/privacy-policy/', '/privacy-policy/'),
            ('/tooth-bonding/family-dentist/', '/family-dentist/'),
            ('/tooth-bonding/accessibility/', '/accessibility/'),
        ]
        
        for wrong_path, correct_path in wrong_nav_patterns:
            if wrong_path in content:
                content = content.replace(wrong_path, correct_path)
                fixes += 1
                print(f"  ✅ Fixed navigation: {wrong_path} → {correct_path}")
                
        return content, fixes
    
    def remove_wordpress_cache_references(self, content):
        """🔵 LOW: Remove WordPress cache file references"""
        fixes = 0
        
        # Remove TenWeb optimizer cache CSS references
        # These files don't exist in static sites
        cache_patterns = [
            r'<link[^>]*wp-content/cache/tw_optimize/css/[^>]*>',
            r'<script[^>]*wp-content/plugins/tenweb-speed-optimizer[^>]*></script>',
        ]
        
        for pattern in cache_patterns:
            old_content = content
            content = re.sub(pattern, '', content)
            if content != old_content:
                fixes += 1
                print("  ✅ Removed WordPress cache reference")
                
        return content, fixes
    
    def process_file(self, file_path):
        """Process a single HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            file_fixes = 0
            
            print(f"\n📄 Processing: {file_path}")
            
            # Apply fixes in priority order
            content, critical_fixes = self.fix_gtm_script_issues(content)
            file_fixes += critical_fixes
            self.fixes_applied['critical'] += critical_fixes
            
            content, critical_fixes2 = self.fix_malformed_external_urls(content)
            file_fixes += critical_fixes2
            self.fixes_applied['critical'] += critical_fixes2
            
            content, high_fixes = self.fix_missing_image_paths(content)
            file_fixes += high_fixes
            self.fixes_applied['high'] += high_fixes
            
            content, high_fixes2 = self.fix_font_paths(content)
            file_fixes += high_fixes2
            self.fixes_applied['high'] += high_fixes2
            
            content, medium_fixes = self.fix_navigation_structure_issues(content)
            file_fixes += medium_fixes
            self.fixes_applied['medium'] += medium_fixes
            
            content, low_fixes = self.remove_wordpress_cache_references(content)
            file_fixes += low_fixes
            self.fixes_applied['low'] += low_fixes
            
            # Write file if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  💾 Saved {file_fixes} fixes")
            else:
                print("  ℹ️  No fixes needed")
                
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
    
    def run(self):
        """Run the comprehensive fix process"""
        print("🚀 Starting Comprehensive 404 Error Fix")
        print("=" * 50)
        
        html_files = self.find_html_files()
        print(f"Found {len(html_files)} HTML files to process")
        
        for file_path in html_files:
            self.process_file(file_path)
            self.files_processed += 1
        
        self.print_summary()
    
    def print_summary(self):
        """Print summary of fixes applied"""
        print("\n" + "=" * 50)
        print("📊 SUMMARY OF FIXES APPLIED")
        print("=" * 50)
        
        total_fixes = sum(self.fixes_applied.values())
        
        print(f"Files processed: {self.files_processed}")
        print(f"Total fixes applied: {total_fixes}")
        print()
        print("Fixes by priority:")
        print(f"  🔴 Critical: {self.fixes_applied['critical']} (GTM, malformed URLs)")
        print(f"  🟠 High:     {self.fixes_applied['high']} (images, fonts)")
        print(f"  🟡 Medium:   {self.fixes_applied['medium']} (navigation)")
        print(f"  🔵 Low:      {self.fixes_applied['low']} (cache cleanup)")
        
        if total_fixes > 0:
            print(f"\n✅ SUCCESS: Applied {total_fixes} fixes across {self.files_processed} files!")
            print("\n🔍 Next steps:")
            print("1. Test the site functionality")
            print("2. Re-run Screaming Frog to verify fixes")
            print("3. Check critical pages manually")
        else:
            print("\nℹ️  No issues found to fix")


if __name__ == "__main__":
    fixer = ComprehensiveLinkFixer()
    fixer.run() 