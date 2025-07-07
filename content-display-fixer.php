<?php
/**
 * Plugin Name: Alexandria Content Display Fixer
 * Plugin URI: https://alexandriadental.com
 * Description: Fixes content display issues for imported Beaver Builder content
 * Version: 1.0.0
 * Author: Alexandria Dental Health
 * License: GPL v2 or later
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class Alexandria_Content_Fixer {
    
    public function __construct() {
        add_action('init', array($this, 'init'));
    }
    
    public function init() {
        add_action('wp_enqueue_scripts', array($this, 'enqueue_content_fixes'));
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_filter('the_content', array($this, 'fix_content_structure'), 20);
        add_action('admin_init', array($this, 'handle_content_fix'));
    }
    
    /**
     * Add admin menu page
     */
    public function add_admin_menu() {
        add_tools_page(
            'Content Display Fixer',
            'Fix Content Display',
            'manage_options',
            'alexandria-content-fixer',
            array($this, 'admin_page')
        );
    }
    
    /**
     * Enqueue CSS fixes for Beaver Builder content
     */
    public function enqueue_content_fixes() {
        wp_add_inline_style('alexandria-dental-style', $this->get_content_css());
    }
    
    /**
     * Get CSS to fix Beaver Builder content display
     */
    private function get_content_css() {
        return "
        /* Beaver Builder Content Fixes */
        .fl-builder-content {
            width: 100%;
        }
        
        .fl-row, .fl-row-content-wrap {
            width: 100%;
            margin: 0 auto;
            position: relative;
        }
        
        .fl-col-group {
            display: flex;
            flex-wrap: wrap;
            margin: 0 -15px;
        }
        
        .fl-col {
            padding: 0 15px;
            box-sizing: border-box;
        }
        
        .fl-col-small {
            flex: 0 0 50%;
            max-width: 50%;
        }
        
        .fl-col-medium {
            flex: 0 0 100%;
            max-width: 100%;
        }
        
        .fl-col-large {
            flex: 0 0 100%;
            max-width: 100%;
        }
        
        .fl-col-content {
            height: 100%;
        }
        
        .fl-module {
            margin-bottom: 20px;
        }
        
        .fl-module-content {
            position: relative;
        }
        
        /* Button Fixes */
        .fl-button-wrap {
            text-align: center;
            margin: 10px 0;
        }
        
        .fl-button {
            display: inline-block;
            padding: 12px 24px;
            background-color: #a27295;
            color: white !important;
            text-decoration: none;
            border-radius: 4px;
            font-weight: 600;
            transition: background-color 0.3s ease;
        }
        
        .fl-button:hover {
            background-color: #72b7bc;
            color: white !important;
        }
        
        .fl-button-width-full .fl-button {
            width: 100%;
            text-align: center;
        }
        
        /* Text Module Fixes */
        .fl-rich-text p {
            margin-bottom: 1em;
            line-height: 1.6;
        }
        
        .fl-rich-text h1, .fl-rich-text h2, .fl-rich-text h3 {
            color: #32192f;
            margin: 1.5em 0 1em 0;
        }
        
        /* Image Fixes */
        .fl-photo {
            text-align: center;
            margin: 20px 0;
        }
        
        .fl-photo img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }
        
        /* Background Colors */
        .fl-col-bg-color {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .fl-col-group {
                flex-direction: column;
            }
            
            .fl-col-small {
                flex: 0 0 100%;
                max-width: 100%;
            }
        }
        
        /* Fix for missing images - show placeholder */
        img[src*='wp-content/uploads'] {
            background-color: #f0f0f0;
            border: 2px dashed #ccc;
            min-height: 200px;
            display: block;
            position: relative;
        }
        
        img[src*='wp-content/uploads']:after {
            content: 'Image not found - Copy images from scraped site';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #666;
            font-size: 14px;
            text-align: center;
        }
        
        /* Content wrapper fixes */
        .post-content, .page-content, .entry-content {
            max-width: 100%;
            overflow-x: hidden;
        }
        
        /* Sidebar layout fixes */
        .content-area {
            width: 100%;
        }
        
        .site-main {
            margin: 0;
            padding: 20px;
        }
        ";
    }
    
    /**
     * Fix content structure on display
     */
    public function fix_content_structure($content) {
        // Fix broken image paths
        $content = preg_replace('/src="\.\.\/([^"]+)"/', 'src="/' . '$1"', $content);
        
        // Add responsive classes
        $content = str_replace('fl-col-group', 'fl-col-group responsive-row', $content);
        
        // Fix button styling
        $content = preg_replace('/<a([^>]*class="[^"]*fl-button[^"]*"[^>]*)>/', '<a$1>', $content);
        
        // Clean up excessive whitespace
        $content = preg_replace('/\s+/', ' ', $content);
        
        return $content;
    }
    
    /**
     * Handle bulk content fixing
     */
    public function handle_content_fix() {
        if (!isset($_POST['fix_all_content']) || !isset($_POST['_wpnonce'])) {
            return;
        }
        
        if (!wp_verify_nonce($_POST['_wpnonce'], 'fix_content')) {
            wp_die('Security check failed');
        }
        
        if (!current_user_can('manage_options')) {
            wp_die('You do not have sufficient permissions');
        }
        
        $this->fix_all_content();
        
        wp_redirect(add_query_arg('content_fixed', '1', admin_url('tools.php?page=alexandria-content-fixer')));
        exit;
    }
    
    /**
     * Fix all imported content
     */
    private function fix_all_content() {
        $pages = get_posts(array(
            'post_type' => array('page', 'post'),
            'posts_per_page' => -1,
            'post_status' => 'publish'
        ));
        
        foreach ($pages as $page) {
            $content = $page->post_content;
            
            // Fix image paths
            $content = preg_replace('/src="\.\.\/wp-content\/uploads\/([^"]+)"/', 'src="/wp-content/uploads/$1"', $content);
            
            // Simplify Beaver Builder structure for better compatibility
            $content = preg_replace('/<div[^>]*fl-node-[^>]*>/', '<div class="content-section">', $content);
            
            // Clean up data attributes
            $content = preg_replace('/data-node="[^"]*"/', '', $content);
            
            // Update the post
            wp_update_post(array(
                'ID' => $page->ID,
                'post_content' => $content
            ));
        }
    }
    
    /**
     * Admin page content
     */
    public function admin_page() {
        ?>
        <div class="wrap">
            <h1>🔧 Alexandria Content Display Fixer</h1>
            
            <?php if (isset($_GET['content_fixed'])): ?>
                <div class="notice notice-success">
                    <p><strong>✅ Success!</strong> Content has been fixed for better display!</p>
                </div>
            <?php endif; ?>
            
            <div class="card" style="max-width: 800px;">
                <h2>Fix Content Display Issues</h2>
                <p>This tool fixes common issues with imported Beaver Builder content:</p>
                
                <h3>🎯 What This Fixes:</h3>
                <ul>
                    <li><strong>✅ Layout Issues:</strong> Adds CSS for proper column display</li>
                    <li><strong>✅ Button Styling:</strong> Restores button appearance</li>
                    <li><strong>✅ Image Paths:</strong> Fixes broken image references</li>
                    <li><strong>✅ Mobile Responsive:</strong> Ensures mobile compatibility</li>
                    <li><strong>✅ Content Structure:</strong> Cleans up unnecessary markup</li>
                </ul>
                
                <div style="background: #e7f3ff; padding: 15px; border-left: 4px solid #0073aa; margin: 20px 0;">
                    <h4>📋 Manual Steps Still Needed:</h4>
                    <ol>
                        <li><strong>Copy Images:</strong> Copy files from <code>wp-content/uploads/</code> in scraped site to WordPress</li>
                        <li><strong>Check Pages:</strong> Review pages after running this fixer</li>
                        <li><strong>Adjust Styling:</strong> Fine-tune any remaining display issues</li>
                    </ol>
                </div>
                
                <h3>🚀 Run Content Fixer</h3>
                <p>This will update all pages and posts to fix display issues:</p>
                
                <form method="post" style="margin-top: 30px;">
                    <?php wp_nonce_field('fix_content'); ?>
                    <p>
                        <button type="submit" name="fix_all_content" class="button button-primary button-hero" 
                                onclick="return confirm('This will update all pages and posts. Continue?')">
                            🔧 Fix All Content
                        </button>
                    </p>
                </form>
            </div>
            
            <div class="card" style="max-width: 800px; margin-top: 20px;">
                <h3>📁 Image Copy Instructions</h3>
                <p>To restore images, copy these folders from your scraped site to WordPress:</p>
                
                <h4>From Scraped Site:</h4>
                <code>wp-content/uploads/</code>
                
                <h4>To WordPress Site:</h4>
                <code>/wp-content/uploads/</code>
                
                <p><strong>Note:</strong> Only copy the year folders (2017, 2018, etc.) and skip bb-plugin/bb-theme folders.</p>
            </div>
        </div>
        
        <style>
        .card h3 { margin-top: 0; color: #23282d; }
        .card ul, .card ol { margin: 10px 0; }
        .card li { margin: 5px 0; }
        .button-hero { font-size: 16px !important; padding: 10px 20px !important; height: auto !important; }
        </style>
        <?php
    }
}

// Initialize the plugin
new Alexandria_Content_Fixer();
?> 