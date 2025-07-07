# Alexandria Dental Health - WordPress Conversion

This project converts the scraped Alexandria Dental Health website into a custom WordPress theme and generates an importable XML file with all the content.

## Overview

The conversion process includes:

- **Custom WordPress Theme**: A clean, responsive theme that matches the original design
- **Content Extraction**: Python script that processes all HTML files and creates WordPress-compatible content
- **XML Import File**: WordPress WXR format file for importing all pages and posts
- **Preserved Styling**: Original fonts, colors, and responsive design maintained

## Prerequisites

- Python 3.7 or higher
- WordPress site (Local, staging, or production)
- Access to WordPress admin and file system

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Content Extraction

Navigate to your scraped website directory and run:

```bash
python content-extractor.py
```

This will:
- Scan all HTML files in the directory
- Extract page titles, content, and metadata
- Identify blog posts vs. pages based on directory structure
- Generate `alexandria-dental-import.xml` for WordPress import
- Create `content-summary.json` with extraction details

### 3. Install WordPress Theme

1. Copy the `alexandria-dental-theme` folder to your WordPress `wp-content/themes/` directory
2. In WordPress admin, go to **Appearance > Themes**
3. Activate the **Alexandria Dental Health** theme

### 4. Import Content

1. In WordPress admin, go to **Tools > Import**
2. Install the "WordPress" importer if not already installed
3. Choose the `alexandria-dental-import.xml` file
4. Map authors (or create new ones)
5. Check "Download and import file attachments" if desired
6. Run the import

### 5. Copy Media Files

Copy the images and media from your scraped site to WordPress:

```bash
# Copy from scraped site wp-content/uploads to WordPress
cp -r /path/to/scraped-site/wp-content/uploads/* /path/to/wordpress/wp-content/uploads/
```

### 6. Configure WordPress

#### Set up Navigation Menus
1. Go to **Appearance > Menus**
2. Create a "Primary Menu" and assign it to "Primary Navigation"
3. Add your pages to create the site structure

#### Configure Theme Settings
1. Go to **Appearance > Customize**
2. Set up your logo in **Site Identity**
3. Configure footer information in **Footer Settings**:
   - Practice Address
   - Phone Number
   - Email Address
   - Office Hours

#### Set Homepage
1. Go to **Settings > Reading**
2. Set "Your homepage displays" to "A static page"
3. Choose your homepage from the dropdown

## Theme Features

### Responsive Design
- Mobile-first approach with breakpoints at 768px and 1024px
- Flexible grid system
- Optimized for all devices

### Typography
- Google Fonts: Raleway (headings) and Nunito (body text)
- Consistent hierarchy and spacing
- Optimized for readability

### Color Scheme
- Primary Purple: #32192f
- Accent Mauve: #a27295
- Hover Teal: #72b7bc
- Bright Orange: #ffae00

### Navigation
- Dropdown menu support
- Mobile hamburger menu
- Keyboard accessible
- SEO-friendly structure

### Blog Support
- Grid layout for blog posts
- Featured images
- Post excerpts and metadata
- Pagination

### SEO Optimized
- Clean HTML structure
- Meta descriptions
- Schema.org markup ready
- Fast loading

## Content Structure

### Pages
All index.html files outside of `/blog/` become WordPress pages:
- About
- Services (various dental procedures)
- Patient Information
- Contact
- etc.

### Blog Posts
All index.html files inside `/blog/` subdirectories become WordPress posts:
- Dental health articles
- Treatment information
- Practice updates

## Customization

### Theme Files
- `style.css` - Main stylesheet
- `functions.php` - Theme functionality
- `header.php` - Site header and navigation
- `footer.php` - Site footer
- `index.php` - Main template
- `front-page.php` - Homepage template

### Adding Custom Styles
Add custom CSS in **Appearance > Customize > Additional CSS** or edit the theme's `style.css` file.

### Modifying Templates
Edit the PHP template files to change layout and functionality. Always create a child theme for major modifications.

## Troubleshooting

### Common Issues

1. **Images not displaying**
   - Ensure images are copied to the correct WordPress uploads directory
   - Check file permissions (755 for directories, 644 for files)

2. **Menu not appearing**
   - Create a menu in **Appearance > Menus**
   - Assign it to the "Primary Navigation" location

3. **Styles not loading**
   - Clear any caching plugins
   - Check that the theme is properly activated

4. **Import errors**
   - Increase PHP memory limit in wp-config.php: `ini_set('memory_limit', '256M');`
   - Check file upload limits

### Support

For issues with the conversion process:
1. Check the `content-summary.json` file for extraction details
2. Verify all required HTML files are present
3. Ensure Python dependencies are installed correctly

## File Structure

```
alexandria-dental-theme/
├── style.css           # Main stylesheet
├── index.php          # Main template
├── header.php         # Header template
├── footer.php         # Footer template
├── front-page.php     # Homepage template
├── functions.php      # Theme functions
└── assets/
    └── images/        # Theme images

content-extractor.py    # Extraction script
requirements.txt       # Python dependencies
README.md             # This file
```

## License

This theme conversion is provided as-is for the specific purpose of migrating the Alexandria Dental Health website. Please ensure compliance with any existing licensing agreements for the original content and design.

## Next Steps After Setup

1. **Test thoroughly** - Check all pages and functionality
2. **SEO optimization** - Install Yoast SEO or similar plugin
3. **Performance optimization** - Consider caching and image optimization plugins
4. **Security** - Keep WordPress core, themes, and plugins updated
5. **Backup** - Set up regular automated backups
6. **Analytics** - Add Google Analytics tracking
7. **Forms** - Set up contact forms with Contact Form 7 or similar

Your Alexandria Dental Health website is now successfully converted to WordPress with a custom theme that maintains the original design and functionality! 