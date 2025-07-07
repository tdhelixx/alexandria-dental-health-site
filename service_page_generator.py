#!/usr/bin/env python3
"""
Service Page Generator for Alexandria Dental Health
Combines WordPress XML metadata with clean HTML content extraction
Enhanced for CloudCannon visual editing optimization
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
        
        # Smart hero image mapping based on service type and available images
        self.hero_image_mapping = {
            # Cosmetic services
            'invisalign': '/images/services/woman-hands-by-face-smiling.webp',
            'veneers': '/images/cosmetic/Dentist-Woman-Close-Up-Of-Pretty-Smile-CS1.webp', 
            'getting-veneers': '/images/cosmetic/Dentist-Woman-Close-Up-Of-Pretty-Smile-CS1.webp',
            'teeth-whitening': '/images/services/couple-younger-smiling.webp',
            'cosmetic': '/images/cosmetic/Woman-Cosmetic-Dentistry-Smiling-CS1.webp',
            
            # Restorative services  
            'dental-implants': '/images/services/dental-implants-hero.webp',
            'about-dental-implants': '/images/restorative/Dentist-Alexandria-VA-Dental-Implants-FC.webp',
            'implant-supported-dentures': '/images/restorative/man-older-dentures-smiling-at-dentist.jpg',
            'dentures': '/images/restorative/man-older-dentures-smiling-at-dentist.jpg',
            'dentures-cleaning': '/images/restorative/man-older-dentures-smiling-at-dentist.jpg',
            'dental-crowns': '/images/restorative/Dentist-Senior-Couple-Outside-Smiling-CS1.webp',
            'dental-bridges': '/images/cosmetic/Dentist-Woman-Close-Up-Of-Pretty-Smile-CS1.webp',
            'root-canal': '/images/restorative/Dentist-Alexandria-VA-Root-Canal-Therapy.webp',
            
            # Family services
            'family-dentist': '/images/family/Family-Mom-Dad-Kids-Smiling-CS1.webp',
            'family': '/images/family/Family-Mom-Dad-Kids-Smiling-CS1.webp'
        }
        
        self.image_mapping = {
            '../wp-content/uploads/': '/images/',
            'http://alexandriadentalhealthcom.local/wp-content/uploads/': '/images/',
            'https://www.alexandriadentalhealth.com/wp-content/uploads/': '/images/',
            '../images/': '/images/',
            'wp-content/uploads/': '/images/',
            '/wp-content/uploads/': '/images/'
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
        hero_image = self.get_smart_hero_image(post_name, soup)
        
        # Generate service metadata with CloudCannon optimization
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
        
        # Add CloudCannon visual editing fields
        service_data.update(self.add_cloudcannon_fields(post_name, title))
        
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
        service_data['related_services'] = self.generate_related_services(post_name)
        
        return {
            'data': service_data,
            'content': main_content,
            'filename': f'{post_name}.md'
        }

    def get_smart_hero_image(self, post_name, soup):
        """Get hero image using smart mapping first, then HTML extraction"""
        
        # First, try smart mapping based on service type
        for service_key, image_path in self.hero_image_mapping.items():
            if service_key in post_name.lower():
                return image_path
        
        # Fallback to HTML extraction but with better filtering
        img_tags = soup.find_all('img')
        
        for img in img_tags:
            src = img.get('src') or img.get('data-src')
            if src:
                # Skip logos, headers, and small images
                if any(skip in src.lower() for skip in ['logo', 'header', 'footer', 'icon']):
                    continue
                
                # Skip clearly small images
                width = img.get('width')
                height = img.get('height')
                if width and height:
                    try:
                        if int(width) < 200 or int(height) < 100:
                            continue
                    except:
                        pass
                
                # Convert WordPress paths
                for wp_path, new_path in self.image_mapping.items():
                    src = src.replace(wp_path, new_path)
                
                return src
        
        # Final fallback based on category
        category = self.determine_category_from_name(post_name)
        fallback_images = {
            'cosmetic': '/images/cosmetic/Woman-Cosmetic-Dentistry-Smiling-CS1.webp',
            'restorative': '/images/restorative/Dentist-Senior-Couple-Outside-Smiling-CS1.webp',
            'family': '/images/family/Family-Mom-Dad-Kids-Smiling-CS1.webp'
        }
        
        return fallback_images.get(category, '/images/cosmetic/Woman-Cosmetic-Dentistry-Smiling-CS1.webp')

    def add_cloudcannon_fields(self, post_name, title):
        """Add CloudCannon-specific visual editing fields"""
        
        fields = {
            # Visual editing support
            'editable_regions': ['hero', 'content', 'sidebar'],
            
            # SEO and social
            'social_image': self.get_smart_hero_image(post_name, None),
            'og_description': self.generate_description(""),
            
            # Page structure  
            'show_hero': True,
            'show_sidebar': True,
            'show_cta': True,
            
            # Content organization
            'content_sections': ['benefits', 'process', 'investment', 'faq'],
            
            # Navigation
            'in_nav': True,
            'nav_order': self.get_nav_order(post_name),
            
            # Page type
            'page_type': 'service'
        }
        
        return fields

    def get_nav_order(self, post_name):
        """Determine navigation order for service"""
        nav_order_map = {
            'invisalign': 1,
            'veneers': 2, 
            'teeth-whitening': 3,
            'dental-crowns': 4,
            'dental-bridges': 5,
            'dental-implants': 6,
            'dentures': 7,
            'root-canal-therapy': 8,
            'family-dentist': 9
        }
        
        for key, order in nav_order_map.items():
            if key in post_name:
                return order
        
        return 99  # Default for unlisted services

    def determine_category_from_name(self, post_name):
        """Determine category from post name alone"""
        cosmetic_services = ['invisalign', 'veneers', 'teeth-whitening', 'cosmetic']
        restorative_services = ['dental-crowns', 'dental-bridges', 'dental-implants', 'root-canal', 'dentures']
        family_services = ['family-dentist', 'pediatric', 'children']
        
        name_lower = post_name.lower()
        
        if any(service in name_lower for service in cosmetic_services):
            return 'cosmetic'
        elif any(service in name_lower for service in restorative_services):
            return 'restorative' 
        elif any(service in name_lower for service in family_services):
            return 'family'
        
        return 'general'

    def generate_related_services(self, post_name):
        """Generate related services based on category - always non-empty"""
        
        category = self.determine_category_from_name(post_name)
        
        related_map = {
            'cosmetic': [
                {'title': 'Porcelain Veneers', 'url': '/veneers/'},
                {'title': 'Invisalign Clear Braces', 'url': '/invisalign/'},
                {'title': 'Professional Teeth Whitening', 'url': '/teeth-whitening/'}
            ],
            'restorative': [
                {'title': 'Dental Implants', 'url': '/dental-implants/'},
                {'title': 'Dental Crowns', 'url': '/dental-crowns/'},
                {'title': 'Dental Bridges', 'url': '/dental-bridges/'}
            ],
            'family': [
                {'title': 'Dental Cleanings', 'url': '/dental-cleanings/'},
                {'title': 'Dental Exams', 'url': '/dental-exams/'},
                {'title': 'Cavity Treatment', 'url': '/dental-cavities-solutions/'}
            ]
        }
        
        related_services = related_map.get(category, [])
        
        # Remove self from related services
        current_url = f'/{post_name}/'
        filtered_services = [service for service in related_services if service['url'] != current_url]
        
        # Ensure we always have at least 2 related services for CloudCannon
        if len(filtered_services) < 2:
            # Add fallback services from other categories
            fallback_services = [
                {'title': 'Cosmetic Dentistry', 'url': '/cosmetic-dentistry/'},
                {'title': 'Restorative Dentistry', 'url': '/restorative/'},
                {'title': 'Family Dentistry', 'url': '/family-dentist/'},
                {'title': 'Emergency Dentistry', 'url': '/emergency-dental-information/'},
                {'title': 'Preventative Care', 'url': '/preventative/'}
            ]
            
            # Add fallback services until we have at least 2
            for service in fallback_services:
                if service['url'] != current_url and service not in filtered_services:
                    filtered_services.append(service)
                    if len(filtered_services) >= 2:
                        break
        
        # Limit to maximum 3 related services for clean UI
        return filtered_services[:3]

    def extract_main_content(self, soup):
        """Extract main content from HTML, starting from fl-content-full container"""
        
        # Find the main content container (improved selection)
        main_container = soup.find('div', class_='fl-content-full')
        if not main_container:
            # Try alternative containers
            main_container = soup.find('div', class_='fl-rich-text') or soup.find('div', class_='fl-post-content')
        
        if not main_container:
            return "Content not found"
        
        # Remove sidebar content
        sidebar_selectors = [
            '.fl-col-small',  # Sidebar columns
            '.uabb-creative-menu',  # Navigation menus
            '.fl-module-html',  # Sidebar widgets
            '.symptomhover',  # Special offer widgets
            'script'  # Scripts
        ]
        
        for selector in sidebar_selectors:
            for element in main_container.select(selector):
                element.decompose()
        
        # Extract text content while preserving structure
        content_parts = []
        
        # Process each element in order
        for element in main_container.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li', 'blockquote']):
            if element.name.startswith('h'):
                # Headers
                level = '#' * int(element.name[1])
                content_parts.append(f"\n{level} {element.get_text().strip()}\n")
            elif element.name == 'p':
                # Paragraphs
                text = element.get_text().strip()
                if text and len(text) > 10:  # Skip very short paragraphs
                    content_parts.append(f"{text}\n")
            elif element.name == 'blockquote':
                # Blockquotes
                text = element.get_text().strip()
                if text:
                    content_parts.append(f"> {text}\n")
            elif element.name in ['ul', 'ol']:
                # Lists (only if not already processed)
                if not any(ancestor.name in ['ul', 'ol'] for ancestor in element.parents):
                    content_parts.append("")
                    for li in element.find_all('li', recursive=False):
                        list_text = li.get_text().strip()
                        if list_text:
                            content_parts.append(f"- {list_text}")
                    content_parts.append("")
        
        # Clean up the content
        content = '\n'.join(content_parts)
        content = re.sub(r'\n{3,}', '\n\n', content)  # Max 2 consecutive newlines
        content = content.strip()
        
        return content

    def extract_benefits_from_html(self, soup):
        """Extract benefits from HTML structure with improved detection"""
        benefits = []
        
        # Look for various benefit patterns
        benefit_indicators = ['benefit', 'advantage', 'why choose', 'includes', 'features']
        
        # Check for lists near benefit headings
        for heading in soup.find_all(['h2', 'h3', 'h4']):
            heading_text = heading.get_text().lower()
            
            if any(indicator in heading_text for indicator in benefit_indicators):
                # Look for the next list after this heading
                next_list = heading.find_next(['ul', 'ol'])
                if next_list:
                    for li in next_list.find_all('li')[:6]:  # Max 6 benefits
                        benefit_text = li.get_text().strip()
                        if benefit_text and len(benefit_text) > 15:  # Substantial benefits only
                            benefits.append(benefit_text)
                    break
        
        # If no benefits found near headings, look for any substantial lists
        if not benefits:
            for ul in soup.find_all('ul'):
                # Skip navigation menus and small lists
                if ul.find_parent(['nav', 'footer']) or len(ul.find_all('li')) < 3:
                    continue
                
                potential_benefits = []
                for li in ul.find_all('li')[:6]:
                    benefit_text = li.get_text().strip()
                    if benefit_text and len(benefit_text) > 15:
                        potential_benefits.append(benefit_text)
                
                if len(potential_benefits) >= 3:  # At least 3 substantial items
                    benefits = potential_benefits
                    break
        
        return benefits if benefits else None

    def extract_process_steps_from_html(self, soup):
        """Extract process steps with improved detection"""
        steps = []
        
        # Look for step indicators in headings
        step_indicators = ['step', 'process', 'procedure', 'treatment', 'consultation', 'preparation', 'placement', 'recovery']
        
        all_headings = soup.find_all(['h2', 'h3', 'h4'])
        
        for heading in all_headings:
            heading_text = heading.get_text().strip()
            
            # Check if this looks like a step
            if (re.search(r'\d+\.|step\s+\d+|phase\s+\d+', heading_text.lower()) or
                any(indicator in heading_text.lower() for indicator in step_indicators)):
                
                # Get the description (next paragraph or content)
                description = ""
                next_elem = heading.find_next_sibling(['p', 'div'])
                if next_elem:
                    desc_text = next_elem.get_text().strip()
                    description = desc_text[:200] + "..." if len(desc_text) > 200 else desc_text
                
                if description and len(description) > 20:
                    steps.append({
                        'title': heading_text,
                        'description': description
                    })
                
                if len(steps) >= 4:  # Max 4 steps
                    break
        
        return steps if steps else None

    def extract_investment_from_html(self, soup):
        """Extract pricing with improved patterns"""
        investment = {}
        
        # Get all text content
        all_text = soup.get_text()
        
        # Enhanced pricing patterns
        price_patterns = [
            r'\$[\d,]+(?:\s*[-–]\s*\$[\d,]+)?(?:\s*per\s+\w+)?',
            r'(?:cost|price|fee|investment)s?[:\s]+\$[\d,]+',
            r'starting\s+(?:at|from)\s+\$[\d,]+',
            r'between\s+\$[\d,]+\s+(?:and|to)\s+\$[\d,]+',
            r'range\s+(?:from|between)\s+\$[\d,]+',
            r'\$[\d,]+\s*(?:to|[-–])\s*\$[\d,]+'
        ]
        
        prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            prices.extend(matches)
        
        if prices:
            # Clean and deduplicate prices
            unique_prices = list(dict.fromkeys(prices))  # Remove duplicates while preserving order
            
            if len(unique_prices) >= 2:
                investment['primary'] = unique_prices[0]
                investment['secondary'] = unique_prices[1]
            else:
                investment['primary'] = unique_prices[0]
            
            investment['financing'] = "Payment plans available"
            investment['note'] = "Prices may vary based on individual treatment needs"
            return investment
        
        return None

    def clean_title(self, title):
        """Clean WordPress title with better handling"""
        if not title:
            return "Service Page"
        
        # Remove HTML entities and extra text
        title = unescape(title)
        
        # Remove common WordPress suffixes
        suffixes_to_remove = [
            r'\s+in\s+Alexandria\s+VA\s*$',
            r'\s+Alexandria\s+VA\s*$', 
            r'\s+–\s+Alexandria.*$',
            r'\s+\|\s+Alexandria.*$'
        ]
        
        for suffix in suffixes_to_remove:
            title = re.sub(suffix, '', title, flags=re.IGNORECASE)
        
        return title.strip()

    def generate_subtitle(self, title, content):
        """Generate subtitle with enhanced mapping"""
        service_name = self.clean_title(title).lower()
        
        subtitle_patterns = {
            'invisalign': 'Clear Aligners for a Discreet, Confident Smile',
            'dental-crowns': 'Same-Day CEREC Crowns for Immediate Restoration', 
            'dental-bridges': 'Replace Missing Teeth with Permanent Fixed Bridges',
            'dental-implants': 'Permanent, Natural-Looking Tooth Replacement',
            'about-dental-implants': 'What to Expect from Your Dental Implant Journey',
            'implant-supported-dentures': 'All-on-Four® Fixed Denture Solutions',
            'veneers': 'Transform Your Smile with Custom Ceramic Veneers',
            'getting-veneers': 'Your Complete Guide to Porcelain Veneers',
            'teeth-whitening': 'Professional Whitening for a Brighter, Confident Smile',
            'root-canal': 'Pain-Free Root Canal Treatment to Save Your Natural Teeth',
            'root-canal-therapy': 'Advanced Endodontic Treatment for Lasting Relief',
            'root-canal-recovery': 'Your Guide to Comfortable Root Canal Healing',
            'root-canal-symptoms': 'Recognizing When You Need Root Canal Treatment',
            'dentures': 'Restore Your Smile with Custom Full & Partial Dentures',
            'dentures-cleaning': 'Expert Care Tips for Long-Lasting Dentures',
            'family-dentist': 'Comprehensive Dental Care for the Whole Family',
            'invisalign-teen': 'Clear Braces Designed Specifically for Teenagers'
        }
        
        # Check for exact matches first
        for key, subtitle in subtitle_patterns.items():
            if key in service_name or key.replace('-', ' ') in service_name:
                return subtitle
        
        # Fallback generation
        return f"Professional {self.clean_title(title)} in Alexandria VA"

    def generate_description(self, content):
        """Generate meta description with improved extraction"""
        if not content:
            return "Expert dental services at Alexandria Dental Health & Smile Studio. Dr. Mazhari provides comprehensive care in Alexandria VA."
        
        # Take first meaningful sentence
        sentences = content.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 50 and len(sentence) < 160:
                return sentence + "."
        
        # Fallback to first paragraph
        paragraphs = content.split('\n\n')
        if paragraphs and len(paragraphs[0]) < 160:
            return paragraphs[0].strip()
        
        return "Expert dental services at Alexandria Dental Health & Smile Studio. Dr. Mazhari provides comprehensive care in Alexandria VA."

    def generate_keywords(self, title, content):
        """Generate SEO keywords with enhanced mapping"""
        service_name = self.clean_title(title).lower()
        base_keywords = f"{service_name} Alexandria VA, {service_name}"
        
        # Enhanced keyword mapping
        keyword_map = {
            'invisalign': 'clear braces, invisible aligners, orthodontics',
            'dental crowns': 'CEREC crowns, same-day crowns, tooth restoration',
            'dental bridges': 'tooth replacement, missing teeth, fixed bridge',
            'dental implants': 'tooth replacement, implant dentist, permanent teeth',
            'veneers': 'cosmetic dentistry, smile makeover, porcelain veneers',
            'teeth whitening': 'professional whitening, Opalescence, smile brightening',
            'root canal': 'endodontic treatment, tooth pain relief, root canal therapy',
            'dentures': 'partial dentures, implant-supported dentures, tooth replacement',
            'family dentist': 'pediatric dentist, children\'s dental care, family dental'
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
        """Generate CTA button text with enhanced mapping"""
        service_name = self.clean_title(title).lower()
        
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
            if key in service_name:
                return cta
        
        return "Schedule Consultation"

    def determine_category(self, title, content):
        """Determine service category with improved logic"""
        service_name = self.clean_title(title).lower()
        
        categories = {
            'cosmetic': ['invisalign', 'veneers', 'teeth whitening', 'cosmetic', 'smile makeover'],
            'restorative': ['dental crowns', 'dental bridges', 'dental implants', 'root canal', 'dentures', 'restoration'],
            'family': ['family dentist', 'pediatric', 'children', 'family dental']
        }
        
        for category, keywords in categories.items():
            if any(keyword in service_name for keyword in keywords):
                return category
        
        return 'general'

    def extract_faq_from_html(self, soup):
        """Extract FAQ from HTML - enhanced for common patterns"""
        faqs = []
        
        # Look for FAQ section headings
        faq_headings = soup.find_all(['h2', 'h3', 'h4'], string=re.compile(r'faq|question|frequently', re.IGNORECASE))
        
        for heading in faq_headings:
            # Look for questions and answers after the FAQ heading
            current = heading.find_next_sibling()
            while current and len(faqs) < 10:
                if current.name in ['h2', 'h3', 'h4']:
                    # Stop if we hit another major heading
                    break
                
                if current.name in ['h4', 'h5', 'h6', 'strong']:
                    question_text = current.get_text().strip()
                    if '?' in question_text:
                        answer_elem = current.find_next_sibling(['p', 'div'])
                        if answer_elem:
                            answer_text = answer_elem.get_text().strip()
                            if answer_text and len(answer_text) > 20:
                                faqs.append({
                                    'question': question_text,
                                    'answer': answer_text
                                })
                
                current = current.find_next_sibling()
        
        return faqs if faqs else None

    def get_text(self, element):
        """Safely get text from XML element"""
        return element.text if element is not None else None

    def save_service_page(self, service_page, output_dir):
        """Save service page to markdown file"""
        output_path = Path(output_dir) / service_page['filename']
        
        # Create YAML frontmatter with proper formatting
        yaml_content = yaml.dump(
            service_page['data'], 
            default_flow_style=False, 
            allow_unicode=True,
            sort_keys=False  # Preserve field order
        )
        
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
                print(f"    📸 Hero: {page['data']['heroImage']}")
                if page['data'].get('benefits'):
                    print(f"    ✅ Benefits: {len(page['data']['benefits'])} items")
                if page['data'].get('process_steps'):
                    print(f"    ✅ Process Steps: {len(page['data']['process_steps'])} steps")
                if page['data'].get('investment'):
                    print(f"    ✅ Investment: {page['data']['investment']['primary']}")
                print()
            return
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate pages
        for page in service_pages:
            self.save_service_page(page, output_dir)
        
        print(f"\n🎉 Generated {len(service_pages)} enhanced service pages!")


def main():
    parser = argparse.ArgumentParser(description='Generate enhanced service pages from WordPress XML + HTML files')
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