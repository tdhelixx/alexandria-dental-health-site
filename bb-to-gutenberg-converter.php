<?php
/**
 * Plugin Name: Beaver Builder to Gutenberg Converter
 * Description: Convert Beaver Builder content to proper Gutenberg blocks
 * Version: 1.0
 * Author: Alexandria Dental Health
 */

if (!defined('ABSPATH')) {
    exit;
}

class BBToGutenbergConverter {
    
    public function __construct() {
        add_action('init', array($this, 'init'));
    }
    
    public function init() {
        if (is_admin()) {
            add_action('admin_menu', array($this, 'add_admin_menu'));
            add_action('wp_ajax_convert_bb_content', array($this, 'convert_bb_content'));
        }
    }
    
    public function add_admin_menu() {
        if (function_exists('add_tools_page')) {
            add_tools_page(
                'BB to Gutenberg Converter',
                'BB → Blocks',
                'manage_options',
                'bb-to-gutenberg',
                array($this, 'admin_page')
            );
        }
    }
    
    public function admin_page() {
        ?>
        <div class="wrap">
            <h1>🔄 Beaver Builder to Gutenberg Converter</h1>
            <p>Convert Beaver Builder content to editable Gutenberg blocks.</p>
            
            <div class="card" style="max-width: 800px;">
                <h2>Select Content to Convert</h2>
                
                <form id="conversion-form">
                    <table class="widefat">
                        <thead>
                            <tr>
                                <th width="50">Convert</th>
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
                                $row_class = $has_bb ? 'has-bb-content' : 'no-bb-content';
                                echo '<tr class="' . $row_class . '">';
                                echo '<td><input type="checkbox" name="post_ids[]" value="' . $post->ID . '"' . ($has_bb ? ' checked' : '') . '></td>';
                                echo '<td>' . esc_html($post->post_title) . '</td>';
                                echo '<td>' . $post->post_type . '</td>';
                                echo '<td>' . ($has_bb ? '🔧 Has BB Content' : '✅ Clean') . '</td>';
                                echo '</tr>';
                            }
                            ?>
                        </tbody>
                    </table>
                    
                    <p style="margin-top: 20px;">
                        <button type="button" id="convert-selected" class="button button-primary">
                            🔄 Convert Selected to Gutenberg Blocks
                        </button>
                        <button type="button" id="select-bb" class="button">Select BB Content Only</button>
                    </p>
                </form>
                
                <div id="conversion-results" style="margin-top: 20px;"></div>
            </div>
        </div>
        
