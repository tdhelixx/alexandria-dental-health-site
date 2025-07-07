<?php
/**
 * Plugin Name: Simple Extractor Direct
 * Description: Direct content extractor - no complex structure
 * Version: 1.0
 */

if (!defined('ABSPATH')) exit;

// Add admin menu after WordPress fully loads
add_action('init', 'init_content_extractor');

function init_content_extractor() {
    if (is_admin()) {
        add_action('admin_menu', 'add_simple_extractor_menu');
    }
}

function add_simple_extractor_menu() {
    if (function_exists('add_tools_page')) {
        add_tools_page(
            'Content Extractor',
            'Content Extractor', 
            'manage_options',
            'content-extractor',
            'show_extractor_page'
        );
    }
}

function show_extractor_page() {
    ?>
    <div class="wrap">
        <h1>Content Extractor</h1>
        <p>Extract clean content from Beaver Builder HTML.</p>
        
        <div id="results"></div>
        
        <form id="extractor-form">
            <table class="wp-list-table widefat fixed striped">
                <thead>
                    <tr>
                        <th width="50"><input type="checkbox" id="select-all"></th>
                        <th>Title</th>
                        <th>Type</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <?php
                    $posts = get_posts(array(
                        'post_type' => array('page', 'post'),
                        'posts_per_page' => -1,
                        'post_status' => 'publish'
                    ));
                    
                    foreach ($posts as $post) {
                        $has_bb = strpos($post->post_content, 'fl-builder-content') !== false;
                        ?>
                        <tr>
                            <td>
                                <?php if ($has_bb): ?>
                                <input type="checkbox" name="post_ids[]" value="<?php echo $post->ID; ?>">
                                <?php endif; ?>
                            </td>
                            <td><?php echo esc_html($post->post_title); ?></td>
                            <td><?php echo $post->post_type; ?></td>
                            <td>
                                <?php if ($has_bb): ?>
                                    <span style="color: orange;">🔧 Needs Extraction</span>
                                <?php else: ?>
                                    <span style="color: green;">✅ Clean</span>
                                <?php endif; ?>
                            </td>
                        </tr>
                        <?php
                    }
                    ?>
                </tbody>
            </table>
            
            <p>
                <button type="button" id="extract-btn" class="button button-primary">
                    Extract Selected Content
                </button>
            </p>
        </form>
    </div>
    
    <script>
    document.getElementById('select-all').addEventListener('change', function() {
        const checkboxes = document.querySelectorAll('input[name="post_ids[]"]');
        checkboxes.forEach(cb => cb.checked = this.checked);
    });
    
    document.getElementById('extract-btn').addEventListener('click', function() {
        const selected = Array.from(document.querySelectorAll('input[name="post_ids[]"]:checked'))
                            .map(cb => cb.value);
        
        if (selected.length === 0) {
            alert('Please select pages to extract.');
            return;
        }
        
        const results = document.getElementById('results');
        results.innerHTML = '<p>🔄 Processing...</p>';
        
        // Simple form submission
        const form = document.createElement('form');
        form.method = 'POST';
        form.innerHTML = `
            <input type="hidden" name="action" value="extract_now">
            <input type="hidden" name="post_ids" value="${selected.join(',')}">
            <?php echo '<input type="hidden" name="_wpnonce" value="' . wp_create_nonce('extract_now') . '">'; ?>
        `;
        document.body.appendChild(form);
        form.submit();
    });
    </script>
    <?php
}

// Handle extraction
add_action('admin_init', 'handle_extraction');

function handle_extraction() {
    if (isset($_POST['action']) && $_POST['action'] === 'extract_now') {
        check_admin_referer('extract_now');
        
        $post_ids = explode(',', $_POST['post_ids']);
        $processed = 0;
        
        foreach ($post_ids as $post_id) {
            $post = get_post($post_id);
            if (!$post) continue;
            
            $original = $post->post_content;
            $clean = extract_clean_content($original);
            
            if ($clean !== $original) {
                wp_update_post(array(
                    'ID' => $post_id,
                    'post_content' => $clean
                ));
                $processed++;
            }
        }
        
        wp_redirect(admin_url('tools.php?page=content-extractor&extracted=' . $processed));
        exit;
    }
}

function extract_clean_content($html) {
    $dom = new DOMDocument();
    libxml_use_internal_errors(true);
    $dom->loadHTML('<?xml encoding="UTF-8">' . $html);
    libxml_clear_errors();
    
    $xpath = new DOMXPath($dom);
    $clean = '';
    
    // Extract headings
    $headings = $xpath->query('//h1 | //h2 | //h3 | //h4 | //h5 | //h6');
    foreach ($headings as $h) {
        $text = trim($h->textContent);
        if (!empty($text)) {
            $tag = $h->tagName;
            $clean .= "<{$tag}>{$text}</{$tag}>\n\n";
        }
    }
    
    // Extract paragraphs
    $paras = $xpath->query('//p');
    foreach ($paras as $p) {
        $text = trim($p->textContent);
        if (!empty($text) && strlen($text) > 15) {
            $clean .= "<p>{$text}</p>\n\n";
        }
    }
    
    // Extract images
    $images = $xpath->query('//img');
    foreach ($images as $img) {
        $src = $img->getAttribute('src');
        $alt = $img->getAttribute('alt');
        if (!empty($src)) {
            $clean .= "<img src=\"{$src}\" alt=\"{$alt}\" />\n\n";
        }
    }
    
    return empty(trim($clean)) ? $html : $clean;
}

// Show success message
add_action('admin_notices', 'show_extraction_notice');

function show_extraction_notice() {
    if (isset($_GET['extracted'])) {
        $count = intval($_GET['extracted']);
        echo '<div class="notice notice-success"><p>✅ Successfully extracted content from ' . $count . ' pages!</p></div>';
    }
}
?> 