<?php
/**
 * Plugin Name: Alexandria Content Display Fixer (Simple)
 * Description: Simple CSS fixes for imported Beaver Builder content
 * Version: 1.0
 * Author: Alexandria Dental Health
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Simple function to add CSS fixes
function alexandria_content_fixes() {
    $css = "
    /* Beaver Builder Content Fixes */
    .fl-builder-content {
        width: 100%;
        max-width: 100%;
    }
    
    .fl-row, .fl-row-content-wrap {
        width: 100%;
        margin: 0 auto;
        position: relative;
    }
    
    .fl-col-group {
        display: flex;
        flex-wrap: wrap;
        margin: 0;
    }
    
    .fl-col {
        padding: 10px;
        box-sizing: border-box;
        flex: 1;
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
    
    .fl-button, .uabb-button {
        display: inline-block;
        padding: 12px 24px;
        background-color: #a27295;
        color: white !important;
        text-decoration: none;
        border-radius: 4px;
        font-weight: 600;
        transition: background-color 0.3s ease;
        border: none;
    }
    
    .fl-button:hover, .uabb-button:hover {
        background-color: #72b7bc;
        color: white !important;
    }
    
    /* Text Module Fixes */
    .fl-rich-text p, .fl-module-rich-text p {
        margin-bottom: 1em;
        line-height: 1.6;
    }
    
    .fl-rich-text h1, .fl-rich-text h2, .fl-rich-text h3,
    .fl-module-heading h1, .fl-module-heading h2, .fl-module-heading h3 {
        color: #32192f;
        margin: 1.5em 0 1em 0;
    }
    
    /* Image Fixes */
    .fl-photo, .fl-module-photo {
        text-align: center;
        margin: 20px 0;
    }
    
    .fl-photo img, .fl-module-photo img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
    }
    
    .fl-photo-content img {
        max-width: 100%;
        height: auto;
    }
    
    /* Background Colors */
    .fl-col-bg-color {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Fix broken images */
    img[src*='wp-content/uploads'] {
        max-width: 100%;
        height: auto;
    }
    
    /* Layout responsiveness */
    @media (max-width: 768px) {
        .fl-col-group {
            flex-direction: column;
        }
        
        .fl-col {
            flex: 0 0 100%;
            max-width: 100%;
        }
    }
    
    /* Content area fixes */
    .entry-content, .post-content, .page-content {
        max-width: 100%;
        overflow-x: hidden;
    }
    
    /* Menu fixes */
    .uabb-creative-menu {
        width: 100%;
    }
    
    .uabb-creative-menu .menu {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        list-style: none;
        margin: 0;
        padding: 0;
    }
    
    .uabb-creative-menu .menu li {
        margin: 0 10px;
        padding: 5px 0;
    }
    
    .uabb-creative-menu .menu a {
        color: #32192f;
        text-decoration: none;
        padding: 8px 15px;
        display: block;
    }
    
    .uabb-creative-menu .menu a:hover {
        color: #a27295;
    }
    
    /* UABB button fixes */
    .uabb-creative-button-wrap a {
        background-color: #ffae00 !important;
        color: #0a0a0a !important;
        padding: 10px 20px;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        font-weight: bold;
    }
    
    .uabb-creative-button-wrap a:hover {
        background-color: #e69500 !important;
    }
    
    /* Info box fixes */
    .uabb-infobox {
        text-align: center;
        padding: 20px;
    }
    
    .uabb-infobox-text {
        color: #fff;
        font-weight: 300;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    ";
    
    wp_add_inline_style('wp-block-library', $css);
}

// Hook the CSS function to WordPress
add_action('wp_enqueue_scripts', 'alexandria_content_fixes');

// Also fix content on display
function alexandria_fix_content($content) {
    // Fix broken image paths
    $content = preg_replace('/src="\.\.\/([^"]+)"/', 'src="/$1"', $content);
    
    // Clean up excessive whitespace
    $content = preg_replace('/\s+/', ' ', $content);
    
    return $content;
}

add_filter('the_content', 'alexandria_fix_content', 20); 