        <style>
        .has-bb-content { background-color: #fff3cd; }
        .no-bb-content { background-color: #d1ecf1; }
        </style>
        
        <script>
        jQuery(document).ready(function($) {
            $('#select-bb').click(function() {
                $('input[name="post_ids[]"]').prop('checked', false);
                $('.has-bb-content input[name="post_ids[]"]').prop('checked', true);
            });
            
            $('#convert-selected').click(function() {
                var selectedIds = [];
                $('input[name="post_ids[]"]:checked').each(function() {
                    selectedIds.push($(this).val());
                });
                
                if (selectedIds.length === 0) {
                    alert('Please select at least one item to convert.');
                    return;
                }
                
                $('#conversion-results').html('<div class="notice notice-info"><p>🔄 Converting ' + selectedIds.length + ' items...</p></div>');
                
                $.ajax({
                    url: ajaxurl,
                    type: 'POST',
                    data: {
                        action: 'convert_bb_content',
                        post_ids: selectedIds,
                        nonce: '<?php echo wp_create_nonce('convert_bb_content'); ?>'
                    },
                    success: function(response) {
                        if (response.success) {
                            $('#conversion-results').html('<div class="notice notice-success"><p>✅ ' + response.data + '</p></div>');
                            // Refresh the page to show updated status
                            setTimeout(function() { location.reload(); }, 2000);
                        } else {
                            $('#conversion-results').html('<div class="notice notice-error"><p>❌ Error: ' + response.data + '</p></div>');
                        }
                    }
                });
            });
        });
        </script>
        <?php
    }
    
    public function convert_bb_content() {
        check_ajax_referer('convert_bb_content', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_send_json_error('Unauthorized');
        }
        
        $post_ids = $_POST['post_ids'];
        $converted_count = 0;
        
        foreach ($post_ids as $post_id) {
            $post = get_post($post_id);
            if (!$post) continue;
            
            $converted_content = $this->parse_bb_to_gutenberg($post->post_content);
            
            wp_update_post(array(
                'ID' => $post_id,
                'post_content' => $converted_content
            ));
            
            $converted_count++;
        }
        
        wp_send_json_success($converted_count . ' items converted successfully!');
    }
    
    private function parse_bb_to_gutenberg($content) {
        $blocks = array();
        
        // Parse the content using DOMDocument
        $dom = new DOMDocument();
        libxml_use_internal_errors(true);
        $dom->loadHTML('<?xml encoding="UTF-8">' . $content);
        libxml_clear_errors();
        
        $xpath = new DOMXPath($dom);
        
        // Find all FL modules
        $modules = $xpath->query('//div[contains(@class, "fl-module")]');
        
        foreach ($modules as $module) {
            $module_classes = $module->getAttribute('class');
            
            // Convert different module types
            if (strpos($module_classes, 'fl-module-heading') !== false) {
                $blocks[] = $this->convert_heading_module($module, $xpath);
            } elseif (strpos($module_classes, 'fl-module-rich-text') !== false) {
                $blocks[] = $this->convert_rich_text_module($module, $xpath);
            } elseif (strpos($module_classes, 'fl-module-photo') !== false) {
                $blocks[] = $this->convert_photo_module($module, $xpath);
            } elseif (strpos($module_classes, 'fl-module-button') !== false) {
                $blocks[] = $this->convert_button_module($module, $xpath);
            } elseif (strpos($module_classes, 'fl-module-post-grid') !== false) {
                $blocks[] = $this->convert_post_grid_module($module, $xpath);
            } else {
                // Fallback: convert to HTML block
                $blocks[] = $this->convert_to_html_block($module);
            }
        }
        
        // If no modules found, try to parse as simple content
        if (empty($blocks)) {
            return $this->parse_simple_content($content);
        }
        
        return implode("\n\n", array_filter($blocks));
    }
    
    private function convert_heading_module($module, $xpath) {
        $heading = $xpath->query('.//h1 | .//h2 | .//h3 | .//h4 | .//h5 | .//h6', $module)->item(0);
        if (!$heading) return '';
        
        $level = intval(substr($heading->tagName, 1));
        $text = trim($heading->textContent);
        
        return "<!-- wp:heading {\"level\":{$level}} -->\n<h{$level}>{$text}</h{$level}>\n<!-- /wp:heading -->";
    }
    
    private function convert_rich_text_module($module, $xpath) {
        $content_div = $xpath->query('.//div[contains(@class, "fl-rich-text")]', $module)->item(0);
        if (!$content_div) return '';
        
        $html = $this->get_inner_html($content_div);
        $html = $this->clean_html($html);
        
        // Try to split into paragraphs
        $paragraphs = explode('</p>', $html);
        $blocks = array();
        
        foreach ($paragraphs as $p) {
            $p = trim(str_replace('<p>', '', $p));
            if (!empty($p)) {
                $blocks[] = "<!-- wp:paragraph -->\n<p>{$p}</p>\n<!-- /wp:paragraph -->";
            }
        }
        
        return implode("\n\n", $blocks);
    }
    
    private function convert_photo_module($module, $xpath) {
        $img = $xpath->query('.//img', $module)->item(0);
        if (!$img) return '';
        
        $src = $img->getAttribute('src');
        $alt = $img->getAttribute('alt');
        $title = $img->getAttribute('title');
        
        // Fix relative paths
        $src = preg_replace('/^\.\.\//', '/', $src);
        
        return "<!-- wp:image -->\n<figure class=\"wp-block-image\"><img src=\"{$src}\" alt=\"{$alt}\" title=\"{$title}\"/></figure>\n<!-- /wp:image -->";
    }
    
    private function convert_button_module($module, $xpath) {
        $link = $xpath->query('.//a', $module)->item(0);
        if (!$link) return '';
        
        $href = $link->getAttribute('href');
        $text = trim($link->textContent);
        
        return "<!-- wp:button -->\n<div class=\"wp-block-button\"><a class=\"wp-block-button__link\" href=\"{$href}\">{$text}</a></div>\n<!-- /wp:button -->";
    }
    
    private function convert_post_grid_module($module, $xpath) {
        // Convert post grid to a latest posts block
        return "<!-- wp:latest-posts {\"displayPostContent\":true,\"excerptLength\":40,\"displayPostDate\":true,\"postLayout\":\"grid\",\"columns\":3,\"displayFeaturedImage\":true} /-->";
    }
    
    private function convert_to_html_block($module) {
        $html = $this->get_outer_html($module);
        $html = $this->clean_html($html);
        
        return "<!-- wp:html -->\n{$html}\n<!-- /wp:html -->";
    }
    
    private function parse_simple_content($content) {
        // Fallback for content that doesn't have clear BB structure
        $content = $this->clean_html($content);
        
        // Wrap in HTML block
        return "<!-- wp:html -->\n{$content}\n<!-- /wp:html -->";
    }
    
    private function get_inner_html($element) {
        $innerHTML = '';
        $children = $element->childNodes;
        foreach ($children as $child) {
            $innerHTML .= $element->ownerDocument->saveHTML($child);
        }
        return $innerHTML;
    }
    
    private function get_outer_html($element) {
        return $element->ownerDocument->saveHTML($element);
    }
    
    private function clean_html($html) {
        // Remove FL-specific classes and IDs
        $html = preg_replace('/class="[^"]*fl-[^"]*"/', '', $html);
        $html = preg_replace('/id="[^"]*fl-[^"]*"/', '', $html);
        $html = preg_replace('/data-[^=]*="[^"]*"/', '', $html);
        
        // Clean up multiple spaces
        $html = preg_replace('/\s+/', ' ', $html);
        $html = preg_replace('/>\s+</', '><', $html);
        
        return trim($html);
    }
}

new BBToGutenbergConverter(); 