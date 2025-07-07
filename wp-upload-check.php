<?php
/**
 * WordPress Upload Directory Diagnostic
 * Run this file in your WordPress root to check upload settings
 * DELETE THIS FILE AFTER USE FOR SECURITY
 */

// WordPress bootstrap
require_once('wp-config.php');
require_once('wp-includes/wp-db.php');
require_once('wp-includes/functions.php');
require_once('wp-includes/option.php');

echo "<h2>WordPress Upload Directory Diagnostic</h2>";

// Get upload directory information
$upload_dir = wp_upload_dir();

echo "<h3>Upload Directory Information:</h3>";
echo "<pre>";
print_r($upload_dir);
echo "</pre>";

echo "<h3>WordPress Constants:</h3>";
echo "<strong>ABSPATH:</strong> " . ABSPATH . "<br>";
echo "<strong>WP_CONTENT_DIR:</strong> " . (defined('WP_CONTENT_DIR') ? WP_CONTENT_DIR : 'Not defined') . "<br>";
echo "<strong>WP_CONTENT_URL:</strong> " . (defined('WP_CONTENT_URL') ? WP_CONTENT_URL : 'Not defined') . "<br>";
echo "<strong>UPLOADS:</strong> " . (defined('UPLOADS') ? UPLOADS : 'Not defined') . "<br>";

echo "<h3>File System Check:</h3>";
$upload_path = $upload_dir['basedir'];
echo "<strong>Upload Path:</strong> " . $upload_path . "<br>";
echo "<strong>Path Exists:</strong> " . (file_exists($upload_path) ? 'YES' : 'NO') . "<br>";
echo "<strong>Is Writable:</strong> " . (is_writable($upload_path) ? 'YES' : 'NO') . "<br>";
echo "<strong>Directory Permissions:</strong> " . substr(sprintf('%o', fileperms($upload_path)), -4) . "<br>";

echo "<h3>Current Directory Structure:</h3>";
if (file_exists($upload_path)) {
    $files = scandir($upload_path);
    echo "<pre>";
    foreach ($files as $file) {
        if ($file != '.' && $file != '..') {
            echo $file . " - " . (is_dir($upload_path . '/' . $file) ? '[DIR]' : '[FILE]') . "\n";
        }
    }
    echo "</pre>";
} else {
    echo "<strong style='color: red;'>Upload directory does not exist!</strong>";
}

echo "<h3>WordPress Options:</h3>";
echo "<strong>upload_path:</strong> " . get_option('upload_path') . "<br>";
echo "<strong>upload_url_path:</strong> " . get_option('upload_url_path') . "<br>";

?> 