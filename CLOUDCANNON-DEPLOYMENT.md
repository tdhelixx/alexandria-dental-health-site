# CloudCannon Deployment Guide
## Alexandria Dental Health Website

### Quick Setup Steps

1. **Connect to CloudCannon**
   - Log into your CloudCannon account
   - Click "Add Site" → "Connect your own files"
   - Connect this Git repository
   - Select the `cloudcannon-production` branch

2. **Build Settings**
   - CloudCannon will automatically detect the configuration from `cloudcannon.config.yml`
   - Build command: `npm run build` (11ty build process)
   - Build output: `_site/` directory
   - Install command: `npm install`

3. **Domain Setup**
   - Add your domain in CloudCannon Site Settings
   - Update DNS to point to CloudCannon's servers
   - Enable SSL certificate

4. **Content Management**
   - Use CloudCannon's visual editor for page content
   - Blog posts are in `src/blog/` directory (Markdown files)
   - Service pages in `src/services/` directory (Markdown files)
   - Page templates in `src/_includes/layouts/` directory
   - Homepage at `src/index.njk`

### Key Files

- `cloudcannon.config.yml` - CloudCannon configuration
- `.eleventy.js` - 11ty configuration
- `package.json` - Node.js dependencies and build scripts
- `src/` - Source files directory
  - `src/_includes/layouts/` - Page templates
  - `src/blog/` - Blog posts (Markdown)
  - `src/services/` - Service pages (Markdown)
  - `src/pages/` - Regular pages (Markdown)
  - `src/index.njk` - Homepage template
- `alexandria-dental-enhanced-styles.css` - Main stylesheet

### Forms Configuration

Contact forms are ready for CloudCannon's form handling:
- Contact page: `/contact-us/`
- Forms will automatically work with CloudCannon

### SEO & Performance

- All pages have proper meta tags
- Images are optimized
- Mobile responsive design
- Fast loading static HTML

### Content Updates

After connecting to CloudCannon:
1. Edit content through CloudCannon's interface
2. Changes auto-save and publish
3. No need to commit to Git manually

### Support

For technical issues:
- Check CloudCannon documentation
- Contact CloudCannon support
- Review `README-CLOUDCANNON.md` for detailed info

### Branch Information

- **Main Branch**: `master` (development)
- **Production Branch**: `cloudcannon-production` (live site)
- Always deploy from `cloudcannon-production` branch 