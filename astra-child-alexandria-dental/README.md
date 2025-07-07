# Astra Child Theme - Alexandria Dental Health

A custom WordPress child theme built on the Astra framework for Alexandria Dental Health & Smile Studio.

## Features

✅ **Professional Dental Design** - Custom header with multi-row layout  
✅ **Perfect Two-Column Layout** - Content area with dedicated sidebar  
✅ **Special Offers Button** - Prominent yellow circular call-to-action  
✅ **Google Maps Integration** - Embedded location map in sidebar  
✅ **Mobile Responsive** - Optimized for all devices  
✅ **SEO Optimized** - Clean code and proper heading structure  
✅ **Performance Optimized** - Minimal bloat, fast loading  

## Installation

1. **Install Parent Theme First**
   - Upload and activate the Astra theme (located in `../Astra Theme/`)
   - Make sure Astra is active before proceeding

2. **Install Child Theme**
   - Upload the `astra-child-alexandria-dental` folder to `/wp-content/themes/`
   - Activate "Astra Child - Alexandria Dental Health" from WordPress admin

3. **Setup Menus**
   - Go to Appearance > Menus
   - Create a "Primary Menu" and assign to "Primary Menu" location
   - Create a "Footer Menu" and assign to "Footer Menu" location

4. **Upload Logo**
   - Go to Appearance > Customize > Site Identity
   - Upload your dental practice logo
   - The logo will automatically appear in both header rows

## Theme Structure

### Header Layout
- **Top Bar**: Small logo, "Love Your Smile" tagline, special offers button
- **Main Header**: Large logo, phone number, action buttons
- **Navigation**: Full-width menu bar with dental practice pages

### Content Layout
- **Banner Image**: Full-width featured image above content
- **Two-Column Layout**: 66% content area + 33% sidebar
- **Sidebar Contents**: Special offers button, contact info, hours, Google Maps

### Footer
- **Simple Design**: Copyright notice and footer menu links

## Customization Options

### Colors (CSS Variables)
```css
:root {
    --primary-color: #32192f;    /* Dark purple */
    --secondary-color: #a27295;  /* Light purple */
    --accent-color: #ffae00;     /* Yellow/orange */
    --hover-color: #72b7bc;      /* Teal */
}
```

### Fonts
- **Headings**: Raleway (Google Fonts)
- **Body Text**: Nunito (Google Fonts)

### Phone Number
Update in `functions.php` line 125:
```php
<a href="tel:7032129622">(703) 212-9622</a>
```

### Office Hours
Update in `functions.php` lines 190-197:
```php
<p><strong>Monday:</strong> 8:00 AM - 5:00 PM<br>
<!-- Update each day as needed -->
```

### Google Maps
Update the iframe src in `functions.php` line 202 with your actual Google Maps embed code.

## Page Templates

### Standard Pages
- Use the default Astra page layout
- Automatically includes sidebar and banner image

### Custom Dental Template
- Template Name: "Dental Page"
- Ensures perfect two-column layout
- Prevents duplicate H1 tags
- Optimized for page builder content

## CSS Classes Reference

### Layout Classes
- `.dental-banner-hero` - Full-width banner image
- `.dental-sidebar` - Custom sidebar container
- `.dental-sidebar-card` - Individual sidebar sections

### Header Classes
- `.dental-top-bar` - Top header row
- `.dental-main-header` - Main header row
- `.dental-navigation` - Navigation menu row

### Button Classes
- `.dental-special-link` - Yellow circular special offers button
- `.dental-btn` - Generic button styling
- `.dental-btn-special` - Yellow special offers button
- `.dental-btn-schedule` - Purple schedule button

## Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers

## Performance Features

- **Optimized CSS**: Minimal, efficient styling
- **Google Fonts**: Preloaded for better performance  
- **Clean HTML**: Semantic, accessible markup
- **Mobile First**: Responsive design approach

## SEO Features

- **Proper Heading Structure**: Prevents duplicate H1 tags
- **Schema Markup**: Built-in Astra SEO features
- **Fast Loading**: Optimized assets and code
- **Mobile Friendly**: Google Mobile-First indexing ready

## Maintenance

### Regular Updates
1. Keep Astra parent theme updated
2. Test child theme after parent updates
3. Backup before any major changes

### Adding New Pages
1. Create page in WordPress admin
2. Set featured image for banner
3. Choose "Dental Page" template if needed
4. Content will automatically use two-column layout

## Troubleshooting

### Layout Issues
- Ensure Astra parent theme is active
- Check that CSS is loading properly
- Clear any caching plugins

### Sidebar Not Showing
- Verify sidebar widgets are configured
- Check page template selection
- Ensure two-column layout is enabled

### Header Problems
- Upload logo through Customizer
- Check menu assignments
- Verify functions.php is loading

## Support

For technical support or customization requests, contact your web developer or WordPress administrator.

## Version History

- **v1.0.0** - Initial release with complete dental practice design
- Custom header, sidebar, and layout implementation
- Google Maps integration and special offers button
- Mobile responsive design and SEO optimization 