#!/usr/bin/env python3
"""
Service Page Generator for Alexandria Dental Health
Combines WordPress XML metadata with clean HTML content extraction
"""

import xml.etree.ElementTree as ET
import re
import yaml
from pathlib import Path
from html import unescape
from datetime import datetime
import argparse
from bs4 import BeautifulSoup


class ServicePageGenerator:
    def __init__(self, xml_file, content_dir="."):
        self.xml_file = xml_file
        self.content_dir = Path(content_dir)
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        
        # WordPress namespace
        self.wp_ns = '{http://wordpress.org/export/1.2/}'
        
        # Field mappings and patterns
        self.service_patterns = [
            'invisalign', 'dental-crowns', 'dental-bridges', 'dental-implants',
            'veneers', 'teeth-whitening', 'root-canal', 'dentures', 'family-dentist'
        ]
        
        self.image_mapping = {
            '../wp-content/uploads/': '/images/',
            'http://alexandriadentalhealthcom.local/wp-content/uploads/': '/images/',
            'https://www.alexandriadentalhealth.com/wp-content/uploads/': '/images/',
            '../images/': '/images/',
            'wp-content/uploads/': '/images/'
        }

    def extract_service_pages(self):
        """Extract all service pages from WordPress XML"""
        service_pages = []
        
        for item in self.root.findall('.//item'):
            post_type = item.find(f'.//{self.wp_ns}post_type')
            post_name = item.find(f'.//{self.wp_ns}post_name')
            status = item.find(f'.//{self.wp_ns}status')
            
            if (post_type is not None and 
                post_type.text == 'page' and 
                status is not None and 
                status.text == 'publish' and
                post_name is not None):
                
                # Check if this looks like a service page
                page_name = post_name.text.lower()
                if any(pattern in page_name for pattern in self.service_patterns):
                    # Check if corresponding HTML file exists
                    html_file = self.content_dir / page_name / "index.html"
                    if html_file.exists():
                        service_pages.append(self.parse_service_page(item, html_file))
                    else:
                        print(f"⚠️  HTML file not found for {page_name}: {html_file}")
        
        return service_pages

    def parse_service_page(self, xml_item, html_file):
        """Parse service page combining XML metadata with HTML content"""
        
        # Extract metadata from XML
        title = self.get_text(xml_item.find('.//title'))
        excerpt = self.get_text(xml_item.find('.//excerpt:encoded', {'excerpt': 'http://wordpress.org/export/1.2/excerpt/'}))
        post_name = self.get_text(xml_item.find(f'.//{self.wp_ns}post_name'))
        
        # Extract clean content from HTML file
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse HTML and extract main content
        soup = BeautifulSoup(html_content, 'html.parser')
        main_content = self.extract_main_content(soup)
        
        # Extract structured data from clean HTML
        benefits = self.extract_benefits_from_html(soup)
        process_steps = self.extract_process_steps_from_html(soup)
        faq = self.extract_faq_from_html(soup)
        investment = self.extract_investment_from_html(soup)
        hero_image = self.extract_hero_image_from_html(soup)
        
        # Generate service metadata
        service_data = {
            'layout': 'layouts/service.njk',
            'title': self.clean_title(title),
            'subtitle': self.generate_subtitle(title, main_content),
            'description': excerpt or self.generate_description(main_content),
            'keywords': self.generate_keywords(title, main_content),
            'heroImage': hero_image,
            'heroImageAlt': self.generate_image_alt(title),
            'permalink': f'/{post_name}/',
            'ctaText': self.generate_cta_text(title),
            'ctaLink': '/contact-us/',
            'tags': ['services', self.determine_category(title, main_content)]
        }
        
        # Add extracted structured data
        if benefits:
            service_data['benefits'] = benefits
        if process_steps:
            service_data['process_steps'] = process_steps
        if investment:
            service_data['investment'] = investment
        if faq:
            service_data['faq'] = faq
            
        # Add related services (placeholder for now)
        service_data['related_services'] = []
        
        return {
            'data': service_data,
            'content': main_content,
            'filename': f'{post_name}.md'
        }

    def extract_main_content(self, soup):
        """Extract main content from HTML, starting from fl-content-full container"""
        
        # Find the main content container
        main_container = soup.find('div', class_='fl-content-full')
        if not main_container:
            # Fallback to fl-rich-text if no main container found
            main_container = soup.find('div', class_='fl-rich-text')
        
        if not main_container:
            return "Content not found"
        
        # Extract text content while preserving some structure
        content_parts = []
        
        # Process each element
        for element in main_container.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'li']):
            if element.name.startswith('h'):
                # Headers
                level = '#' * int(element.name[1])
                content_parts.append(f"\n{level} {element.get_text().strip()}\n")
            elif element.name == 'p':
                # Paragraphs
                text = element.get_text().strip()
                if text:
                    content_parts.append(f"{text}\n")
            elif element.name in ['ul', 'ol']:
                # Lists
                content_parts.append("")
                for li in element.find_all('li'):
                    content_parts.append(f"- {li.get_text().strip()}")
                content_parts.append("")
        
        # Clean up the content
        content = '\n'.join(content_parts)
        content = re.sub(r'\n{3,}', '\n\n', content)  # Max 2 consecutive newlines
        content = content.strip()
        
        return content

    def extract_benefits_from_html(self, soup):
        """Extract benefits from HTML structure"""
        benefits = []
        
        # Look for list items that could be benefits
        for ul in soup.find_all('ul'):
            parent_text = ""
            if ul.find_previous(['h2', 'h3', 'p']):
                parent_text = ul.find_previous(['h2', 'h3', 'p']).get_text().lower()
            
            # Check if this list is likely benefits
            if any(keyword in parent_text for keyword in ['benefit', 'advantage', 'why choose', 'includes']):
                for li in ul.find_all('li')[:6]:  # Max 6 benefits
                    benefit_text = li.get_text().strip()
                    if benefit_text and len(benefit_text) > 10:
                        benefits.append(benefit_text)
                break
        
        return benefits if benefits else None

    def extract_process_steps_from_html(self, soup):
        """Extract process steps from HTML headings and content"""
        steps = []
        
        # Look for numbered headings or step patterns
        all_headings = soup.find_all(['h2', 'h3', 'h4'])
        
        for i, heading in enumerate(all_headings):
            heading_text = heading.get_text().strip()
            
            # Check if this looks like a step
            if (re.search(r'\d+\.|\bstep\b|process|procedure', heading_text.lower()) or
                any(word in heading_text.lower() for word in ['consultation', 'preparation', 'treatment', 'placement', 'recovery'])):
                
                # Get the description (next paragraph or content)
                description = ""
                next_elem = heading.find_next_sibling(['p', 'div'])
                if next_elem:
                    description = next_elem.get_text().strip()[:200] + "..." if len(next_elem.get_text()) > 200 else next_elem.get_text().strip()
                
                if description:
                    steps.append({
                        'title': heading_text,
                        'description': description
                    })
                
                if len(steps) >= 4:  # Max 4 steps
                    break
        
        return steps if steps else None

    def extract_faq_from_html(self, soup):
        """Extract FAQ from HTML - this might be in a different structure"""
        # For now, return None as FAQ might be handled separately
        # We can enhance this based on specific FAQ structures found
        return None

    def extract_investment_from_html(self, soup):
        """Extract pricing from HTML content"""
        investment = {}
        
        # Get all text content
        all_text = soup.get_text()
        
        # Look for pricing patterns
        price_patterns = [
            r'\$[\d,]+(?:\s*[-–]\s*\$[\d,]+)?(?:\s*per\s+\w+)?',
            r'(?:cost|price|fee)s?[:\s]+\$[\d,]+',
            r'starting\s+(?:at|from)\s+\$[\d,]+'
        ]
        
        prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            prices.extend(matches)
        
        if prices:
            if len(prices) >= 2:
                investment['primary'] = prices[0]
                investment['secondary'] = prices[1]
            else:
                investment['primary'] = prices[0]
            
            investment['financing'] = "Payment plans available"
            return investment
        
        return None

    def extract_hero_image_from_html(self, soup):
        """Extract hero image from HTML"""
        
        # Look for the main image (usually the first large image)
        img_tags = soup.find_all('img')
        
        for img in img_tags:
            src = img.get('src') or img.get('data-src')
            if src:
                # Skip small images, icons, logos
                width = img.get('width')
                height = img.get('height')
                
                # Skip if clearly a small image/icon
                if width and height:
                    try:
                        if int(width) < 200 or int(height) < 100:
                            continue
                    except:
                        pass
                
                # Convert WordPress paths
                for wp_path, new_path in self.image_mapping.items():
                    src = src.replace(wp_path, new_path)
                
                # Return first suitable image
                return src
        
        return "/images/services/default-hero.webp"

    def clean_title(self, title):
        """Clean WordPress title"""
        if not title:
            return "Service Page"
        # Remove HTML entities and extra text
        title = unescape(title)
        title = re.sub(r'\s+in\s+Alexandria\s+VA\s*$', '', title, flags=re.IGNORECASE)
        return title.strip()

    def generate_subtitle(self, title, content):
        """Generate subtitle from title and content"""
        service_name = self.clean_title(title)
        
        subtitle_patterns = {
            'invisalign': 'Clear Aligners for a Discreet, Confident Smile',
            'dental-crowns': 'Same-Day CEREC Crowns for Immediate Restoration',
            'dental-bridges': 'Replace Missing Teeth with Permanent Fixed Bridges',
            'dental-implants': 'Permanent, Natural-Looking Tooth Replacement',
            'veneers': 'Transform Your Smile with Custom Ceramic Veneers',
            'teeth-whitening': 'Professional Whitening for a Brighter, Confident Smile',
            'root-canal': 'Pain-Free Root Canal Treatment to Save Your Natural Teeth',
            'dentures': 'Restore Your Smile with Custom Full & Partial Dentures',
            'family-dentist': 'Comprehensive Dental Care for the Whole Family'
        }
        
        for key, subtitle in subtitle_patterns.items():
            if key in service_name.lower():
                return subtitle
        
        return f"Professional {service_name} in Alexandria VA"

    def generate_description(self, content):
        """Generate meta description from content"""
        if not content:
            return "Professional dental services at Alexandria Dental Health & Smile Studio."
        
        # Take first sentence or paragraph
        first_para = content.split('\n\n')[0] if content else ""
        first_sentence = first_para.split('.')[0] if first_para else ""
        
        if len(first_sentence) > 50 and len(first_sentence) < 160:
            return first_sentence + "."
        
        return "Professional dental services at Alexandria Dental Health & Smile Studio."

    def generate_keywords(self, title, content):
        """Generate SEO keywords"""
        service_name = self.clean_title(title).lower()
        base_keywords = f"{service_name} Alexandria VA, {service_name}"
        
        # Add specific keywords based on service
        keyword_map = {
            'invisalign': 'clear braces, invisible aligners',
            'dental crowns': 'CEREC crowns, same-day crowns',
            'dental bridges': 'tooth replacement, missing teeth',
            'dental implants': 'tooth replacement, implant dentist',
            'veneers': 'cosmetic dentistry, smile makeover',
            'teeth whitening': 'professional whitening, Opalescence',
            'root canal': 'endodontic treatment, tooth pain relief',
            'dentures': 'partial dentures, implant-supported dentures',
            'family dentist': 'pediatric dentist, children\'s dental care'
        }
        
        for key, additional in keyword_map.items():
            if key in service_name:
                base_keywords += f", {additional}"
                break
        
        return base_keywords

    def generate_image_alt(self, title):
        """Generate alt text for hero image"""
        service_name = self.clean_title(title)
        return f"{service_name} Treatment at Alexandria Dental Health & Smile Studio"

    def generate_cta_text(self, title):
        """Generate CTA button text"""
        service_name = self.clean_title(title)
        
        cta_map = {
            'invisalign': 'Schedule Invisalign Consultation',
            'dental crowns': 'Schedule Crown Consultation',
            'dental bridges': 'Schedule Bridge Consultation',
            'dental implants': 'Schedule Implant Consultation',
            'veneers': 'Schedule Veneers Consultation',
            'teeth whitening': 'Schedule Whitening Consultation',
            'root canal': 'Schedule Emergency Appointment',
            'dentures': 'Schedule Denture Consultation',
            'family dentist': 'Schedule Family Appointment'
        }
        
        for key, cta in cta_map.items():
            if key in service_name.lower():
                return cta
        
        return "Schedule Consultation"

    def determine_category(self, title, content):
        """Determine service category"""
        service_name = self.clean_title(title).lower()
        
        categories = {
            'cosmetic': ['invisalign', 'veneers', 'teeth whitening', 'cosmetic'],
            'restorative': ['dental crowns', 'dental bridges', 'dental implants', 'root canal', 'dentures'],
            'family': ['family dentist', 'pediatric', 'children']
        }
        
        for category, keywords in categories.items():
            if any(keyword in service_name for keyword in keywords):
                return category
        
        return 'general'

    def get_text(self, element):
        """Safely get text from XML element"""
        return element.text if element is not None else None

    def save_service_page(self, service_page, output_dir):
        """Save service page to markdown file"""
        output_path = Path(output_dir) / service_page['filename']
        
        # Create YAML frontmatter
        yaml_content = yaml.dump(service_page['data'], default_flow_style=False, allow_unicode=True)
        
        # Create full markdown content
        full_content = f"---\n{yaml_content}---\n\n{service_page['content']}"
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"✅ Generated: {output_path}")

    def generate_all_service_pages(self, output_dir="src/services", dry_run=False):
        """Generate all service pages from XML + HTML"""
        service_pages = self.extract_service_pages()
        
        print(f"Found {len(service_pages)} service pages with matching HTML files")
        
        if dry_run:
            print("\n🔍 DRY RUN - Preview of what would be generated:")
            for page in service_pages:
                print(f"  - {page['filename']}: {page['data']['title']}")
                if page['data'].get('benefits'):
                    print(f"    ✅ Benefits: {len(page['data']['benefits'])} items")
                if page['data'].get('process_steps'):
                    print(f"    ✅ Process Steps: {len(page['data']['process_steps'])} steps")
                if page['data'].get('investment'):
                    print(f"    ✅ Investment: {page['data']['investment']['primary']}")
            return
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate pages
        for page in service_pages:
            self.save_service_page(page, output_dir)
        
        print(f"\n🎉 Generated {len(service_pages)} service pages!")


def main():
    parser = argparse.ArgumentParser(description='Generate service pages from WordPress XML + HTML files')
    parser.add_argument('xml_file', help='Path to WordPress XML export file')
    parser.add_argument('--content-dir', '-c', default='.', help='Directory containing service HTML folders')
    parser.add_argument('--output', '-o', default='src/services', help='Output directory')
    parser.add_argument('--dry-run', action='store_true', help='Preview without generating files')
    parser.add_argument('--test-page', help='Generate only one page for testing')
    
    args = parser.parse_args()
    
    generator = ServicePageGenerator(args.xml_file, args.content_dir)
    
    if args.test_page:
        # Test mode - generate one page
        service_pages = generator.extract_service_pages()
        test_page = next((page for page in service_pages if args.test_page in page['filename']), None)
        
        if test_page:
            print(f"🧪 Testing with: {test_page['filename']}")
            if not args.dry_run:
                generator.save_service_page(test_page, args.output)
            else:
                print(f"Preview: {test_page['data']}")
                print(f"Content preview: {test_page['content'][:500]}...")
        else:
            print(f"❌ Test page '{args.test_page}' not found")
    else:
        generator.generate_all_service_pages(args.output, args.dry_run)


if __name__ == "__main__":
    main() 