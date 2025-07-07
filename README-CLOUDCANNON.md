# Alexandria Dental Health - CloudCannon Site

This repository contains the CloudCannon-ready version of the Alexandria Dental Health website.

## Overview

This is a static HTML site optimized for CloudCannon CMS deployment. The site was originally a WordPress site that has been converted to static HTML pages for better performance and easier management through CloudCannon.

## Site Structure

```
/
├── index.html                 # Homepage
├── about/                     # About pages
├── blog/                      # Blog posts
├── services/                  # Service pages (dental procedures)
├── contact-us/               # Contact information
├── smile-gallery/            # Before/after photos
├── assets/                   # CSS, JS, images
├── cloudcannon.config.yml    # CloudCannon configuration
└── README-CLOUDCANNON.md     # This file
```

## CloudCannon Setup

1. **Connect Repository**: Connect this Git repository to your CloudCannon site
2. **Build Settings**: CloudCannon will automatically detect the configuration from `cloudcannon.config.yml`
3. **Content Management**: Use CloudCannon's visual editor to manage content

## Key Features

- **Static HTML**: Fast loading times
- **Mobile Responsive**: Works on all devices
- **SEO Optimized**: Proper meta tags and structure
- **Contact Forms**: Ready for CloudCannon form handling
- **Image Gallery**: Smile gallery with before/after photos
- **Blog System**: WordPress posts converted to static pages

## Content Areas

### Pages
- Homepage (`index.html`)
- About Us (`about/index.html`)
- Services (various `/[service-name]/index.html`)
- Contact (`contact-us/index.html`)

### Blog
- Located in `/blog/` directory
- Each post has its own subdirectory with `index.html`

### Dental Services
Individual service pages include:
- Dental Implants
- Invisalign
- Teeth Whitening
- Root Canal Therapy
- Dental Crowns
- Veneers
- And many more...

## CloudCannon Configuration

The `cloudcannon.config.yml` file includes:
- Collection settings for pages and blog posts
- Editor configuration for content management
- Input types for metadata
- Asset path configuration

## Deployment

1. Push changes to the main branch
2. CloudCannon will automatically build and deploy
3. Preview changes in CloudCannon's staging environment
4. Publish to live site when ready

## Development

To work on this site locally:
1. Clone the repository
2. Open `index.html` in a browser
3. Make changes to HTML/CSS files
4. Test thoroughly before pushing

## Assets

- **CSS**: Main stylesheet is `alexandria-dental-enhanced-styles.css`
- **Images**: Various directories contain optimized images
- **Fonts**: Google Fonts loaded via CDN for performance

## Contact Information

Website: Alexandria Dental Health
Location: Alexandria, VA
Services: Comprehensive dental care

## Notes

- This site was converted from WordPress to static HTML
- All dynamic functionality has been preserved through CloudCannon
- Forms are configured for CloudCannon's form handling
- SEO structure maintained from original site 