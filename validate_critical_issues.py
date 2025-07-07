#!/usr/bin/env python3
"""
Targeted validation script for WordPress-to-static conversion issues
Focuses on specific problems: canonicals, corrupted SVGs, hardcoded URLs, missing assets
"""
import os
import re
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
import argparse

class SiteValidator:
    def __init__(self, site_root):
        self.site_root = Path(site_root)
        self.issues = {
            'canonical_errors': [],
            'corrupted_svgs': [],
            'hardcoded_domains': [],
            'missing_assets': [],
            'navigation_issues': []
        }
        
    def validate_canonicals(self, html_content, file_path):
        """Check for incorrect canonical URLs"""
        canonical_pattern = r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']'
        matches = re.findall(canonical_pattern, html_content, re.IGNORECASE)
        
        for canonical_url in matches:
            # Check for incorrect canonical patterns
            if canonical_url in ['index.html', '', '../index.html']:
                self.issues['canonical_errors'].append({
                    'file': str(file_path),
                    'issue': f'Invalid canonical URL: {canonical_url}',
                    'recommended': self._get_proper_canonical(file_path)
                })
            elif canonical_url.startswith('index.html'):
                self.issues['canonical_errors'].append({
                    'file': str(file_path),
                    'issue': f'Relative canonical URL: {canonical_url}',
                    'recommended': self._get_proper_canonical(file_path)
                })
    
    def _get_proper_canonical(self, file_path):
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
    
    def validate_svgs(self, html_content, file_path):
        """Check for corrupted SVG data URIs"""
        # Pattern for SVG data URIs
        svg_pattern = r'data:image/svg\+xml[^"\']*'
        matches = re.findall(svg_pattern, html_content)
        
        for svg_data in matches:
            # Check for corrupted patterns
            if 'wp-content' in svg_data or 'plugins' in svg_data:
                self.issues['corrupted_svgs'].append({
                    'file': str(file_path),
                    'issue': 'SVG data URI has file path concatenated',
                    'corrupted_data': svg_data[:100] + '...' if len(svg_data) > 100 else svg_data
                })
            
            # Check for empty viewBox
            if 'viewBox=%220%200%20%20%22' in svg_data:
                self.issues['corrupted_svgs'].append({
                    'file': str(file_path),
                    'issue': 'SVG data URI has empty viewBox',
                    'corrupted_data': svg_data[:100] + '...' if len(svg_data) > 100 else svg_data
                })
    
    def validate_hardcoded_domains(self, html_content, file_path):
        """Check for hardcoded domain references"""
        domain_patterns = [
            r'https://www\.alexandriadentalhealth\.com',
            r'http://www\.alexandriadentalhealth\.com',
            r'www\.alexandriadentalhealth\.com'
        ]
        
        for pattern in domain_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                self.issues['hardcoded_domains'].append({
                    'file': str(file_path),
                    'count': len(matches),
                    'pattern': pattern,
                    'issue': 'Hardcoded domain reference will break when moved'
                })
    
    def validate_assets(self, html_content, file_path):
        """Check for missing critical assets"""
        # Check for essential asset patterns
        asset_patterns = {
            'css': r'<link[^>]*href=["\']([^"\']*\.css)["\']',
            'js': r'<script[^>]*src=["\']([^"\']*\.js)["\']',
            'images': r'<img[^>]*src=["\']([^"\']*\.(jpg|jpeg|png|gif|webp|svg))["\']',
            'fonts': r'url\(["\']?([^"\']*\.(woff2?|eot|ttf))["\']?\)'
        }
        
        for asset_type, pattern in asset_patterns.items():
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                asset_url = match if isinstance(match, str) else match[0]
                
                # Skip data URIs and external URLs
                if asset_url.startswith(('data:', 'http://', 'https://', '//')):
                    continue
                
                # Resolve relative path
                if asset_url.startswith('/'):
                    asset_path = self.site_root / asset_url.lstrip('/')
                else:
                    asset_path = file_path.parent / asset_url
                
                # Check if asset exists
                if not asset_path.exists():
                    self.issues['missing_assets'].append({
                        'file': str(file_path),
                        'asset_type': asset_type,
                        'missing_asset': asset_url,
                        'resolved_path': str(asset_path)
                    })
    
    def validate_navigation(self, html_content, file_path):
        """Check for navigation issues"""
        # Check for broken internal links
        link_pattern = r'<a[^>]*href=["\']([^"\']*)["\']'
        matches = re.findall(link_pattern, html_content, re.IGNORECASE)
        
        for link in matches:
            # Skip external links and special URLs
            if link.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'javascript:')):
                continue
            
            # Check for problematic link patterns
            if link.endswith('.php'):
                self.issues['navigation_issues'].append({
                    'file': str(file_path),
                    'issue': 'Link to PHP file in static site',
                    'link': link
                })
    
    def validate_file(self, file_path):
        """Validate a single HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            self.validate_canonicals(content, file_path)
            self.validate_svgs(content, file_path)
            self.validate_hardcoded_domains(content, file_path)
            self.validate_assets(content, file_path)
            self.validate_navigation(content, file_path)
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    def validate_site(self):
        """Validate all HTML files in the site"""
        html_files = list(self.site_root.rglob("*.html"))
        
        print(f"Validating {len(html_files)} HTML files...")
        
        for i, html_file in enumerate(html_files, 1):
            if i % 50 == 0:
                print(f"Processed {i}/{len(html_files)} files...")
            self.validate_file(html_file)
        
        return self.issues
    
    def generate_report(self, output_file=None):
        """Generate validation report"""
        total_issues = sum(len(issues) for issues in self.issues.values())
        
        report = {
            'summary': {
                'total_issues': total_issues,
                'canonical_errors': len(self.issues['canonical_errors']),
                'corrupted_svgs': len(self.issues['corrupted_svgs']),
                'hardcoded_domains': len(self.issues['hardcoded_domains']),
                'missing_assets': len(self.issues['missing_assets']),
                'navigation_issues': len(self.issues['navigation_issues'])
            },
            'details': self.issues
        }
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"Report saved to {output_file}")
        
        return report
    
    def print_summary(self):
        """Print a summary of found issues"""
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        
        summary = {
            'Canonical URL Errors': len(self.issues['canonical_errors']),
            'Corrupted SVG Data URIs': len(self.issues['corrupted_svgs']),
            'Hardcoded Domain References': len(self.issues['hardcoded_domains']),
            'Missing Assets': len(self.issues['missing_assets']),
            'Navigation Issues': len(self.issues['navigation_issues'])
        }
        
        total = sum(summary.values())
        print(f"Total Issues Found: {total}")
        print("-" * 30)
        
        for issue_type, count in summary.items():
            status = "❌" if count > 0 else "✅"
            print(f"{status} {issue_type}: {count}")
        
        if total > 0:
            print(f"\n⚠️  Priority Issues to Fix:")
            if self.issues['canonical_errors']:
                print(f"   • {len(self.issues['canonical_errors'])} canonical URL errors")
            if self.issues['corrupted_svgs']:
                print(f"   • {len(self.issues['corrupted_svgs'])} corrupted SVG data URIs")
            if self.issues['hardcoded_domains']:
                print(f"   • {len(self.issues['hardcoded_domains'])} hardcoded domain references")

def main():
    parser = argparse.ArgumentParser(description='Validate critical WordPress-to-static conversion issues')
    parser.add_argument('site_root', help='Path to the site root directory')
    parser.add_argument('--output', '-o', help='Output JSON report file')
    parser.add_argument('--test-file', help='Test on a single file instead of entire site')
    
    args = parser.parse_args()
    
    validator = SiteValidator(args.site_root)
    
    if args.test_file:
        print(f"Testing single file: {args.test_file}")
        test_path = Path(args.site_root) / args.test_file
        if test_path.exists():
            validator.validate_file(test_path)
        else:
            print(f"Test file not found: {test_path}")
            return
    else:
        validator.validate_site()
    
    validator.print_summary()
    
    if args.output or not args.test_file:
        output_file = args.output or 'validation_report.json'
        validator.generate_report(output_file)

if __name__ == "__main__":
    main() 