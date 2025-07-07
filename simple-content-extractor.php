<?php
/**
 * Plugin Name: Simple Content Extractor
 * Description: Extract clean content from Beaver Builder HTML
 * Version: 1.0
 * Author: Alexandria Dental Health
 */

if (!defined('ABSPATH')) {
    exit;
}

class SimpleContentExtractor {
    
    public function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('wp_ajax_extract_content', array($this, 'extract_content'));
    }
    
    public function add_admin_menu() {
        if (function_exists('add_tools_page')) {
            add_tools_page(
                'Simple Content Extractor',
                'Extract Content',
                'manage_options',
                'simple-extractor',
                array($this, 'admin_page')
            );
        }
    }
    
    public function admin_page() {
        ?>
        <div class="wrap">
            <h1>Simple Content Extractor</h1>
            <p>Extract clean content from Beaver Builder pages and convert to simple, editable format.</p>
            
            <div id="extraction-results"></div>
            
            <form method="post" action="">
                <table class="wp-list-table widefat fixed striped">
                    <thead>
                        <tr>
                            <th width="50"><input type="checkbox" id="select-all"></th>
                            <th>Page/Post Title</th>
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
                            $has_bb_content = strpos($post->post_content, 'fl-builder-content') !== false;
                            ?>
                            <tr>
                                <td>
                                    <?php if ($has_bb_content): ?>
                                    <input type="checkbox" name="post_ids[]" value="<?php echo $post->ID; ?>">
                                    <?php endif; ?>
                                </td>
                                <td><?php echo esc_html($post->post_title); ?></td>
                                <td><?php echo $post->post_type; ?></td>
                                <td>
                                    <?php if ($has_bb_content): ?>
                                        <span style="color: orange">🔧 Needs Extraction</span>
                                    <?php else: ?>
                                        <span style="color: green">✅ Clean</span>
                                    <?php endif; ?>
                                </td>
                            </tr>
                            <?php
                        }
                        ?>
                    </tbody>
                </table>
                
                <p>
                    <button type="button" id="extract-selected" class="button button-primary">
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
        
        document.getElementById('extract-selected').addEventListener('click', function() {
            const selected = Array.from(document.querySelectorAll('input[name="post_ids[]"]:checked'))
                                .map(cb => cb.value);
            
            if (selected.length === 0) {
                alert('Please select at least one page/post to extract.');
                return;
            }
            
            const resultsDiv = document.getElementById('extraction-results');
            resultsDiv.innerHTML = '<p>🔄 Extracting content...</p>';
            
            fetch(ajaxurl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    action: 'extract_content',
                    post_ids: selected.join(','),
                    _wpnonce: '<?php echo wp_create_nonce('extract_content'); ?>'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultsDiv.innerHTML = '<div class="notice notice-success"><p>✅ ' + data.data.message + '</p></div>';
                    setTimeout(() => location.reload(), 2000);
                } else {
                    resultsDiv.innerHTML = '<div class="notice notice-error"><p>❌ ' + data.data.message + '</p></div>';
                }
            })
            .catch(error => {
                resultsDiv.innerHTML = '<div class="notice notice-error"><p>❌ Error: ' + error + '</p></div>';
            });
        });
        </script>
        <?php
    }
    
    public function extract_content() {
        check_ajax_referer('extract_content');
        
        if (!current_user_can('manage_options')) {
            wp_die('Unauthorized');
        }
        
        $post_ids = explode(',', $_POST['post_ids']);
        $processed = 0;
        
        foreach ($post_ids as $post_id) {
            $post = get_post($post_id);
            if (!$post) continue;
            
            $original_content = $post->post_content;
            $clean_content = $this->extract_clean_content($original_content);
            
            if ($clean_content !== $original_content) {
                wp_update_post(array(
                    'ID' => $post_id,
                    'post_content' => $clean_content
                ));
                $processed++;
            }
        }
        
        wp_send_json_success(array(
            'message' => "Successfully extracted content from {$processed} pages/posts."
        ));
    }
    
    private function extract_clean_content($html) {
        // Parse HTML
        $dom = new DOMDocument();
        libxml_use_internal_errors(true);
        $dom->loadHTML('<?xml encoding="UTF-8">' . $html);
        libxml_clear_errors();
        
        $xpath = new DOMXPath($dom);
        
        $clean_content = '';
        
        // Extract headings
        $headings = $xpath->query('//h1 | //h2 | //h3 | //h4 | //h5 | //h6');
        foreach ($headings as $heading) {
            $text = trim($heading->textContent);
            if (!empty($text)) {
                $tag = $heading->tagName;
                $clean_content .= "<{$tag}>{$text}</{$tag}>\n\n";
            }
        }
        
        // Extract paragraphs and text content
        $text_elements = $xpath->query('//p | //div[contains(@class, "fl-rich-text")]//p | //div[contains(@class, "fl-module-content")]//p');
        foreach ($text_elements as $element) {
            $text = trim($element->textContent);
            if (!empty($text) && strlen($text) > 20) { // Skip very short text
                $clean_content .= "<p>{$text}</p>\n\n";
            }
        }
        
        // Extract images
        $images = $xpath->query('//img');
        foreach ($images as $img) {
            $src = $img->getAttribute('src');
            $alt = $img->getAttribute('alt');
            if (!empty($src)) {
                $clean_content .= "<img src=\"{$src}\" alt=\"{$alt}\" />\n\n";
            }
        }
        
        // Extract links/buttons
        $links = $xpath->query('//a[contains(@class, "fl-button")]');
        foreach ($links as $link) {
            $href = $link->getAttribute('href');
            $text = trim($link->textContent);
            if (!empty($href) && !empty($text)) {
                $clean_content .= "<p><a href=\"{$href}\" class=\"button\">{$text}</a></p>\n\n";
            }
        }
        
        // If no content extracted, try to get any meaningful text
        if (empty(trim($clean_content))) {
            $all_text = $xpath->query('//text()[normalize-space()]');
            $text_content = '';
            foreach ($all_text as $text_node) {
                $text = trim($text_node->textContent);
                if (strlen($text) > 10) {
                    $text_content .= $text . ' ';
                }
            }
            
            if (!empty($text_content)) {
                $clean_content = "<p>" . trim($text_content) . "</p>";
            }
        }
        
        return empty(trim($clean_content)) ? $html : $clean_content;
    }
}

new SimpleContentExtractor();
?> 