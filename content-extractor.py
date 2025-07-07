#!/usr/bin/env python3
"""
Content Extractor for Alexandria Dental Health Website
Converts scraped HTML files to WordPress XML import format
"""

import os
import re
import json
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
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
        """Clean and extract main content from HTML"""
        if not html_content:
            return ""
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style', 'meta', 'link']):
            element.decompose()
            
        # Try to find main content areas (Beaver Builder content)
        main_content = None
        
        # Look for Beaver Builder content
        bb_content = soup.find('div', class_='fl-builder-content')
        if bb_content:
            main_content = bb_content
        else:
            # Fallback to article or main content
            main_content = soup.find('article') or soup.find('main') or soup.find('div', class_='entry-content')
            
        if not main_content:
            # Last resort - get body content
            body = soup.find('body')
            if body:
                # Remove header, footer, nav
                for element in body.find_all(['header', 'footer', 'nav']):
                    element.decompose()
                main_content = body
                
        if main_content:
            # Clean up WordPress-specific classes and IDs
            for element in main_content.find_all():
                if element.get('class'):
                    # Keep only relevant classes, remove BB-specific ones
                    classes = element.get('class')
                    new_classes = [c for c in classes if not c.startswith(('fl-', 'uabb-', 'pp-'))]
                    if new_classes:
                        element['class'] = new_classes
                    else:
                        del element['class']
                        
                # Remove WordPress-specific attributes
                for attr in ['data-node', 'data-bb-id', 'id']:
                    if element.get(attr) and element[attr].startswith(('fl-', 'uabb-', 'pp-')):
                        del element[attr]
                        
            # Convert to clean HTML
            content = str(main_content)
            
            # Clean up extra whitespace
            content = re.sub(r'\s+', ' ', content)
            content = re.sub(r'>\s+<', '><', content)
            
            return content.strip()
            
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
        # Look for date in various formats
        date_selectors = [
            'time[datetime]',
            '.posted-on time',
            '.entry-date',
            'meta[property="article:published_time"]'
        ]
        
        for selector in date_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    date_str = element.get('content')
                else:
                    date_str = element.get('datetime') or element.get_text(strip=True)
                    
                if date_str:
                    try:
                        # Try to parse the date
                        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    except:
                        pass
                        
        # Default to current date
        return datetime.now(timezone.utc)
    
    def process_html_file(self, file_path):
        """Process a single HTML file"""
        try:
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
            else:
                self.extracted_content['pages'].append(item)
                
            print(f"✓ Processed {'post' if is_post else 'page'}: {title}")
            
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
        """Generate WordPress WXR (WordPress eXtended RSS) import file"""
        
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
        
        # Add categories for blog posts
        blog_category = ET.SubElement(channel, 'wp:category')
        ET.SubElement(blog_category, 'wp:term_id').text = '1'
        ET.SubElement(blog_category, 'wp:category_nicename').text = 'dental-health'
        ET.SubElement(blog_category, 'wp:category_parent').text = ''
        ET.SubElement(blog_category, 'wp:cat_name').text = 'Dental Health'
        
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
            
            # Categories
            category = ET.SubElement(item, 'category', domain='category', nicename='dental-health')
            category.text = 'Dental Health'
            
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
    
    def save_xml(self, xml_element, filename='alexandria-dental-import.xml'):
        """Save XML to file with proper formatting"""
        rough_string = ET.tostring(xml_element, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent='  '))
        
        print(f"✓ WordPress import file saved: {filename}")
    
    def save_json_summary(self, filename='content-summary.json'):
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
        
        print(f"✓ Content summary saved: {filename}")
    
    def run(self):
        """Main extraction process"""
        print("=" * 60)
        print("Alexandria Dental Health - Content Extractor")
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
        print("\nGenerating WordPress import file...")
        xml_root = self.generate_wordpress_xml()
        self.save_xml(xml_root)
        
        # Save summary
        self.save_json_summary()
        
        print("\n" + "=" * 60)
        print("EXTRACTION COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Copy the 'alexandria-dental-theme' folder to your WordPress themes directory")
        print("2. Activate the theme in WordPress admin")
        print("3. Import the 'alexandria-dental-import.xml' file using WordPress Tools > Import")
        print("4. Copy images from wp-content/uploads to your WordPress uploads folder")
        print("5. Configure navigation menus and customize theme settings")

if __name__ == "__main__":
    import sys
    
    source_directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    extractor = ContentExtractor(source_directory)
    extractor.run() 