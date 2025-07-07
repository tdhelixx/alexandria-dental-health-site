<?php
/**
 * WordPress Media Library Cleanup Script
 * Removes thumbnail duplicates and keeps only original images
 * RUN ONCE THEN DELETE THIS FILE
 */

// Load WordPress
require_once('wp-config.php');
require_once('wp-includes/wp-db.php');
require_once('wp-includes/functions.php');
require_once('wp-includes/option.php');
require_once('wp-admin/includes/image.php');
require_once('wp-admin/includes/file.php');
require_once('wp-admin/includes/media.php');

echo "<h2>WordPress Media Library Cleanup</h2>";
echo "<p><strong>This will remove thumbnail duplicates from your Media Library</strong></p>";

// Get all attachments
global $wpdb;
$attachments = $wpdb->get_results("
    SELECT ID, post_title, guid 
    FROM {$wpdb->posts} 
    WHERE post_type = 'attachment' 
    AND post_mime_type LIKE 'image/%'
    ORDER BY post_title
");

echo "<h3>Current Media Library Status:</h3>";
echo "<p><strong>Total attachments found:</strong> " . count($attachments) . "</p>";

// Analyze which are thumbnails
$thumbnails_to_delete = array();
$originals_to_keep = array();

foreach ($attachments as $attachment) {
    $filename = basename($attachment->guid);
    
    // Check if this looks like a WordPress thumbnail (contains -NUMBERxNUMBER)
    if (preg_match('/-\d+x\d+\./', $filename)) {
        $thumbnails_to_delete[] = $attachment;
    } else {
        $originals_to_keep[] = $attachment;
    }
}

echo "<p><strong>Original images to keep:</strong> " . count($originals_to_keep) . "</p>";
echo "<p><strong>Thumbnail duplicates to remove:</strong> " . count($thumbnails_to_delete) . "</p>";

// Show some examples
echo "<h3>Examples of what will be removed:</h3>";
echo "<ul>";
for ($i = 0; $i < min(10, count($thumbnails_to_delete)); $i++) {
    echo "<li>" . esc_html(basename($thumbnails_to_delete[$i]->guid)) . "</li>";
}
if (count($thumbnails_to_delete) > 10) {
    echo "<li><em>... and " . (count($thumbnails_to_delete) - 10) . " more thumbnail files</em></li>";
}
echo "</ul>";

echo "<h3>Examples of what will be kept:</h3>";
echo "<ul>";
for ($i = 0; $i < min(10, count($originals_to_keep)); $i++) {
    echo "<li>" . esc_html(basename($originals_to_keep[$i]->guid)) . "</li>";
}
if (count($originals_to_keep) > 10) {
    echo "<li><em>... and " . (count($originals_to_keep) - 10) . " more original files</em></li>";
}
echo "</ul>";

// Add confirmation button
if (!isset($_POST['confirm_cleanup'])) {
    echo "<form method='post'>";
    echo "<h3>⚠️ Confirmation Required</h3>";
    echo "<p><strong>This will permanently delete " . count($thumbnails_to_delete) . " thumbnail duplicates from your Media Library.</strong></p>";
    echo "<p>Original images (" . count($originals_to_keep) . ") will be preserved.</p>";
    echo "<label><input type='checkbox' name='confirm_cleanup' value='1' required> I understand this will delete thumbnail duplicates</label><br><br>";
    echo "<input type='submit' value='Clean Up Media Library' style='background: #d63638; color: white; padding: 10px 20px; border: none; cursor: pointer;'>";
    echo "</form>";
} else {
    // Perform cleanup
    echo "<h3>🧹 Performing Cleanup...</h3>";
    
    $deleted_count = 0;
    $error_count = 0;
    
    foreach ($thumbnails_to_delete as $attachment) {
        $result = wp_delete_attachment($attachment->ID, true);
        if ($result) {
            $deleted_count++;
            if ($deleted_count <= 20) {
                echo "<p>✅ Deleted: " . esc_html(basename($attachment->guid)) . "</p>";
            } elseif ($deleted_count % 50 === 0) {
                echo "<p><em>Progress: {$deleted_count} deleted so far...</em></p>";
                flush();
            }
        } else {
            $error_count++;
            if ($error_count <= 5) {
                echo "<p>❌ Error deleting: " . esc_html(basename($attachment->guid)) . "</p>";
            }
        }
    }
    
    echo "<div style='background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; margin: 20px 0;'>";
    echo "<h3>✅ Cleanup Complete!</h3>";
    echo "<p><strong>Deleted:</strong> {$deleted_count} thumbnail duplicates</p>";
    echo "<p><strong>Errors:</strong> {$error_count}</p>";
    echo "<p><strong>Remaining:</strong> " . count($originals_to_keep) . " original images</p>";
    echo "</div>";
    
    echo "<h3>Next Steps:</h3>";
    echo "<ol>";
    echo "<li>Go to <a href='" . admin_url('upload.php') . "'>Media Library</a> to verify cleanup</li>";
    echo "<li>You should now see ~" . count($originals_to_keep) . " items instead of " . count($attachments) . "</li>";
    echo "<li><strong style='color: red;'>DELETE THIS FILE</strong> for security</li>";
    echo "</ol>";
}

echo "<hr>";
echo "<p><em>Script run at " . date('Y-m-d H:i:s') . "</em></p>";
?> 