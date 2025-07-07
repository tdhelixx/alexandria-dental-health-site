<?php
/**
 * Alexandria Dental Health - Auto Menu Creator
 * 
 * Instructions:
 * 1. Upload this file to your WordPress root directory
 * 2. Visit: yoursite.com/create-navigation-menu.php
 * 3. Delete this file after running
 * 
 * WARNING: This will create/overwrite a menu called "Primary Menu"
 */

// Include WordPress
require_once('wp-config.php');
require_once('wp-load.php');

// Check if user is admin (security)
if (!current_user_can('manage_options')) {
    die('Access denied. You must be logged in as an administrator.');
}

echo "<h1>Alexandria Dental Health - Menu Creator</h1>";

// Delete existing "Primary Menu" if it exists
$existing_menu = wp_get_nav_menu_object('Primary Menu');
if ($existing_menu) {
    wp_delete_nav_menu($existing_menu->term_id);
    echo "<p>✅ Deleted existing 'Primary Menu'</p>";
}

// Create new menu
$menu_id = wp_create_nav_menu('Primary Menu');
if (is_wp_error($menu_id)) {
    die('Error creating menu: ' . $menu_id->get_error_message());
}

echo "<p>✅ Created new 'Primary Menu' (ID: $menu_id)</p>";

// Menu structure
$menu_items = array(
    // Main items
    array(
        'title' => 'Home',
        'url' => home_url('/'),
        'parent' => 0
    ),
    array(
        'title' => 'About',
        'url' => home_url('/about/'),
        'parent' => 0
    ),
    array(
        'title' => 'Services',
        'url' => home_url('/services/'),
        'parent' => 0,
        'is_parent' => true
    ),
    array(
        'title' => 'Contact',
        'url' => home_url('/contact-us/'),
        'parent' => 0
    ),
    array(
        'title' => 'Blog',
        'url' => home_url('/blog/'),
        'parent' => 0
    ),
    
    // Services submenu
    array(
        'title' => 'Cosmetic Dentistry',
        'url' => home_url('/cosmetic-dentistry/'),
        'parent' => 'Services'
    ),
    array(
        'title' => 'Dental Implants',
        'url' => home_url('/dental-implants/'),
        'parent' => 'Services'
    ),
    array(
        'title' => 'Invisalign',
        'url' => home_url('/invisalign/'),
        'parent' => 'Services'
    ),
    array(
        'title' => 'Teeth Whitening',
        'url' => home_url('/teeth-whitening/'),
        'parent' => 'Services'
    ),
    array(
        'title' => 'Dental Crowns',
        'url' => home_url('/dental-crowns/'),
        'parent' => 'Services'
    ),
    array(
        'title' => 'Veneers',
        'url' => home_url('/veneers/'),
        'parent' => 'Services'
    ),
    array(
        'title' => 'Root Canal Therapy',
        'url' => home_url('/root-canal-therapy/'),
        'parent' => 'Services'
    ),
    array(
        'title' => 'Emergency Dentistry',
        'url' => home_url('/emergency-dentistry/'),
        'parent' => 'Services'
    ),
    
    // Patient Information section
    array(
        'title' => 'Patient Information',
        'url' => home_url('/patient-information/'),
        'parent' => 0,
        'is_parent' => true
    ),
    array(
        'title' => 'New Patients',
        'url' => home_url('/patient-information/'),
        'parent' => 'Patient Information'
    ),
    array(
        'title' => 'Insurance',
        'url' => home_url('/dental-insurance-accepted/'),
        'parent' => 'Patient Information'
    ),
    array(
        'title' => 'Office Tour',
        'url' => home_url('/office-tour/'),
        'parent' => 'Patient Information'
    ),
    array(
        'title' => 'Testimonials',
        'url' => home_url('/testimonials/'),
        'parent' => 'Patient Information'
    )
);

// Track parent IDs
$parent_ids = array();
$menu_order = 1;

// Add all menu items
foreach ($menu_items as $item) {
    $parent_id = 0;
    
    // Handle parent relationships
    if ($item['parent'] !== 0 && isset($parent_ids[$item['parent']])) {
        $parent_id = $parent_ids[$item['parent']];
    }
    
    // Add menu item
    $menu_item_id = wp_update_nav_menu_item($menu_id, 0, array(
        'menu-item-title' => $item['title'],
        'menu-item-url' => $item['url'],
        'menu-item-status' => 'publish',
        'menu-item-type' => 'custom',
        'menu-item-parent-id' => $parent_id,
        'menu-item-position' => $menu_order
    ));
    
    if (is_wp_error($menu_item_id)) {
        echo "<p>❌ Error adding '{$item['title']}': " . $menu_item_id->get_error_message() . "</p>";
    } else {
        echo "<p>✅ Added '{$item['title']}' (ID: $menu_item_id)</p>";
        
        // Store parent ID for children
        if (isset($item['is_parent']) && $item['is_parent']) {
            $parent_ids[$item['title']] = $menu_item_id;
        }
    }
    
    $menu_order++;
}

// Assign menu to Primary Navigation location
$locations = get_theme_mod('nav_menu_locations');
$locations['primary'] = $menu_id;
set_theme_mod('nav_menu_locations', $locations);

echo "<p>✅ Assigned menu to 'Primary Navigation' location</p>";

echo "<h2>🎉 DONE!</h2>";
echo "<p><strong>Your navigation menu has been created!</strong></p>";
echo "<p>📋 <strong>Next steps:</strong></p>";
echo "<ul>";
echo "<li>✅ Visit your website to see the new navigation</li>";
echo "<li>✅ Delete this file from your server for security</li>";
echo "<li>✅ Fine-tune the menu in Appearance → Menus if needed</li>";
echo "</ul>";

echo "<p><a href='" . home_url() . "' target='_blank'>🔗 View Your Site</a> | ";
echo "<a href='" . admin_url('nav-menus.php') . "' target='_blank'>🔗 Edit Menus</a></p>";
?> 