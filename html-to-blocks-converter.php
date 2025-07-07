<?php
/**
 * Plugin Name: HTML to Blocks Converter
 * Description: Convert Beaver Builder HTML to Gutenberg-friendly content
 * Version: 1.0
 * Author: Alexandria Dental Converter
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class HTMLToBlocksConverter {
    
    public function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('wp_ajax_convert_page_content', array($this, 'convert_page_content'));
    }
    
    public function add_admin_menu() {
        add_management_page(
            'HTML to Blocks Converter',
            'HTML to Blocks',
            'manage_options',
            'html-to-blocks',
            array($this, 'admin_page')
        );
    }
    
    public function admin_page() {
        ?>
        <div class="wrap">
            <h1>HTML to Blocks Converter</h1>
            <p>Convert Beaver Builder HTML content to Gutenberg-friendly blocks.</p>
            
            <div class="conversion-tool">
                <h2>Convert Page Content</h2>
                <label for="page-select">Select Page:</label>
                <select id="page-select">
                    <option value="">Select a page...</option>
                    <?php
                    $pages = get_pages();
                    foreach ($pages as $page) {
                        echo '<option value="' . $page->ID . '">' . esc_html($page->post_title) . '</option>';
                    }
                    ?>
                </select>
                
                <br><br>
                <button id="convert-btn" class="button button-primary">Convert to Blocks</button>
                <button id="preview-btn" class="button">Preview Changes</button>
                
                <div id="conversion-result" style="margin-top: 20px;"></div>
            </div>
        </div>
        
        <script>
        jQuery(document).ready(function($) {
            $('#convert-btn').click(function() {
                var pageId = $('#page-select').val();
                if (!pageId) {
                    alert('Please select a page first.');
                    return;
                }
                
                $.ajax({
                    url: ajaxurl,
                    type: 'POST',
                    data: {
                        action: 'convert_page_content',
                        page_id: pageId,
                        nonce: '<?php echo wp_create_nonce('convert_content'); ?>'
                    },
                    success: function(response) {
                        if (response.success) {
                            $('#conversion-result').html('<div class="notice notice-success"><p>Page converted successfully!</p></div>');
                        } else {
                            $('#conversion-result').html('<div class="notice notice-error"><p>Error: ' + response.data + '</p></div>');
                        }
                    }
                });
            });
            
            $('#preview-btn').click(function() {
                var pageId = $('#page-select').val();
                if (!pageId) {
                    alert('Please select a page first.');
                    return;
                }
                
                window.open('/wp-admin/post.php?post=' + pageId + '&action=edit', '_blank');
            });
        });
        </script>
        <?php
    }
    
    public function convert_page_content() {
        check_ajax_referer('convert_content', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_die('Unauthorized');
        }
        
        $page_id = intval($_POST['page_id']);
        $page = get_post($page_id);
        
        if (!$page) {
            wp_send_json_error('Page not found');
        }
        
        $content = $page->post_content;
        $converted_content = $this->convert_bb_to_blocks($content);
        
        // Update the page
        wp_update_post(array(
            'ID' => $page_id,
            'post_content' => $converted_content
        ));
        
        wp_send_json_success('Page converted successfully');
    }
    
    private function convert_bb_to_blocks($content) {
        // Remove unnecessary wrapper divs and convert to simpler structure
        
        // Convert FL photos to image blocks
        $content = preg_replace_callback(
            '/<div[^>]*fl-module-photo[^>]*>.*?<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>.*?<\/div>/s',
            function($matches) {
                $src = $matches[1];
                $alt = $matches[2];
                return "\n<!-- wp:image -->\n<figure class=\"wp-block-image\"><img src=\"{$src}\" alt=\"{$alt}\"/></figure>\n<!-- /wp:image -->\n";
            },
            $content
        );
        
        // Convert FL headings to heading blocks
        $content = preg_replace_callback(
            '/<div[^>]*fl-module-heading[^>]*>.*?<h([1-6])[^>]*>(.*?)<\/h[1-6]>.*?<\/div>/s',
            function($matches) {
                $level = $matches[1];
                $text = strip_tags($matches[2]);
                return "\n<!-- wp:heading {\"level\":{$level}} -->\n<h{$level}>{$text}</h{$level}>\n<!-- /wp:heading -->\n";
            },
            $content
        );
        
        // Convert FL rich text to paragraph blocks
        $content = preg_replace_callback(
            '/<div[^>]*fl-module-rich-text[^>]*>(.*?)<\/div>/s',
            function($matches) {
                $text_content = $matches[1];
                // Clean up the content
                $text_content = strip_tags($text_content, '<p><strong><em><a><ul><ol><li>');
                return "\n<!-- wp:html -->\n{$text_content}\n<!-- /wp:html -->\n";
            },
            $content
        );
        
        // Convert FL buttons to button blocks
        $content = preg_replace_callback(
            '/<div[^>]*fl-module-button[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>.*?<\/div>/s',
            function($matches) {
                $url = $matches[1];
                $text = strip_tags($matches[2]);
                return "\n<!-- wp:button -->\n<div class=\"wp-block-button\"><a class=\"wp-block-button__link\" href=\"{$url}\">{$text}</a></div>\n<!-- /wp:button -->\n";
            },
            $content
        );
        
        // Remove all FL wrapper divs and classes
        $content = preg_replace('/<div[^>]*fl-[^>]*>/', '', $content);
        $content = preg_replace('/<\/div>/', '', $content);
        
        // Clean up extra whitespace
        $content = preg_replace('/\s+/', ' ', $content);
        $content = trim($content);
        
        // If content doesn't start with blocks, wrap in HTML block
        if (!strpos($content, '<!-- wp:')) {
            $content = "<!-- wp:html -->\n{$content}\n<!-- /wp:html -->";
        }
        
        return $content;
    }
}

new HTMLToBlocksConverter(); 