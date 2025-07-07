#!/usr/bin/env python3
"""
FIXED Content Extractor for Alexandria Dental Health Website
Properly extracts PRIMARY content only, not navigation menus
"""

import os
import re
import json
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom

class ContentExtractor:
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
            'wp-content', 'js', 'api', 's', 'feed', 'page', 'author'
        }
        
        # Blog post pattern
        self.blog_dir = 'blog'
        
    def clean_html_content(self, html_content):
        """Clean and extract ONLY primary page content from HTML"""
        if not html_content:
            return ""
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style', 'meta', 'link']):
            element.decompose()
            
        # CRITICAL FIX: Look for PRIMARY content only
        main_content = None
        
        # Look for Beaver Builder PRIMARY content specifically
        primary_content = soup.find('div', class_='fl-builder-content-primary')
        if primary_content:
            print(f"  ✓ Found primary Beaver Builder content")
            main_content = primary_content
        else:
            # Fallback: Look for any fl-builder-content but exclude headers/footers
            bb_contents = soup.find_all('div', class_='fl-builder-content')
            for bb_content in bb_contents:
                # Skip headers, footers, and navigation parts
                if (bb_content.get('data-type') in ['header', 'footer', 'part'] or
                    'header' in str(bb_content.get('class', [])) or
                    'footer' in str(bb_content.get('class', []))):
                    continue
                # Use the first non-header/footer content
                print(f"  ✓ Found Beaver Builder content (fallback)")
                main_content = bb_content
                break
                
        if not main_content:
            # Last resort - try to find article content
            main_content = soup.find('article') or soup.find('main') or soup.find('div', class_='entry-content')
            if main_content:
                print(f"  ✓ Found fallback content container")
                
        if not main_content:
            print(f"  ✗ No content found, using body as fallback")
            # Very last resort - get body but remove nav/header/footer
            body = soup.find('body')
            if body:
                # Remove header, footer, nav elements
                for element in body.find_all(['header', 'footer', 'nav']):
                    element.decompose()
                # Remove Beaver Builder header/footer sections
                for element in body.find_all('div', {'data-type': ['header', 'footer']}):
                    element.decompose()
                main_content = body
                
        if main_content:
            # Clean up WordPress/Beaver Builder-specific classes and IDs
            for element in main_content.find_all():
                if element.get('class'):
                    # Keep structural classes but remove BB-specific node IDs
                    classes = element.get('class')
                    # Keep fl-, uabb- classes for layout but remove node-specific ones
                    new_classes = []
                    for c in classes:
                        if (c.startswith(('fl-', 'uabb-')) and 
                            not c.startswith(('fl-node-', 'uabb-node-'))):
                            new_classes.append(c)
                        elif not c.startswith(('fl-', 'uabb-', 'pp-')):
                            new_classes.append(c)
                    
                    if new_classes:
                        element['class'] = new_classes
                    else:
                        del element['class']
                        
                # Remove WordPress-specific node attributes
                for attr in ['data-node', 'data-bb-id', 'data-post-id', 'data-type']:
                    if element.get(attr):
                        del element[attr]
                        
                # Clean up IDs (keep meaningful ones, remove BB node IDs)
                if element.get('id') and element['id'].startswith(('fl-node-', 'uabb-node-')):
                    del element['id']
                        
            # Convert to clean HTML
            content = str(main_content)
            
            # Clean up extra whitespace
            content = re.sub(r'\s+', ' ', content)
            content = re.sub(r'>\s+<', '><', content)
            
            # Basic content validation
            text_content = BeautifulSoup(content, 'html.parser').get_text(strip=True)
            if len(text_content) < 50:
                print(f"  ⚠️ Warning: Very short content ({len(text_content)} chars)")
            else:
                print(f"  ✓ Content extracted ({len(text_content)} chars)")
            
            return content.strip()
            
        print(f"  ✗ No content could be extracted")
        return ""
    
    def extract_title(self, soup):
        """Extract page title from HTML"""
        # Try different title sources
        title_sources = [
            soup.find('h1'),
            soup.find('title'),
            soup.find('meta', property='og:title'),
            soup.find('meta', attrs={'name': 'title'})
        ]
        
        for source in title_sources:
            if source:
                if source.name == 'meta':
                    title = source.get('content', '')
                else:
                    title = source.get_text(strip=True)
                    
                if title:
                    # Clean up title
                    title = re.sub(r'\s+', ' ', title).strip()
                    # Remove site name from title
                    title = re.sub(r'\s*\|\s*.*$', '', title)
                    title = re.sub(r'\s*-\s*Alexandria.*$', '', title, re.IGNORECASE)
                    return title
                    
        return "Untitled"
    
    def extract_meta_description(self, soup):
        """Extract meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '').strip()
        return ""
    
    def is_blog_post(self, file_path):
        """Check if the file is a blog post"""
        return self.blog_dir in file_path and file_path != f"{self.blog_dir}/index.html"
    
    def get_post_date(self, soup):
        """Extract post date from HTML"""
        # Default to current date
        return datetime.now(timezone.utc)
    
    def process_html_file(self, file_path):
        """Process a single HTML file"""
        try:
            print(f"\nProcessing: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
                
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract basic information
            title = self.extract_title(soup)
            content = self.clean_html_content(html_content)
            meta_description = self.extract_meta_description(soup)
            
            # Determine if it's a blog post or page
            is_post = self.is_blog_post(file_path)
            
            # Generate slug from file path
            slug = self.generate_slug(file_path)
            
            item = {
                'title': title,
                'content': content,
                'excerpt': meta_description,
                'slug': slug,
                'type': 'post' if is_post else 'page',
                'status': 'publish',
                'date': self.get_post_date(soup).isoformat(),
                'file_path': file_path
            }
            
            if is_post:
                self.extracted_content['posts'].append(item)
                print(f"✓ Processed POST: {title}")
            else:
                self.extracted_content['pages'].append(item)
                print(f"✓ Processed PAGE: {title}")
            
        except Exception as e:
            print(f"✗ Error processing {file_path}: {str(e)}")
    
    def generate_slug(self, file_path):
        """Generate WordPress slug from file path"""
        # Remove index.html and clean up path
        path_parts = file_path.replace('/index.html', '').split('/')
        
        # Filter out empty parts and blog directory for posts
        clean_parts = [part for part in path_parts if part and part != self.blog_dir]
        
        if clean_parts:
            slug = clean_parts[-1]  # Use the last directory name
        else:
            slug = 'home'
            
        # Clean slug
        slug = re.sub(r'[^a-zA-Z0-9-]', '-', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
        
        return slug or 'untitled'
    
    def scan_directory(self):
        """Scan directory for HTML files"""
        print(f"Scanning directory: {self.source_dir}")
        
        html_files = []
        
        for root, dirs, files in os.walk(self.source_dir):
            # Skip unwanted directories
            dirs[:] = [d for d in dirs if d not in self.skip_paths]
            
            for file in files:
                if file == 'index.html':
                    file_path = os.path.relpath(os.path.join(root, file), self.source_dir)
                    # Skip root index file as it's just a redirect
                    if file_path != 'index.html':
                        html_files.append(file_path)
        
        return html_files
    
    def generate_wordpress_xml(self):
        """Generate WordPress WXR import file"""
        # Create XML structure
        rss = ET.Element('rss', version='2.0')
        rss.set('xmlns:excerpt', 'http://wordpress.org/export/1.2/excerpt/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        rss.set('xmlns:wfw', 'http://wellformedweb.org/CommentAPI/')
        rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
        rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')
        
        channel = ET.SubElement(rss, 'channel')
        
        # Channel information
        ET.SubElement(channel, 'title').text = 'Alexandria Dental Health & Smile Studio'
        ET.SubElement(channel, 'link').text = self.site_url
        ET.SubElement(channel, 'description').text = 'Dentist in Alexandria VA'
        ET.SubElement(channel, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        ET.SubElement(channel, 'language').text = 'en-US'
        ET.SubElement(channel, 'wp:wxr_version').text = '1.2'
        ET.SubElement(channel, 'wp:base_site_url').text = self.site_url
        ET.SubElement(channel, 'wp:base_blog_url').text = self.site_url
        
        # Add author
        author = ET.SubElement(channel, 'wp:author')
        ET.SubElement(author, 'wp:author_id').text = '1'
        ET.SubElement(author, 'wp:author_login').text = 'admin'
        ET.SubElement(author, 'wp:author_email').text = 'admin@alexandriadentalhealth.com'
        ET.SubElement(author, 'wp:author_display_name').text = 'Administrator'
        ET.SubElement(author, 'wp:author_first_name').text = 'Site'
        ET.SubElement(author, 'wp:author_last_name').text = 'Administrator'
        
        # Process all content
        post_id = 1
        
        # Add pages
        for page in self.extracted_content['pages']:
            item = ET.SubElement(channel, 'item')
            
            ET.SubElement(item, 'title').text = page['title']
            ET.SubElement(item, 'link').text = f"{self.site_url}/{page['slug']}/"
            ET.SubElement(item, 'pubDate').text = datetime.fromisoformat(page['date']).strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, 'dc:creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"{self.site_url}/?page_id={post_id}"
            ET.SubElement(item, 'description')
            
            # Content
            content_encoded = ET.SubElement(item, 'content:encoded')
            content_encoded.text = page['content']
            
            # Excerpt
            excerpt_encoded = ET.SubElement(item, 'excerpt:encoded')
            excerpt_encoded.text = page['excerpt']
            
            # WordPress specific
            ET.SubElement(item, 'wp:post_id').text = str(post_id)
            ET.SubElement(item, 'wp:post_date').text = datetime.fromisoformat(page['date']).strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, 'wp:post_date_gmt').text = datetime.fromisoformat(page['date']).strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, 'wp:comment_status').text = 'closed'
            ET.SubElement(item, 'wp:ping_status').text = 'closed'
            ET.SubElement(item, 'wp:post_name').text = page['slug']
            ET.SubElement(item, 'wp:status').text = page['status']
            ET.SubElement(item, 'wp:post_parent').text = '0'
            ET.SubElement(item, 'wp:menu_order').text = '0'
            ET.SubElement(item, 'wp:post_type').text = 'page'
            ET.SubElement(item, 'wp:post_password').text = ''
            ET.SubElement(item, 'wp:is_sticky').text = '0'
            
            post_id += 1
        
        # Add blog posts
        for post in self.extracted_content['posts']:
            item = ET.SubElement(channel, 'item')
            
            ET.SubElement(item, 'title').text = post['title']
            ET.SubElement(item, 'link').text = f"{self.site_url}/{post['slug']}/"
            ET.SubElement(item, 'pubDate').text = datetime.fromisoformat(post['date']).strftime('%a, %d %b %Y %H:%M:%S +0000')
            ET.SubElement(item, 'dc:creator').text = 'admin'
            ET.SubElement(item, 'guid', isPermaLink='false').text = f"{self.site_url}/?p={post_id}"
            ET.SubElement(item, 'description')
            
            # Content
            content_encoded = ET.SubElement(item, 'content:encoded')
            content_encoded.text = post['content']
            
            # Excerpt
            excerpt_encoded = ET.SubElement(item, 'excerpt:encoded')
            excerpt_encoded.text = post['excerpt']
            
            # WordPress specific
            ET.SubElement(item, 'wp:post_id').text = str(post_id)
            ET.SubElement(item, 'wp:post_date').text = datetime.fromisoformat(post['date']).strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, 'wp:post_date_gmt').text = datetime.fromisoformat(post['date']).strftime('%Y-%m-%d %H:%M:%S')
            ET.SubElement(item, 'wp:comment_status').text = 'open'
            ET.SubElement(item, 'wp:ping_status').text = 'open'
            ET.SubElement(item, 'wp:post_name').text = post['slug']
            ET.SubElement(item, 'wp:status').text = post['status']
            ET.SubElement(item, 'wp:post_parent').text = '0'
            ET.SubElement(item, 'wp:menu_order').text = '0'
            ET.SubElement(item, 'wp:post_type').text = 'post'
            ET.SubElement(item, 'wp:post_password').text = ''
            ET.SubElement(item, 'wp:is_sticky').text = '0'
            
            post_id += 1
        
        return rss
    
    def save_xml(self, xml_element, filename='alexandria-dental-import-FIXED.xml'):
        """Save XML to file with proper formatting"""
        rough_string = ET.tostring(xml_element, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent='  '))
        
        print(f"✓ FIXED WordPress import file saved: {filename}")
    
    def save_json_summary(self, filename='content-summary-FIXED.json'):
        """Save content summary as JSON"""
        summary = {
            'extraction_date': datetime.now().isoformat(),
            'total_pages': len(self.extracted_content['pages']),
            'total_posts': len(self.extracted_content['posts']),
            'pages': [{'title': p['title'], 'slug': p['slug']} for p in self.extracted_content['pages']],
            'posts': [{'title': p['title'], 'slug': p['slug']} for p in self.extracted_content['posts']]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✓ FIXED Content summary saved: {filename}")
    
    def run(self):
        """Main extraction process"""
        print("=" * 60)
        print("Alexandria Dental Health - FIXED Content Extractor")
        print("=" * 60)
        
        # Scan for HTML files
        html_files = self.scan_directory()
        print(f"Found {len(html_files)} HTML files to process")
        
        # Process each file
        print("\nProcessing files...")
        for file_path in html_files:
            self.process_html_file(file_path)
        
        # Generate outputs
        print(f"\nExtraction complete!")
        print(f"Pages: {len(self.extracted_content['pages'])}")
        print(f"Posts: {len(self.extracted_content['posts'])}")
        
        # Generate WordPress XML import file
        print("\nGenerating FIXED WordPress import file...")
        xml_root = self.generate_wordpress_xml()
        self.save_xml(xml_root)
        
        # Save summary
        self.save_json_summary()
        
        print("\n" + "=" * 60)
        print("FIXED EXTRACTION COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Import the NEW 'alexandria-dental-import-FIXED.xml' file")
        print("2. The content should now display properly!")
        print("3. Copy images from wp-content/uploads to your WordPress uploads folder")

if __name__ == "__main__":
    import sys
    
    source_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    extractor = ContentExtractor(source_directory)
    extractor.run() 