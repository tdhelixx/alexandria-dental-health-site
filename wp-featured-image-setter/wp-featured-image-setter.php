<?php
/*
Plugin Name: WordPress Featured Image Setter
Description: Sets standard WordPress featured images for posts/pages based on FIFU report data. Uses existing media library images.
Version: 2.0
Author: Alexandria Dental Health
*/

if ( ! defined( 'ABSPATH' ) ) exit; // Exit if accessed directly

// Admin page to run the tool
add_action('admin_menu', function() {
    add_management_page(
        'WP Featured Image & Content Cleaner',
        'WP Featured Image & Content Cleaner',
        'manage_options',
        'wp-featured-image-setter',
        'wpfis_admin_page'
    );
});

function wpfis_admin_page() {
    // Get active tab
    $active_tab = isset($_GET['tab']) ? $_GET['tab'] : 'featured-images';
    
    // Handle Featured Images actions
    $featured_results = [];
    if ($active_tab === 'featured-images') {
        $report_file = plugin_dir_path(__FILE__) . 'corrected_fifu_featured_images_report.txt';
        $featured_images = wpfis_parse_report($report_file);
        $dry_run = !empty($_GET['dry_run']) || !empty($_POST['dry_run']);

        if ( isset($_POST['wpfis_run']) && ! $dry_run ) {
            $featured_results = wpfis_set_featured_images( $featured_images, false );
            echo '<div class="updated"><p>Featured images have been set from existing media library images. See below for details.</p></div>';
        } elseif ( isset($_POST['wpfis_run']) && $dry_run ) {
            $featured_results = wpfis_set_featured_images( $featured_images, true );
            echo '<div class="notice notice-info"><p><strong>DRY RUN COMPLETE:</strong> No changes were made. This is a preview of what would happen.</p></div>';
        }
    }
    
    // Handle Content Cleanup actions
    $cleanup_results = [];
    if ($active_tab === 'content-cleanup') {
        $cleanup_dry_run = !empty($_GET['cleanup_dry_run']) || !empty($_POST['cleanup_dry_run']);
        
        if ( isset($_POST['wpfis_cleanup']) && ! $cleanup_dry_run ) {
            $cleanup_results = wpfis_clean_post_content( false );
            echo '<div class="updated"><p>Post content has been cleaned. See below for details.</p></div>';
        } elseif ( isset($_POST['wpfis_cleanup']) && $cleanup_dry_run ) {
            $cleanup_results = wpfis_clean_post_content( true );
            echo '<div class="notice notice-info"><p><strong>DRY RUN COMPLETE:</strong> No changes were made. This is a preview of what would happen.</p></div>';
        }
    }

    ?>
    <div class="wrap">
        <h1>WordPress Featured Image & Content Cleaner</h1>
        
        <!-- Tab Navigation -->
        <h2 class="nav-tab-wrapper">
            <a href="?page=wp-featured-image-setter&tab=featured-images" class="nav-tab <?php echo $active_tab === 'featured-images' ? 'nav-tab-active' : ''; ?>">Featured Images</a>
            <a href="?page=wp-featured-image-setter&tab=content-cleanup" class="nav-tab <?php echo $active_tab === 'content-cleanup' ? 'nav-tab-active' : ''; ?>">Content Cleanup</a>
        </h2>
        
        <?php if ($active_tab === 'featured-images'): ?>
            <!-- Featured Images Tab -->
            <div class="tab-content">
                <h3>Set Featured Images</h3>
                <p>This tool will find existing images in your media library and set them as standard WordPress featured images.</p>
                <?php if (isset($featured_images)): ?>
                    <p><strong>Report file:</strong> <?php echo esc_html($report_file); ?></p>
                    <p><strong>Images found in report:</strong> <?php echo count($featured_images); ?></p>
                    
                    <?php if (empty($featured_images)): ?>
                        <div class="notice notice-error">
                            <p>No images found in report file. Please make sure the FIFU report file exists at: <?php echo esc_html($report_file); ?></p>
                        </div>
                    <?php else: ?>
                        <form method="post">
                            <p>
                                <label>
                                    <input type="checkbox" name="dry_run" value="1" <?php checked($dry_run); ?> /> 
                                    <strong>Dry Run (preview only - RECOMMENDED for first use)</strong>
                                </label>
                            </p>
                            <p>
                                <button class="button button-primary" type="submit" name="wpfis_run" value="1">
                                    <?php echo $dry_run ? 'Preview Changes' : 'Set Featured Images'; ?>
                                </button>
                            </p>
                        </form>
                    <?php endif; ?>
                    
                    <?php if ( !empty($featured_results) ): ?>
                        <h3>Results <?php echo $dry_run ? '(Preview Mode)' : ''; ?></h3>
                        <p><strong>Total processed:</strong> <?php echo count($featured_results); ?> images</p>
                        <table class="widefat">
                            <thead>
                                <tr>
                                    <th>Post ID</th>
                                    <th>Post Title</th>
                                    <th>Image Filename</th>
                                    <th>Attachment ID</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                            <?php foreach($featured_results as $row): ?>
                                <tr>
                                    <td><?php echo esc_html($row['post_id']); ?></td>
                                    <td><?php echo esc_html($row['post_title']); ?></td>
                                    <td><?php echo esc_html($row['image_filename']); ?></td>
                                    <td><?php echo esc_html($row['attachment_id'] ?: '-'); ?></td>
                                    <td><?php echo esc_html($row['status']); ?></td>
                                </tr>
                            <?php endforeach; ?>
                            </tbody>
                        </table>
                    <?php endif; ?>
                <?php else: ?>
                    <div class="notice notice-error">
                        <p>No images found in report file.</p>
                    </div>
                <?php endif; ?>
            </div>
            
        <?php elseif ($active_tab === 'content-cleanup'): ?>
            <!-- Content Cleanup Tab -->
            <div class="tab-content">
                <h3>Clean Post Content</h3>
                <p>This tool will clean up existing post content by removing empty SVG placeholders and duplicate consecutive images.</p>
                
                <form method="post">
                    <p>
                        <label>
                            <input type="checkbox" name="cleanup_dry_run" value="1" <?php checked(!empty($_GET['cleanup_dry_run']) || !empty($_POST['cleanup_dry_run'])); ?> /> 
                            <strong>Dry Run (preview only - RECOMMENDED for first use)</strong>
                        </label>
                    </p>
                    <p>
                        <button class="button button-primary" type="submit" name="wpfis_cleanup" value="1">
                            <?php echo (!empty($_GET['cleanup_dry_run']) || !empty($_POST['cleanup_dry_run'])) ? 'Preview Content Cleanup' : 'Clean Post Content'; ?>
                        </button>
                    </p>
                </form>
                
                <?php if ( !empty($cleanup_results) ): ?>
                    <h3>Cleanup Results <?php echo (!empty($_GET['cleanup_dry_run']) || !empty($_POST['cleanup_dry_run'])) ? '(Preview Mode)' : ''; ?></h3>
                    <p><strong>Total posts processed:</strong> <?php echo count($cleanup_results); ?></p>
                    <table class="widefat">
                        <thead>
                            <tr>
                                <th>Post ID</th>
                                <th>Post Title</th>
                                <th>Changes Made</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                        <?php foreach($cleanup_results as $row): ?>
                            <tr>
                                <td><?php echo esc_html($row['post_id']); ?></td>
                                <td><?php echo esc_html($row['post_title']); ?></td>
                                <td><?php echo esc_html($row['changes']); ?></td>
                                <td><?php echo esc_html($row['status']); ?></td>
                            </tr>
                        <?php endforeach; ?>
                        </tbody>
                    </table>
                <?php endif; ?>
            </div>
        
        <?php endif; ?>
    </div>
    <?php
}

