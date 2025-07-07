# WordPress Featured Image & Content Cleaner Plugin

## Description
This plugin provides two main functions for WordPress content management:
1. **Featured Images**: Sets featured images for posts/pages using FIFU report data
2. **Content Cleanup**: Removes empty SVG placeholders and duplicate images from post content

## Features
### Featured Images
- Sets standard WordPress featured images (not FIFU meta)
- Uses existing media library images (no downloads needed)
- Processes 69 unique posts from FIFU report data
- Skips posts that already have featured images

### Content Cleanup
- Removes empty SVG placeholders from post content
- Removes duplicate consecutive images
- Cleans up extra whitespace and empty paragraphs
- Works on all published posts and pages

### General Features
- Dual-tab interface for easy navigation
- Dry run mode for both functions (preview before making changes)
- Detailed reporting of what was processed
- Safe operation with error handling

## Installation
1. Copy this entire folder to your WordPress `/wp-content/plugins/` directory
2. Activate the plugin in WordPress Admin → Plugins
3. Go to Tools → WP Featured Image & Content Cleaner

## Usage
### Featured Images Tab
1. **Always use Dry Run first** to preview what will happen
2. Check the results table to see which images will be set (69 unique posts)
3. Run without dry run to actually set the featured images
4. Review the results to confirm everything worked correctly

### Content Cleanup Tab
1. **Always use Dry Run first** to see what content needs cleaning
2. Review the posts that have SVG placeholders or duplicate images
3. Run without dry run to actually clean the post content
4. Check the results to see what was cleaned up

## Files
- `wp-featured-image-setter.php` - Main plugin file
- `corrected_fifu_featured_images_report.txt` - Data file with 103 image mappings
- `README.md` - This documentation file

## Data File Format
The report file contains mappings in this format:
```
folder_name - post_id="123" - attachment_id="N/A" - src="../wp-content/uploads/2025/01/image.webp"
```

## Requirements
- WordPress 5.0 or higher
- Images must already exist in the WordPress media library
- User must have 'manage_options' capability

## Support
This plugin was created specifically for Alexandria Dental Health website migration.

## Version History
- 2.1 - Added Content Cleanup functionality, dual-tab interface
- 2.0 - Clean plugin structure, improved error handling
- 1.0 - Initial version 