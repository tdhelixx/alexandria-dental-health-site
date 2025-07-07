<?php
/**
 * Standalone Content Extractor for Alexandria Dental Health
 * Run this script directly to clean Beaver Builder content
 */

// Load WordPress
require_once('wp-config.php');
require_once('wp-load.php');

if (!current_user_can('manage_options')) {
    die('Access denied. Please log in as administrator.');
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>Content Extractor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .wrap { max-width: 1200px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #f4f4f4; }
        .status-needs { color: orange; font-weight: bold; }
        .status-clean { color: green; font-weight: bold; }
        .button { background: #0073aa; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .button:hover { background: #005a87; }
        .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 15px; margin: 20px 0; }
        .processing { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 15px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="wrap">
        <h1>🛠️ Content Extractor</h1>
        <p>Extract clean content from Beaver Builder HTML and make it Gutenberg-friendly.</p>

<?php

// Handle form submission
if (isset($_POST['extract_content'])) {
    $post_ids = $_POST['post_ids'] ?? array();
    
    if (empty($post_ids)) {
        echo '<div class="processing">❌ No pages selected for extraction.</div>';
    } else {
        echo '<div class="processing">🔄 Processing ' . count($post_ids) . ' pages...</div>';
        
        $processed = 0;
        foreach ($post_ids as $post_id) {
            $post = get_post($post_id);
            if (!$post) continue;
            
            $original_content = $post->post_content;
            $clean_content = extract_bb_content($original_content);
            
            if ($clean_content !== $original_content) {
                wp_update_post(array(
                    'ID' => $post_id,
                    'post_content' => $clean_content
                ));
                $processed++;
                echo "<p>✅ Cleaned: " . esc_html($post->post_title) . "</p>";
            }
        }
        
        echo '<div class="success">🎉 Successfully extracted content from ' . $processed . ' pages!</div>';
        echo '<p><strong>Next steps:</strong></p>';
        echo '<ol>';
        echo '<li>Go to your WordPress admin → Pages</li>';
        echo '<li>Edit any extracted page</li>';
        echo '<li>Use "Convert to Blocks" - it should work much better now!</li>';
        echo '</ol>';
    }
}

// Get all posts and pages
$posts = get_posts(array(
    'post_type' => array('page', 'post'),
    'posts_per_page' => -1,
    'post_status' => 'publish',
    'orderby' => 'title',
    'order' => 'ASC'
));

?>

        <form method="post" action="">
            <table>
                <thead>
                    <tr>
                        <th width="50">
                            <input type="checkbox" id="select-all" onclick="toggleAll(this)"> 
                        </th>
                        <th>Page/Post Title</th>
                        <th>Type</th>
                        <th>Status</th>
                        <th>Content Preview</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    $bb_count = 0;
                    foreach ($posts as $post) {
                        $has_bb_content = strpos($post->post_content, 'fl-builder-content') !== false;
                        if ($has_bb_content) $bb_count++;
                        
                        $preview = substr(strip_tags($post->post_content), 0, 100) . '...';
                        ?>
                        <tr>
                            <td>
                                <?php if ($has_bb_content): ?>
                                <input type="checkbox" name="post_ids[]" value="<?php echo $post->ID; ?>">
                                <?php endif; ?>
                            </td>
                            <td>
                                <strong><?php echo esc_html($post->post_title); ?></strong>
                                <br><small><a href="<?php echo get_permalink($post->ID); ?>" target="_blank">View</a> | 
                                <a href="<?php echo get_edit_post_link($post->ID); ?>" target="_blank">Edit</a></small>
                            </td>
                            <td><?php echo ucfirst($post->post_type); ?></td>
                            <td>
                                <?php if ($has_bb_content): ?>
                                    <span class="status-needs">🔧 Needs Extraction</span>
                                <?php else: ?>
                                    <span class="status-clean">✅ Clean</span>
                                <?php endif; ?>
                            </td>
                            <td><small><?php echo esc_html($preview); ?></small></td>
                        </tr>
                        <?php
                    }
                    ?>
                </tbody>
            </table>
            
            <p>
                <strong>Found <?php echo $bb_count; ?> pages/posts with Beaver Builder content that need extraction.</strong>
            </p>
            
            <?php if ($bb_count > 0): ?>
            <p>
                <button type="submit" name="extract_content" class="button">
                    🚀 Extract Selected Content
                </button>
                <button type="button" onclick="selectAllBB()" class="button" style="background: #666;">
                    Select All BB Pages
                </button>
            </p>
            <?php else: ?>
            <p><em>✅ All content is already clean! No extraction needed.</em></p>
            <?php endif; ?>
        </form>
    </div>

    <script>
    function toggleAll(source) {
        checkboxes = document.querySelectorAll('input[name="post_ids[]"]');
        for(var i=0, n=checkboxes.length;i<n;i++) {
            checkboxes[i].checked = source.checked;
        }
    }
    
    function selectAllBB() {
        checkboxes = document.querySelectorAll('input[name="post_ids[]"]');
        for(var i=0, n=checkboxes.length;i<n;i++) {
            checkboxes[i].checked = true;
        }
        document.getElementById('select-all').checked = true;
    }
    </script>
</body>
</html>

<?php

function extract_bb_content($html) {
    // Parse HTML with DOMDocument
    $dom = new DOMDocument();
    libxml_use_internal_errors(true);
    $dom->loadHTML('<?xml encoding="UTF-8">' . $html);
    libxml_clear_errors();
    
    $xpath = new DOMXPath($dom);
    $clean_content = '';
    
    // Extract headings in order
    $headings = $xpath->query('//h1 | //h2 | //h3 | //h4 | //h5 | //h6');
    foreach ($headings as $heading) {
        $text = trim($heading->textContent);
        if (!empty($text) && strlen($text) > 2) {
            $tag = $heading->tagName;
            $clean_content .= "<{$tag}>{$text}</{$tag}>\n\n";
        }
    }
    
    // Extract paragraphs
    $paragraphs = $xpath->query('//p[string-length(normalize-space(text()))>15]');
    foreach ($paragraphs as $p) {
        $text = trim($p->textContent);
        if (!empty($text)) {
            $clean_content .= "<p>{$text}</p>\n\n";
        }
    }
    
    // Extract images
    $images = $xpath->query('//img[@src]');
    foreach ($images as $img) {
        $src = $img->getAttribute('src');
        $alt = $img->getAttribute('alt');
        $title = $img->getAttribute('title');
        
        if (!empty($src)) {
            $img_html = "<img src=\"{$src}\"";
            if (!empty($alt)) $img_html .= " alt=\"{$alt}\"";
            if (!empty($title)) $img_html .= " title=\"{$title}\"";
            $img_html .= " />";
            $clean_content .= $img_html . "\n\n";
        }
    }
    
    // Extract buttons/links
    $buttons = $xpath->query('//a[contains(@class, "fl-button") or contains(@class, "button")]');
    foreach ($buttons as $button) {
        $href = $button->getAttribute('href');
        $text = trim($button->textContent);
        
        if (!empty($href) && !empty($text)) {
            $clean_content .= "<p><a href=\"{$href}\" class=\"button\">{$text}</a></p>\n\n";
        }
    }
    
    // If nothing was extracted, try to get any meaningful text
    if (empty(trim($clean_content))) {
        // Get all text content, cleaned up
        $all_text = $xpath->query('//text()[normalize-space()]');
        $text_parts = array();
        
        foreach ($all_text as $text_node) {
            $text = trim($text_node->textContent);
            if (strlen($text) > 10 && !in_array($text, $text_parts)) {
                $text_parts[] = $text;
            }
        }
        
        if (!empty($text_parts)) {
            $clean_content = "<p>" . implode("</p>\n\n<p>", $text_parts) . "</p>";
        }
    }
    
    return empty(trim($clean_content)) ? $html : $clean_content;
}

?> 