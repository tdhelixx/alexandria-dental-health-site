<?php
/**
 * WordPress URL Fix Script for Local by Flywheel
 * This script updates WordPress URLs in the database to match the Local domain
 * Run this once, then delete it for security
 */

// Define the new URL (update this to match your Local site)
define('NEW_SITE_URL', 'http://alexandriadentalhealthcom.local');
define('NEW_HOME_URL', 'http://alexandriadentalhealthcom.local');

// Try to find wp-config.php in parent directories (Local structure)
$config_file = null;
$search_paths = [
    __DIR__ . '/wp-config.php',
    dirname(__DIR__) . '/wp-config.php',
    dirname(dirname(__DIR__)) . '/wp-config.php',
];

foreach ($search_paths as $path) {
    if (file_exists($path)) {
        $config_file = $path;
        break;
    }
}

if (!$config_file) {
    die('wp-config.php not found. Please run this script from your WordPress directory.');
}

// Load WordPress
require_once($config_file);
require_once(ABSPATH . 'wp-includes/wp-db.php');
require_once(ABSPATH . 'wp-includes/functions.php');
require_once(ABSPATH . 'wp-includes/option.php');

// Initialize WordPress database
global $wpdb;
if (!isset($wpdb)) {
    $wpdb = new wpdb(DB_USER, DB_PASSWORD, DB_NAME, DB_HOST);
}

echo "<h2>WordPress URL Fix for Local by Flywheel</h2>";

// Get current URLs
$current_site_url = get_option('siteurl');
$current_home_url = get_option('home');

echo "<h3>Current Settings:</h3>";
echo "<strong>Site URL:</strong> " . $current_site_url . "<br>";
echo "<strong>Home URL:</strong> " . $current_home_url . "<br>";

echo "<h3>New Settings:</h3>";
echo "<strong>New Site URL:</strong> " . NEW_SITE_URL . "<br>";
echo "<strong>New Home URL:</strong> " . NEW_HOME_URL . "<br>";

// Update the URLs
$updated_site = update_option('siteurl', NEW_SITE_URL);
$updated_home = update_option('home', NEW_HOME_URL);

echo "<h3>Update Results:</h3>";
echo "<strong>Site URL Updated:</strong> " . ($updated_site ? 'YES' : 'NO') . "<br>";
echo "<strong>Home URL Updated:</strong> " . ($updated_home ? 'YES' : 'NO') . "<br>";

// Also update any hardcoded URLs in content
$old_url_patterns = [
    'http://localhost',
    'https://localhost',
    'http://127.0.0.1',
    'https://127.0.0.1',
    'alexandriadentalhealth.com',
    'http://alexandriadentalhealth.com',
    'https://alexandriadentalhealth.com'
];

echo "<h3>Updating Content URLs:</h3>";
foreach ($old_url_patterns as $old_url) {
    // Update post content
    $posts_updated = $wpdb->query(
        $wpdb->prepare(
            "UPDATE {$wpdb->posts} SET post_content = REPLACE(post_content, %s, %s)",
            $old_url,
            NEW_SITE_URL
        )
    );
    
    // Update post excerpts
    $excerpts_updated = $wpdb->query(
        $wpdb->prepare(
            "UPDATE {$wpdb->posts} SET post_excerpt = REPLACE(post_excerpt, %s, %s)",
            $old_url,
            NEW_SITE_URL
        )
    );
    
    // Update options
    $options_updated = $wpdb->query(
        $wpdb->prepare(
            "UPDATE {$wpdb->options} SET option_value = REPLACE(option_value, %s, %s)",
            $old_url,
            NEW_SITE_URL
        )
    );
    
    if ($posts_updated > 0 || $excerpts_updated > 0 || $options_updated > 0) {
        echo "<strong>Updated URLs from:</strong> $old_url<br>";
        echo "- Posts: $posts_updated<br>";
        echo "- Excerpts: $excerpts_updated<br>";
        echo "- Options: $options_updated<br><br>";
    }
}

// Clear any caches
wp_cache_flush();

echo "<h3>Additional Steps:</h3>";
echo "<ul>";
echo "<li>✓ WordPress URLs updated in database</li>";
echo "<li>✓ Content URLs updated</li>";
echo "<li>✓ Cache cleared</li>";
echo "<li><strong>Next:</strong> Go to WordPress Admin → Settings → Permalinks and click 'Save Changes'</li>";
echo "<li><strong>Security:</strong> Delete this file after use</li>";
echo "</ul>";

echo "<p><strong>You can now visit:</strong> <a href='" . NEW_SITE_URL . "' target='_blank'>" . NEW_SITE_URL . "</a></p>";
echo "<p><strong>WordPress Admin:</strong> <a href='" . NEW_SITE_URL . "/wp-admin' target='_blank'>" . NEW_SITE_URL . "/wp-admin</a></p>";

?> 