function wpfis_parse_report($file_path) {
    $featured_images = [];
    
    if (!file_exists($file_path)) {
        return $featured_images;
    }
    
    $lines = file($file_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    
    foreach ($lines as $line) {
        // Skip header lines and separators
        if (strpos($line, 'post_id=') === false) {
            continue;
        }
        
        // Parse line format: folder_name - post_id="ID" - attachment_id="ID" - src="URL"
        if (preg_match('/post_id="(\d+)".*src="([^"]+)"/', $line, $matches)) {
            $post_id = intval($matches[1]);
            $image_url = $matches[2];
            
            // Extract filename from URL
            $image_filename = basename($image_url);
            $image_filename = preg_replace('/\?.*/', '', $image_filename); // Remove query parameters
            
            $featured_images[$post_id] = $image_filename;
        }
    }
    
    return $featured_images;
}

function wpfis_set_featured_images( $map, $dry_run = true ) {
    $results = [];
    
    foreach ( $map as $post_id => $image_filename ) {
        $post = get_post($post_id);
        $row = [
            'post_id' => $post_id,
            'post_title' => $post ? $post->post_title : 'Unknown',
            'image_filename' => $image_filename,
            'attachment_id' => '',
            'status' => '',
        ];

        if ( ! $post ) {
            $row['status'] = 'Post not found';
        } elseif ( $dry_run ) {
            // For dry run, try to find the attachment to show what would happen
            $attachment_id = wpfis_get_attachment_by_filename($image_filename);
            if ($attachment_id) {
                $row['attachment_id'] = $attachment_id;
                $existing_thumbnail = get_post_thumbnail_id($post_id);
                if ($existing_thumbnail) {
                    $row['status'] = 'Already has featured image - would skip';
                } else {
                    $row['status'] = 'Would set as featured image';
                }
            } else {
                $row['status'] = 'Image not found in media library';
            }
        } else {
            // Check if post already has a featured image
            $existing_thumbnail = get_post_thumbnail_id($post_id);
            if ($existing_thumbnail) {
                $row['attachment_id'] = $existing_thumbnail;
                $row['status'] = 'Already has featured image - skipped';
            } else {
                // Find the attachment in media library
                $attachment_id = wpfis_get_attachment_by_filename($image_filename);
                
                if ($attachment_id) {
                    // Set as featured image
                    $success = set_post_thumbnail($post_id, $attachment_id);
                    
                    if ($success) {
                        $row['attachment_id'] = $attachment_id;
                        $row['status'] = 'Set as featured image';
                    } else {
                        $row['attachment_id'] = $attachment_id;
                        $row['status'] = 'Found image but failed to set as featured';
                    }
                } else {
                    $row['status'] = 'Image not found in media library';
                }
            }
        }

        $results[] = $row;
    }
    
    return $results;
}

function wpfis_get_attachment_by_filename($filename) {
    global $wpdb;
    
    // First try exact filename match
    $attachment_id = $wpdb->get_var($wpdb->prepare(
        "SELECT post_id FROM $wpdb->postmeta 
         WHERE meta_key = '_wp_attached_file' 
         AND meta_value LIKE %s 
         LIMIT 1",
        '%' . $filename
    ));
    
    if ($attachment_id) {
        return $attachment_id;
    }
    
    // If not found, try searching by post title (which is often the filename)
    $attachment_id = $wpdb->get_var($wpdb->prepare(
        "SELECT ID FROM $wpdb->posts 
         WHERE post_type = 'attachment' 
         AND post_title LIKE %s 
         LIMIT 1",
        '%' . pathinfo($filename, PATHINFO_FILENAME) . '%'
    ));
    
    return $attachment_id;
}

function wpfis_clean_post_content( $dry_run = true ) {
    $results = [];
    
    // Get all published posts and pages
    $posts = get_posts(array(
        'post_type' => array('post', 'page'),
        'post_status' => 'publish',
        'numberposts' => -1
    ));
    
    foreach ($posts as $post) {
        $original_content = $post->post_content;
        $cleaned_content = $original_content;
        $changes_made = [];
        
        // 1. Remove empty SVG placeholders
        $svg_pattern = '/<!-- wp:image -->\s*<figure class="wp-block-image"><img src="data:image\/svg\+xml[^"]*" [^>]*><\/figure>\s*<!-- \/wp:image -->/';
        $svg_matches = preg_match_all($svg_pattern, $cleaned_content);
        if ($svg_matches > 0) {
            $cleaned_content = preg_replace($svg_pattern, '', $cleaned_content);
            $changes_made[] = "Removed $svg_matches empty SVG placeholders";
        }
        
        // 2. Remove duplicate consecutive images (same src)
        $duplicate_pattern = '/(<!-- wp:image -->\s*<figure class="wp-block-image"><img src="([^"]*)"[^>]*><\/figure>\s*<!-- \/wp:image -->)\s*(?=<!-- wp:image -->\s*<figure class="wp-block-image"><img src="\2"[^>]*><\/figure>\s*<!-- \/wp:image -->)/';
        $duplicate_matches = 0;
        while (preg_match($duplicate_pattern, $cleaned_content)) {
            $cleaned_content = preg_replace($duplicate_pattern, '', $cleaned_content);
            $duplicate_matches++;
        }
        if ($duplicate_matches > 0) {
            $changes_made[] = "Removed $duplicate_matches duplicate images";
        }
        
        // 3. Clean up extra whitespace and empty paragraphs
        $cleaned_content = preg_replace('/<!-- wp:paragraph -->\s*<p><\/p>\s*<!-- \/wp:paragraph -->\s*<!-- wp:paragraph -->\s*<p><\/p>\s*<!-- \/wp:paragraph -->/', '', $cleaned_content);
        $cleaned_content = preg_replace('/\n\n\n+/', "\n\n", $cleaned_content);
        
        $row = [
            'post_id' => $post->ID,
            'post_title' => $post->post_title,
            'changes' => !empty($changes_made) ? implode(', ', $changes_made) : 'No changes needed',
            'status' => ''
        ];
        
        if ($original_content !== $cleaned_content) {
            if (!$dry_run) {
                // Actually update the post
                $updated_post = array(
                    'ID' => $post->ID,
                    'post_content' => $cleaned_content
                );
                $result = wp_update_post($updated_post);
                
                if ($result && !is_wp_error($result)) {
                    $row['status'] = 'Content updated successfully';
                } else {
                    $row['status'] = 'Error updating content';
                }
            } else {
                $row['status'] = 'Would update content';
            }
        } else {
            $row['status'] = 'No changes needed';
        }
        
        // Only include posts that had changes or would have changes
        if ($original_content !== $cleaned_content || !$dry_run) {
            $results[] = $row;
        }
    }
    
    return $results;
}
?> 