#!/usr/bin/env python3
"""
Smart Comparison Script
Analyzes differences between live site and scraped version to identify real issues
"""
import re
from pathlib import Path
from difflib import unified_diff

def analyze_files():
    live_file = Path('gum-disease-symptoms-TEST/index-LIVE.html')
    scraped_file = Path('gum-disease-symptoms-TEST/index.html')
    
    print("🔍 SMART COMPARISON ANALYSIS")
    print("="*50)
    
    # Read both files
    with open(live_file, 'r', encoding='utf-8', errors='ignore') as f:
        live_content = f.read()
    
    with open(scraped_file, 'r', encoding='utf-8', errors='ignore') as f:
        scraped_content = f.read()
    
    print(f"📄 Live site: {len(live_content):,} characters")
    print(f"📄 Scraped:   {len(scraped_content):,} characters")
    print(f"📊 Difference: {len(live_content) - len(scraped_content):,} characters")
    
    print("\n🎯 ANALYSIS RESULTS:")
    print("-" * 30)
    
    # 1. Canonical URL comparison
    print("\n1️⃣ CANONICAL URL CHECK:")
    live_canonical = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']', live_content, re.IGNORECASE)
    scraped_canonical = re.findall(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']', scraped_content, re.IGNORECASE)
    
    if live_canonical:
        print(f"   Live:    {live_canonical[0]}")
    if scraped_canonical:
        print(f"   Scraped: {scraped_canonical[0]}")
        if scraped_canonical[0] == 'index.html':
            print("   ✅ ISSUE CONFIRMED: Scraped has 'index.html' canonical")
    
    # 2. SVG Data URI comparison
    print("\n2️⃣ SVG DATA URI CHECK:")
    live_svgs = re.findall(r'data:image/svg\+xml[^"\']*', live_content)
    scraped_svgs = re.findall(r'data:image/svg\+xml[^"\']*', scraped_content)
    
    print(f"   Live SVGs:    {len(live_svgs)}")
    print(f"   Scraped SVGs: {len(scraped_svgs)}")
    
    # Check for corrupted SVGs in scraped version
    corrupted_svgs = []
    for i, svg in enumerate(scraped_svgs):
        if 'wp-content' in svg or 'viewBox=%220%200%20%20%22' in svg:
            corrupted_svgs.append(i)
    
    if corrupted_svgs:
        print(f"   ⚠️  Corrupted SVGs in scraped: {len(corrupted_svgs)}")
        for i in corrupted_svgs[:3]:  # Show first 3
            print(f"      #{i+1}: {scraped_svgs[i][:80]}...")
    else:
        print("   ✅ No obviously corrupted SVGs found")
    
    # 3. Domain references
    print("\n3️⃣ DOMAIN REFERENCE CHECK:")
    live_domains = len(re.findall(r'https://www\.alexandriadentalhealth\.com', live_content, re.IGNORECASE))
    scraped_domains = len(re.findall(r'https://www\.alexandriadentalhealth\.com', scraped_content, re.IGNORECASE))
    
    print(f"   Live domain refs:    {live_domains}")
    print(f"   Scraped domain refs: {scraped_domains}")
    
    if scraped_domains > 0:
        print("   ⚠️  Scraped version has hardcoded domain references")
    
    # 4. Font Awesome / Glyph analysis
    print("\n4️⃣ FONT AWESOME / GLYPH CHECK:")
    fa_patterns = [
        'font-awesome',
        'fa-',
        'fontawesome',
        '.fa:',
        'fa-solid'
    ]
    
    for pattern in fa_patterns:
        live_count = len(re.findall(pattern, live_content, re.IGNORECASE))
        scraped_count = len(re.findall(pattern, scraped_content, re.IGNORECASE))
        if live_count != scraped_count:
            print(f"   {pattern}: Live={live_count}, Scraped={scraped_count}")
    
    # 5. Special Offers button analysis
    print("\n5️⃣ SPECIAL OFFERS BUTTON CHECK:")
    live_special = re.findall(r'special.{0,20}offer', live_content, re.IGNORECASE)
    scraped_special = re.findall(r'special.{0,20}offer', scraped_content, re.IGNORECASE)
    
    print(f"   Live special offers refs:    {len(live_special)}")
    print(f"   Scraped special offers refs: {len(scraped_special)}")
    
    # 6. Critical CSS/JS differences
    print("\n6️⃣ CRITICAL ASSET CHECK:")
    css_pattern = r'<link[^>]*\.css[^>]*>'
    js_pattern = r'<script[^>]*\.js[^>]*>'
    
    live_css = len(re.findall(css_pattern, live_content, re.IGNORECASE))
    scraped_css = len(re.findall(css_pattern, scraped_content, re.IGNORECASE))
    live_js = len(re.findall(js_pattern, live_content, re.IGNORECASE))
    scraped_js = len(re.findall(js_pattern, scraped_content, re.IGNORECASE))
    
    print(f"   CSS files: Live={live_css}, Scraped={scraped_css}")
    print(f"   JS files:  Live={live_js}, Scraped={scraped_js}")
    
    # Summary and recommendations
    print("\n🎯 RECOMMENDATIONS:")
    print("-" * 20)
    
    issues_found = []
    
    if scraped_canonical and scraped_canonical[0] == 'index.html':
        issues_found.append("✅ FIX: Canonical URL (safe)")
    
    if scraped_domains > 0:
        issues_found.append("✅ FIX: Hardcoded domain references (safe)")
    
    if corrupted_svgs:
        issues_found.append("⚠️  INVESTIGATE: SVG data URIs (risky - needs careful analysis)")
    
    if live_css != scraped_css or live_js != scraped_js:
        issues_found.append("🚨 CRITICAL: CSS/JS file differences may cause layout issues")
    
    if not issues_found:
        print("✅ No obvious issues found between live and scraped versions")
    else:
        for issue in issues_found:
            print(f"   {issue}")
    
    return {
        'canonical_needs_fix': scraped_canonical and scraped_canonical[0] == 'index.html',
        'domains_need_fix': scraped_domains > 0,
        'svg_issues': len(corrupted_svgs),
        'asset_differences': live_css != scraped_css or live_js != scraped_js
    }

if __name__ == "__main__":
    results = analyze_files()
    
    print(f"\n🛠️  NEXT STEPS:")
    if results['canonical_needs_fix'] or results['domains_need_fix']:
        print("   1. Create MINIMAL fix script for canonical + domains only")
        print("   2. Test the minimal fix")
        print("   3. Investigate SVG/asset issues separately")
    else:
        print("   1. The scraped version may already be working")
        print("   2. Test the original scraped version first") 