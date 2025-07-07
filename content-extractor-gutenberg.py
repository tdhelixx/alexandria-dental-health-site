#!/usr/bin/env python3
"""
Content Extractor with Gutenberg Block Structure
Creates WordPress XML import with proper Gutenberg blocks instead of raw HTML
"""

import os
import re
import json
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom

class GutenbergContentExtractor:
    def __init__(self, source_dir='.'):
        self.source_dir = source_dir
        self.site_url = 'https://www.alexandriadentalhealth.com'
        self.extracted_content = {
            'pages': [],
            'posts': [],
            'media': []
        }
        
        # Skip these directories and files
        self.skip_paths = {
            'hts-cache', 'backups', 'backups_enhanced', 'wp-includes', 
            'wp-content', 'api', 's', 'xfn', 'js'
        }
        
        # Track processed content to avoid duplicates
        self.processed_titles = set()
        self.processed_content_hashes = set()
        
    def extract_all_content(self):
        """Extract content from ALL HTML files (no limits)"""
        print("🔍 Scanning for ALL content files...")
        
        pages_count = 0
        posts_count = 0
        
        # Process home page first if it exists
        home_file = os.path.join(self.source_dir, 'index.html')
        if os.path.exists(home_file):
            content_data = self.extract_content_from_file(home_file, 'home', False)
            if content_data:
                self.extracted_content['pages'].append(content_data)
                pages_count += 1
        
        for root, dirs, files in os.walk(self.source_dir):
            # Skip unwanted directories
            dirs[:] = [d for d in dirs if d not in self.skip_paths]
            
            for file in files:
                if file == 'index.html':
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(root, self.source_dir)
                    
                    # Skip root index since we processed it above
                    if relative_path == '.':
                        continue
                        
                    # Determine if it's a blog post or page
                    is_blog_post = relative_path.startswith('blog') and relative_path != 'blog'
                    
                    content_data = self.extract_content_from_file(file_path, relative_path, is_blog_post)
                    if content_data:
                        if is_blog_post:
                            self.extracted_content['posts'].append(content_data)
                            posts_count += 1
                        else:
                            self.extracted_content['pages'].append(content_data)
                            pages_count += 1
        
        print(f"✅ Extracted {len(self.extracted_content['pages'])} pages")
        print(f"✅ Extracted {len(self.extracted_content['posts'])} posts")
        
    def extract_content_from_file(self, file_path, relative_path, is_blog_post):
        """Extract content from a single HTML file and convert to Gutenberg blocks"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract title (for WordPress title, NOT for content)
            title_elem = soup.find('title')
            title = title_elem.get_text().strip() if title_elem else relative_path.replace('/', ' ').title()
            
            # Clean up title (remove site name, etc.)
            title = self.clean_title(title)
            
            # Skip duplicates based on title
            if title in self.processed_titles:
                print(f"⚠️  Skipping duplicate title: {title}")
                return None
            
            # Extract meta description
            meta_desc = soup.find('meta', {'name': 'description'})
            excerpt = meta_desc.get('content', '').strip() if meta_desc else ''
            
            # Find primary Beaver Builder content, excluding sidebar/footer
            primary_content = soup.find('div', class_=lambda x: x and 'fl-builder-content-primary' in x)
            
            if not primary_content:
                print(f"⚠️  No primary content found: {relative_path}")
                return None
                
            # Remove sidebar and footer content from primary content
            self.remove_sidebar_content(primary_content)
            
            # Remove title tags from content (they shouldn't be in the content area)
            for title_tag in primary_content.find_all(['title']):
                title_tag.decompose()
            
            # Convert Beaver Builder content to Gutenberg blocks
            gutenberg_content = self.convert_to_gutenberg_blocks(primary_content)
            
            if not gutenberg_content.strip():
                print(f"⚠️  No content extracted: {relative_path}")
                return None
            
            # Check for duplicate content
            content_hash = hash(gutenberg_content[:500])  # Hash first 500 chars
            if content_hash in self.processed_content_hashes:
                print(f"⚠️  Skipping duplicate content: {title}")
                return None
            
            # Create URL slug  
            if relative_path == 'home':
                slug = 'home'
            else:
                slug = relative_path.replace('/', '-').replace('\\', '-')
            
            content_data = {
                'title': title,
                'slug': slug,
                'content': gutenberg_content,
                'excerpt': excerpt,
                'relative_path': relative_path,
                'is_blog_post': is_blog_post,
                'date': datetime.now(timezone.utc).isoformat()
            }
            
            # Track processed content
            self.processed_titles.add(title)
            self.processed_content_hashes.add(content_hash)
            
            print(f"✅ Extracted: {title} ({len(gutenberg_content)} chars)")
            return content_data
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {str(e)}")
            return None
    
    def clean_title(self, title):
        """Clean up title by removing site name and common suffixes"""
        # Remove common suffixes
        suffixes_to_remove = [
            '| Alexandria Dental Health & Smile Studio',
            '- Alexandria Dental Health & Smile Studio', 
            'Alexandria Dental Health & Smile Studio',
            '| Dentist Alexandria VA',
            '- Dentist Alexandria VA',
            'Dentist Alexandria VA',
            '| Alexandria VA',
            '- Alexandria VA'
        ]
        
        for suffix in suffixes_to_remove:
            if suffix in title:
                title = title.replace(suffix, '').strip()
        
        # Remove leading/trailing separators
        title = re.sub(r'^[\|\-\–\—]\s*', '', title)
        title = re.sub(r'\s*[\|\-\–\—]$', '', title)
        
        # Fix common title issues
        title = title.replace('  ', ' ').strip()
        
        # Handle incomplete titles
        if title.endswith(' for') or title.endswith(' in'):
            title += ' Alexandria VA'
        
        return title.strip()
    
    def convert_to_gutenberg_blocks(self, content_elem):
        """Convert Beaver Builder content to Gutenberg blocks in document order"""
        gutenberg_blocks = []
        
        # Process all elements in document order to preserve layout
        all_elements = content_elem.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'img', 'a'])
        
        processed_elements = set()  # Track processed elements to avoid duplicates
        seen_text = set()  # Track text content to avoid duplicate content
        
        for element in all_elements:
            # Skip if already processed
            if id(element) in processed_elements:
                continue
                
            # Skip elements that are likely duplicates based on text content
            element_text = element.get_text().strip()
            if element_text in seen_text and len(element_text) > 20:
                continue
                
            # Skip sidebar-related content
            if self.is_sidebar_content(element_text):
                continue
                
            # Process headings
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = element.get_text().strip()
                if text and len(text) > 2 and text not in seen_text and not self.is_sidebar_content(text):
                    level = int(element.name[1])  # h1 -> 1, h2 -> 2, etc.
                    block = self.create_heading_block(text, level)
                    gutenberg_blocks.append(block)
                    processed_elements.add(id(element))
                    seen_text.add(text)
            
            # Process paragraphs
            elif element.name == 'p':
                text = element.get_text().strip()
                if text and len(text) > 15 and text not in seen_text and not self.is_sidebar_content(text):
                    block = self.create_paragraph_block(text)
                    gutenberg_blocks.append(block)
                    processed_elements.add(id(element))
                    seen_text.add(text)
            
            # Process images
            elif element.name == 'img':
                src = element.get('src', '')
                alt = element.get('alt', '')
                title = element.get('title', '')
                
                if src and not self.is_sidebar_image(src, alt):
                    block = self.create_image_block(src, alt, title)
                    gutenberg_blocks.append(block)
                    processed_elements.add(id(element))
            
            # Process buttons
            elif element.name == 'a' and element.get('class') and 'fl-button' in str(element.get('class')):
                text = element.get_text().strip()
                href = element.get('href', '')
                
                if text and href and text not in seen_text and not self.is_sidebar_content(text):
                    block = self.create_button_block(text, href)
                    gutenberg_blocks.append(block)
                    processed_elements.add(id(element))
                    seen_text.add(text)
        
        # If no specific blocks found, extract general text content
        if not gutenberg_blocks:
            # Get all meaningful text
            text_content = content_elem.get_text()
            # Clean up whitespace
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            if text_content and len(text_content) > 50:
                # Split into paragraphs
                paragraphs = [p.strip() for p in text_content.split('\n') if p.strip() and len(p.strip()) > 20]
                for para in paragraphs[:5]:  # Limit to first 5 paragraphs
                    if not self.is_sidebar_content(para):
                        block = self.create_paragraph_block(para)
                        gutenberg_blocks.append(block)
        
        return '\n\n'.join(gutenberg_blocks)
    
    def is_sidebar_content(self, text):
        """Check if text content is sidebar-related and should be excluded"""
        if not text:
            return False
            
        text_lower = text.lower()
        
        # Office hours patterns
        office_patterns = [
            r'monday.*?10:00.*?6:00',
            r'tuesday.*?10:00.*?6:00',
            r'wednesday.*?10:00.*?6:00',
            r'thursday.*?9:00.*?4:00',
            r'friday.*?8:00.*?1:00',
            r'saturday.*?closed',
            r'sunday.*?closed',
            r'office hours',
        ]
        
        for pattern in office_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL):
                return True
        
        # Contact info patterns
        contact_patterns = [
            '2847 duke st',
            'alexandria va 22314',
            '(703) 212-9622',
            'alexandria dental health & smile studio',
        ]
        
        for pattern in contact_patterns:
            if pattern in text_lower:
                return True
        
        # Special offer patterns
        offer_patterns = [
            'view our special offers',
            'click here',
            'special offers',
        ]
        
        for pattern in offer_patterns:
            if pattern in text_lower:
                return True
        
        return False
    
    def is_sidebar_image(self, src, alt):
        """Check if image is sidebar-related"""
        if not src and not alt:
            return False
            
        sidebar_image_patterns = [
            'special-offer',
            'view-our-special',
            'contact',
            'phone',
            'address'
        ]
        
        combined_text = f"{src} {alt}".lower()
        
        for pattern in sidebar_image_patterns:
            if pattern in combined_text:
                return True
                
        return False
    
    def remove_sidebar_content(self, content_elem):
        """Remove sidebar, contact info, and other non-main content"""
        # Remove elements that are typically sidebar/footer content
        selectors_to_remove = [
            # Contact information
            'div[class*="contact"]',
            'div[class*="office-hours"]', 
            'div[class*="phone"]',
            'div[class*="address"]',
            'div[class*="location"]',
            # Navigation elements
            'nav',
            'div[class*="navigation"]',
            'div[class*="menu"]',
            # Sidebar widgets
            'div[class*="sidebar"]',
            'div[class*="widget"]',
            'aside',
            # Footer elements  
            'footer',
            'div[class*="footer"]',
            # Special offer buttons
            'div[class*="special-offer"]',
            'a[class*="special-offer"]',
            'div[class*="special"]',
            # Social media links
            'div[class*="social"]',
            'a[href*="facebook"]',
            'a[href*="twitter"]', 
            'a[href*="instagram"]',
            # Forms and CTAs that are typically in sidebars
            'form[class*="contact"]',
            'div[class*="cta-sidebar"]',
            'div[class*="appointment"]',
        ]
        
        for selector in selectors_to_remove:
            elements = content_elem.select(selector)
            for elem in elements:
                elem.decompose()
        
        # Remove text patterns that are typically sidebar content with more aggressive patterns
        sidebar_text_patterns = [
            # Office hours - more comprehensive
            r'Monday.*?Friday.*?Saturday.*?Sunday',
            r'Office Hours.*?Sunday',
            r'Monday.*?10:00.*?6:00.*?Tuesday.*?10:00.*?6:00.*?Wednesday.*?10:00.*?6:00',
            r'Monday\s*10:00am.*?6:00pm.*?Tuesday\s*10:00am.*?6:00pm',
            # Contact info - more comprehensive
            r'Alexandria Dental Health.*?Smile Studio.*?\d{5}',
            r'\(\d{3}\)\s*\d{3}-\d{4}',  # Phone numbers
            r'2847\s+Duke\s+St.*?Alexandria.*?VA.*?22314',  # Full address
            r'Alexandria\s+VA\s+22314',  # ZIP code
            # Special offers - more comprehensive
            r'VIEW OUR.*?SPECIAL.*?OFFERS.*?CLICK HERE',
            r'SPECIAL.*?OFFERS?.*?CLICK',
            r'View Our Special Offers',
        ]
        
        for pattern in sidebar_text_patterns:
            # Find text nodes matching these patterns
            text_nodes = content_elem.find_all(string=re.compile(pattern, re.IGNORECASE | re.DOTALL))
            for text_node in text_nodes:
                if hasattr(text_node, 'parent') and text_node.parent:
                    # Remove the entire parent element
                    text_node.parent.decompose()
        
        # Remove elements containing specific sidebar text - more comprehensive
        sidebar_keywords = [
            '2847 Duke St', 'Alexandria VA 22314', '(703) 212-9622',
            'Office Hours', 'Monday:', 'Tuesday:', 'Wednesday:', 'Thursday:', 'Friday:', 'Saturday:', 'Sunday:',
            'VIEW OUR SPECIAL OFFERS', 'CLICK HERE', 'SPECIAL OFFERS',
            'Monday 10:00am - 6:00pm', 'Tuesday 10:00am - 6:00pm', 'Wednesday 10:00am - 6:00pm',
            'Thursday 9:00am - 4:00pm', 'Friday 8:00am - 1:00pm', 'Saturday & Sunday Closed'
        ]
        
        for keyword in sidebar_keywords:
            elements = content_elem.find_all(string=lambda text: text and keyword in text)
            for elem in elements:
                if hasattr(elem, 'parent') and elem.parent:
                    # Try to remove the parent container
                    parent = elem.parent
                    # Go up the tree to find a suitable container to remove
                    while parent and parent.name in ['span', 'strong', 'em']:
                        parent = parent.parent
                    if parent and parent.name in ['div', 'p', 'section', 'article']:
                        parent.decompose()
    
    def create_heading_block(self, text, level):
        """Create a Gutenberg heading block"""
        return f'''<!-- wp:heading {{"level":{level}}} -->
<h{level}>{self.escape_html(text)}</h{level}>
<!-- /wp:heading -->'''
    
    def create_paragraph_block(self, text):
        """Create a Gutenberg paragraph block"""
        return f'''<!-- wp:paragraph -->
<p>{self.escape_html(text)}</p>
<!-- /wp:paragraph -->'''
    
    def create_image_block(self, src, alt='', title=''):
        """Create a Gutenberg image block"""
        alt_attr = f' alt="{self.escape_html(alt)}"' if alt else ''
        title_attr = f' title="{self.escape_html(title)}"' if title else ''
        
        return f'''<!-- wp:image -->
<figure class="wp-block-image"><img src="{src}"{alt_attr}{title_attr}/></figure>
<!-- /wp:image -->'''
    
    def create_button_block(self, text, url):
        """Create a Gutenberg button block"""
        return f'''<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link" href="{url}">{self.escape_html(text)}</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->'''
    
    def escape_html(self, text):
        """Escape HTML special characters"""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))
    
    def generate_wordpress_xml(self):
        """Generate WordPress XML import file with Gutenberg blocks"""
        print("📝 Generating WordPress XML import...")
        
        # Create root element
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:excerpt', 'http://wordpress.org/export/1.2/excerpt/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        rss.set('xmlns:wfw', 'http://wellformedweb.org/CommentAPI/')
        rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
        rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')
        
        channel = ET.SubElement(rss, 'channel')
        
        # Channel info
        ET.SubElement(channel, 'title').text = 'Alexandria Dental Health & Smile Studio'
        ET.SubElement(channel, 'link').text = self.site_url
        ET.SubElement(channel, 'description').text = 'Professional dental care in Alexandria VA'
        ET.SubElement(channel, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        ET.SubElement(channel, 'language').text = 'en-US'
        ET.SubElement(channel, 'wp:wxr_version').text = '1.2'
        ET.SubElement(channel, 'wp:base_site_url').text = self.site_url
        ET.SubElement(channel, 'wp:base_blog_url').text = self.site_url
        
        item_id = 1
        
        # Add pages
        for page_data in self.extracted_content['pages']:
            item = ET.SubElement(channel, 'item')
            
            ET.SubElement(item, 'title').text = page_data['title']
            ET.SubElement(item, 'link').text = f"{self.site_url}/{page_data['slug']}/"
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            ET.SubElement(item, 'dc:creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"{self.site_url}/?page_id={item_id}"
            ET.SubElement(item, 'description')
            
            # Content with Gutenberg blocks
            content_elem = ET.SubElement(item, 'content:encoded')
            content_elem.text = page_data['content']
            
            ET.SubElement(item, 'excerpt:encoded').text = page_data.get('excerpt', '')
            ET.SubElement(item, 'wp:post_id').text = str(item_id)
            ET.SubElement(item, 'wp:post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, 'wp:post_date_gmt').text = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, 'wp:comment_status').text = 'closed'
            ET.SubElement(item, 'wp:ping_status').text = 'closed'
            ET.SubElement(item, 'wp:post_name').text = page_data['slug']
            ET.SubElement(item, 'wp:status').text = 'publish'
            ET.SubElement(item, 'wp:post_parent').text = '0'
            ET.SubElement(item, 'wp:menu_order').text = '0'
            ET.SubElement(item, 'wp:post_type').text = 'page'
            ET.SubElement(item, 'wp:post_password').text = ''
            ET.SubElement(item, 'wp:is_sticky').text = '0'
            
            item_id += 1
        
        # Add posts
        for post_data in self.extracted_content['posts']:
            item = ET.SubElement(channel, 'item')
            
            ET.SubElement(item, 'title').text = post_data['title']
            ET.SubElement(item, 'link').text = f"{self.site_url}/{post_data['slug']}/"
            ET.SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            ET.SubElement(item, 'dc:creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"{self.site_url}/?p={item_id}"
            ET.SubElement(item, 'description')
            
            # Content with Gutenberg blocks
            content_elem = ET.SubElement(item, 'content:encoded')
            content_elem.text = post_data['content']
            
            ET.SubElement(item, 'excerpt:encoded').text = post_data.get('excerpt', '')
            ET.SubElement(item, 'wp:post_id').text = str(item_id)
            ET.SubElement(item, 'wp:post_date').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, 'wp:post_date_gmt').text = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, 'wp:comment_status').text = 'open'
            ET.SubElement(item, 'wp:ping_status').text = 'open'
            ET.SubElement(item, 'wp:post_name').text = post_data['slug']
            ET.SubElement(item, 'wp:status').text = 'publish'
            ET.SubElement(item, 'wp:post_parent').text = '0'
            ET.SubElement(item, 'wp:menu_order').text = '0'
            ET.SubElement(item, 'wp:post_type').text = 'post'
            ET.SubElement(item, 'wp:post_password').text = ''
            ET.SubElement(item, 'wp:is_sticky').text = '0'
            
            # Add category
            category = ET.SubElement(item, 'category')
            category.set('domain', 'category')
            category.set('nicename', 'dental-health')
            category.text = 'Dental Health'
            
            item_id += 1
        
        # Pretty print XML
        xml_str = ET.tostring(rss, encoding='unicode')
        dom = minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent='  ')
        
        # Clean up extra whitespace
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        pretty_xml = '\n'.join(lines)
        
        # Save to file
        output_file = 'alexandria-dental-gutenberg-import-CLEAN.xml'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        print(f"✅ Generated {output_file}")
        print(f"📊 File size: {os.path.getsize(output_file) / 1024 / 1024:.1f} MB")
        
    def save_content_summary(self):
        """Save content summary as JSON"""
        summary = {
            'extraction_date': datetime.now().isoformat(),
            'total_pages': len(self.extracted_content['pages']),
            'total_posts': len(self.extracted_content['posts']),
            'pages': [{'title': p['title'], 'slug': p['slug'], 'content_length': len(p['content'])} 
                     for p in self.extracted_content['pages']],
            'posts': [{'title': p['title'], 'slug': p['slug'], 'content_length': len(p['content'])} 
                     for p in self.extracted_content['posts']]
        }
        
        with open('gutenberg-content-summary-CLEAN.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print("✅ Saved content summary to gutenberg-content-summary-CLEAN.json")

def main():
    print("🚀 Alexandria Dental Health - CLEAN Gutenberg Content Extractor")
    print("=" * 70)
    
    extractor = GutenbergContentExtractor()
    
    # Extract ALL content (no limits)
    extractor.extract_all_content()
    
    # Generate WordPress XML with Gutenberg blocks
    extractor.generate_wordpress_xml()
    
    # Save summary
    extractor.save_content_summary()
    
    print("\n🎉 CLEAN extraction complete!")
    print("\n📋 Next steps:")
    print("1. Import 'alexandria-dental-gutenberg-import-CLEAN.xml' into WordPress")
    print("2. All pages and posts with improved sidebar exclusion")
    print("3. Duplicate content detection and title cleaning applied")
    print("4. Ready for production use!")

if __name__ == "__main__":
    main() 