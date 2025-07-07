<?php
/**
 * Astra Child Theme - Alexandria Dental Health Functions
 *
 * @package Astra Child - Alexandria Dental Health
 */

// Exit if accessed directly
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Define theme constants
 */
define( 'ASTRA_CHILD_VERSION', '1.0.0' );
define( 'ASTRA_CHILD_URI', get_stylesheet_directory_uri() );
define( 'ASTRA_CHILD_DIR', get_stylesheet_directory() );

/**
 * Enqueue parent and child theme styles
 */
function astra_child_enqueue_styles() {
    // Enqueue parent theme style
    wp_enqueue_style( 
        'astra-parent-style', 
        get_template_directory_uri() . '/style.css',
        array(),
        wp_get_theme()->get('Version')
    );
    
    // Enqueue child theme style
    wp_enqueue_style( 
        'astra-child-style',
        get_stylesheet_directory_uri() . '/style.css',
        array( 'astra-parent-style' ),
        ASTRA_CHILD_VERSION
    );
    
    // Enqueue Google Fonts with more weights and styles
    wp_enqueue_style(
        'astra-child-fonts',
        'https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,600&family=Nunito:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=Inter:wght@300;400;500;600;700&family=Oxygen:wght@300;400;700&display=swap',
        array(),
        ASTRA_CHILD_VERSION
    );
}
add_action( 'wp_enqueue_scripts', 'astra_child_enqueue_styles' );

/**
 * Theme setup
 */
function astra_child_setup() {
    // Add theme support for post thumbnails
    add_theme_support( 'post-thumbnails' );
    
    // Add custom image sizes
    add_image_size( 'dental-hero', 1200, 400, true );
    add_image_size( 'dental-thumbnail', 400, 300, true );
    
    // Register navigation menus
    register_nav_menus( array(
        'primary' => __( 'Primary Menu', 'astra-child-alexandria-dental' ),
        'footer'  => __( 'Footer Menu', 'astra-child-alexandria-dental' ),
    ) );
}
add_action( 'after_setup_theme', 'astra_child_setup' );

/**
 * Register sidebar areas
 */
function astra_child_widgets_init() {
    register_sidebar( array(
        'name'          => __( 'Dental Sidebar', 'astra-child-alexandria-dental' ),
        'id'            => 'dental-sidebar',
        'description'   => __( 'Sidebar for dental practice information', 'astra-child-alexandria-dental' ),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ) );
}
add_action( 'widgets_init', 'astra_child_widgets_init' );

/**
 * Default menu fallback
 */
function astra_child_default_menu() {
    echo '<nav class="main-navigation">';
    echo '<ul class="main-header-menu">';
    echo '<li><a href="' . esc_url( home_url( '/' ) ) . '">Home</a></li>';
    echo '<li><a href="' . esc_url( home_url( '/about' ) ) . '">About</a></li>';
    echo '<li><a href="' . esc_url( home_url( '/services' ) ) . '">Services</a></li>';
    echo '<li><a href="' . esc_url( home_url( '/contact' ) ) . '">Contact</a></li>';
    echo '</ul>';
    echo '</nav>';
}

/**
 * Custom sidebar content
 * Now integrates with plugin settings
 */
function astra_child_dental_sidebar() {
    // Get settings from plugin if available
    $phone = function_exists('adh_get_phone') ? adh_get_phone() : '(703) 212-9622';
    $address = function_exists('adh_get_address') ? adh_get_address() : "2847 Duke St\nAlexandria VA 22314";
    $hours = function_exists('adh_get_office_hours') ? adh_get_office_hours() : "Monday: 8:00 AM - 5:00 PM\nTuesday: 8:00 AM - 5:00 PM\nWednesday: 8:00 AM - 5:00 PM\nThursday: 8:00 AM - 5:00 PM\nFriday: 8:00 AM - 3:00 PM\nSaturday: Closed\nSunday: Closed";
    $maps_embed = function_exists('adh_get_google_maps') ? adh_get_google_maps() : '';
    $special_url = function_exists('adh_get_special_offers_url') ? adh_get_special_offers_url() : '/special';
    ?>
    <aside class="dental-sidebar">
        <!-- Special Offer Button -->
        <div class="dental-special-offer">
            <a href="<?php echo esc_url( $special_url ); ?>" class="dental-special-link">
                <span class="dental-special-top">VIEW OUR</span>
                <span class="dental-special-main">SPECIAL OFFERS</span>
                <span class="dental-special-cta">CLICK HERE ></span>
            </a>
        </div>
        
        <!-- Contact Information -->
        <div class="dental-sidebar-card">
            <h3>Alexandria Dental Health & Smile Studio</h3>
            <p><?php echo wp_kses_post( nl2br( $address ) ); ?><br>
            <strong><?php echo esc_html( $phone ); ?></strong></p>
        </div>
        
        <!-- Office Hours -->
        <div class="dental-sidebar-card">
            <h3>Office Hours</h3>
            <p><?php echo wp_kses_post( nl2br( $hours ) ); ?></p>
        </div>
        
        <!-- Google Maps -->
        <?php if ( !empty( $maps_embed ) ) : ?>
        <div class="dental-sidebar-card dental-map">
            <h3>Our Location</h3>
            <?php echo wp_kses_post( $maps_embed ); ?>
        </div>
        <?php else : ?>
        <div class="dental-sidebar-card dental-map">
            <h3>Our Location</h3>
            <iframe 
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3107.2698765432109!2d-77.08123456789!3d38.80987654321!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89b7b3f8a1234567%3A0x9876543210abcdef!2s2847%20Duke%20St%2C%20Alexandria%2C%20VA%2022314%2C%20USA!5e0!3m2!1sen!2sus!4v1640995200000!5m2!1sen!2sus"
                width="100%" 
                height="250" 
                style="border:0;border-radius:6px;" 
                allowfullscreen="" 
                loading="lazy" 
                referrerpolicy="no-referrer-when-downgrade"
                title="Alexandria Dental Health & Smile Studio Location">
            </iframe>
        </div>
        <?php endif; ?>
        
        <?php if ( is_active_sidebar( 'dental-sidebar' ) ) : ?>
            <?php dynamic_sidebar( 'dental-sidebar' ); ?>
        <?php endif; ?>
    </aside>
    <?php
}

/**
 * Customize Astra theme options
 */
function astra_child_customize_astra() {
    // Work with Astra's header builder completely
    // Don't add custom elements - let user build in Astra
    
    // Modify sidebar
    add_filter( 'astra_get_sidebar', 'astra_child_get_sidebar' );
    
    // Add minimal custom styles that don't override Astra's color controls
    add_action( 'wp_head', 'astra_child_minimal_header_styles' );
}
add_action( 'init', 'astra_child_customize_astra' );

/**
 * Minimal custom styles that work with Astra's controls
 */
function astra_child_minimal_header_styles() {
    ?>
    <style>
    /* Only add typography and layout styles - let Astra handle colors */
    .main-header-menu a,
    .ast-below-header-menu a,
    .ast-above-header-menu a {
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 0.8px;
        font-family: "Raleway", sans-serif;
        font-weight: 600;
        /* Removed color overrides - let Astra handle colors */
    }
    
    /* Style custom HTML elements without color overrides */
    .dental-phone-link {
        font-size: 1.3em;
        font-weight: bold;
        font-family: "Raleway", sans-serif;
        text-decoration: none;
    }
    
    .dental-action-buttons {
        display: flex;
        gap: 15px;
        align-items: center;
    }
    
    .dental-action-buttons .dental-btn,
    .ast-header-html .dental-btn {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-width: 180px !important;
        width: 180px !important;
        height: 45px !important;
        border-radius: 25px !important;
        text-transform: uppercase !important;
        font-weight: bold !important;
        font-size: 13px !important;
        text-decoration: none !important;
        font-family: "Raleway", sans-serif !important;
        letter-spacing: 0.5px !important;
        padding: 0 25px !important;
        transition: all 0.3s ease !important;
        box-sizing: border-box !important;
    }
    
    .dental-btn-special {
        background: #ffae00;
        color: #000;
    }
    
    .dental-btn-schedule {
        background: #a27295;
        color: white;
    }
    
    .dental-btn:hover {
        transform: translateY(-2px);
    }
    
    /* Tagline styling for Above Header */
    .dental-tagline {
        font-family: "Raleway", sans-serif;
        font-weight: 600;
        font-size: 16px;
        text-align: center;
    }
    
    .love-text {
        font-weight: 800;
        color: #ffae00;
    }
    
    .top-cta-btn {
        background: #ffae00;
        color: #000;
        padding: 8px 16px;
        border-radius: 20px;
        text-transform: uppercase;
        font-weight: bold;
        font-size: 11px;
        text-decoration: none;
        font-family: "Raleway", sans-serif;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    
    .top-cta-btn:hover {
        background: #e69900;
        transform: translateY(-1px);
    }
    </style>
    <?php
}

/**
 * Custom sidebar filter
 */
function astra_child_get_sidebar( $sidebar ) {
    if ( is_page() || is_single() ) {
        ob_start();
        astra_child_dental_sidebar();
        return ob_get_clean();
    }
    return $sidebar;
}

/**
 * Add custom body classes
 */
function astra_child_body_classes( $classes ) {
    $classes[] = 'dental-theme';
    
    if ( is_page() ) {
        $classes[] = 'dental-page';
    }
    
    if ( is_single() ) {
        $classes[] = 'dental-post';
    }
    
    return $classes;
}
add_filter( 'body_class', 'astra_child_body_classes' );

/**
 * Customize excerpt length
 */
function astra_child_excerpt_length( $length ) {
    return 25;
}
add_filter( 'excerpt_length', 'astra_child_excerpt_length' );

/**
 * Add custom favicon if not set
 */
function astra_child_favicon() {
    if ( ! has_site_icon() ) {
        echo '<link rel="icon" href="' . ASTRA_CHILD_URI . '/assets/favicon.png" sizes="32x32">';
        echo '<link rel="apple-touch-icon" href="' . ASTRA_CHILD_URI . '/assets/favicon.png">';
    }
}
add_action( 'wp_head', 'astra_child_favicon' );

/**
 * Customize footer
 */
function astra_child_footer() {
    ?>
    <div class="footer-content">
        <div class="site-info">
            &copy; <?php echo date( 'Y' ); ?> <?php bloginfo( 'name' ); ?>. All rights reserved.
        </div>
        <nav class="footer-navigation">
            <?php
            wp_nav_menu( array(
                'theme_location' => 'footer',
                'menu_class'     => 'footer-menu',
                'container'      => false,
                'fallback_cb'    => 'astra_child_footer_menu',
            ) );
            ?>
        </nav>
    </div>
    <?php
}

/**
 * Footer menu fallback
 */
function astra_child_footer_menu() {
    echo '<ul class="footer-menu">';
    echo '<li><a href="' . esc_url( home_url( '/about' ) ) . '">About</a></li>';
    echo '<li><a href="' . esc_url( home_url( '/services' ) ) . '">Services</a></li>';
    echo '<li><a href="' . esc_url( home_url( '/contact' ) ) . '">Contact</a></li>';
    echo '<li><a href="' . esc_url( home_url( '/privacy-policy' ) ) . '">Privacy Policy</a></li>';
    echo '</ul>';
}

/**
 * Remove Astra default footer and add custom
 */
function astra_child_customize_footer() {
    remove_action( 'astra_footer_content', 'astra_footer_small_footer_template', 5 );
    add_action( 'astra_footer_content', 'astra_child_footer', 5 );
}
add_action( 'init', 'astra_child_customize_footer' );

/**
 * Security enhancements
 */
function astra_child_security() {
    // Remove WordPress version from head
    remove_action( 'wp_head', 'wp_generator' );
    
    // Remove RSD link
    remove_action( 'wp_head', 'rsd_link' );
    
    // Remove Windows Live Writer link
    remove_action( 'wp_head', 'wlwmanifest_link' );
}
add_action( 'init', 'astra_child_security' );

/**
 * Optimize performance
 */
function astra_child_optimize() {
    // Remove emoji scripts
    remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
    remove_action( 'wp_print_styles', 'print_emoji_styles' );
    
    // Disable embeds
    remove_action( 'wp_head', 'wp_oembed_add_discovery_links' );
    remove_action( 'wp_head', 'wp_oembed_add_host_js' );
}
add_action( 'init', 'astra_child_optimize' );

/**
 * Check if Alexandria Dental Helper plugin is active
 */
function astra_child_check_plugin_dependency() {
    if ( ! function_exists( 'adh_get_phone' ) ) {
        add_action( 'admin_notices', 'astra_child_plugin_notice' );
    }
}
add_action( 'admin_init', 'astra_child_check_plugin_dependency' );

/**
 * Admin notice for missing plugin
 */
function astra_child_plugin_notice() {
    ?>
    <div class="notice notice-warning">
        <p><strong>Astra Child - Alexandria Dental:</strong> This theme works best with the Alexandria Dental Helper plugin. Please install and activate it for full functionality.</p>
    </div>
    <?php
}

/**
 * Add custom page template for dental pages
 */
function astra_child_page_template( $template ) {
    if ( is_page() && file_exists( ASTRA_CHILD_DIR . '/page-dental.php' ) ) {
        return ASTRA_CHILD_DIR . '/page-dental.php';
    }
    return $template;
}
add_filter( 'page_template', 'astra_child_page_template' );

/**
 * Add custom color palette to Astra (Working version)
 */
function astra_child_custom_color_palette() {
    // Add Gutenberg editor color palette
    add_theme_support( 'editor-color-palette', array(
        array(
            'name'  => __( 'Primary Purple', 'astra-child-alexandria-dental' ),
            'slug'  => 'primary-purple',
            'color' => '#32192f',
        ),
        array(
            'name'  => __( 'Secondary Purple', 'astra-child-alexandria-dental' ),
            'slug'  => 'secondary-purple',
            'color' => '#a27295',
        ),
        array(
            'name'  => __( 'Accent Orange', 'astra-child-alexandria-dental' ),
            'slug'  => 'accent-orange',
            'color' => '#ffae00',
        ),
        array(
            'name'  => __( 'Hover Teal', 'astra-child-alexandria-dental' ),
            'slug'  => 'hover-teal',
            'color' => '#72b7bc',
        ),
        array(
            'name'  => __( 'Text Gray', 'astra-child-alexandria-dental' ),
            'slug'  => 'text-gray',
            'color' => '#424242',
        ),
        array(
            'name'  => __( 'Light Background', 'astra-child-alexandria-dental' ),
            'slug'  => 'light-bg',
            'color' => '#f8f9fa',
        ),
        array(
            'name'  => __( 'White', 'astra-child-alexandria-dental' ),
            'slug'  => 'white',
            'color' => '#ffffff',
        ),
        array(
            'name'  => __( 'Black', 'astra-child-alexandria-dental' ),
            'slug'  => 'black',
            'color' => '#000000',
        ),
    ) );
}
add_action( 'after_setup_theme', 'astra_child_custom_color_palette' );

/**
 * Add Alexandria Dental palette to Astra's Global Palettes
 */
function astra_child_add_dental_palette( $color_palettes ) {
    // Add our custom palette to the existing ones
    $color_palettes['alexandria-dental'] = array(
        'name'   => __( 'Alexandria Dental', 'astra-child-alexandria-dental' ),
        'colors' => array(
            '#32192f', // Primary Purple
            '#a27295', // Secondary Purple  
            '#ffae00', // Accent Orange
            '#72b7bc', // Hover Teal
            '#424242', // Text Gray
            '#f8f9fa', // Light Background
            '#ffffff', // White
            '#000000', // Black
        ),
    );
    
    return $color_palettes;
}
add_filter( 'astra_color_palettes', 'astra_child_add_dental_palette' );

/**
 * Alternative method - Add to Astra's default palettes
 */
function astra_child_modify_default_palettes( $palettes ) {
    // Add Alexandria Dental as the first palette
    $dental_palette = array(
        'alexandria-dental' => array(
            'name'   => 'Alexandria Dental',
            'colors' => array( '#32192f', '#a27295', '#ffae00', '#72b7bc', '#424242', '#f8f9fa', '#ffffff', '#000000' ),
        ),
    );
    
    return array_merge( $dental_palette, $palettes );
}
add_filter( 'astra_default_color_palettes', 'astra_child_modify_default_palettes' );

/**
 * Add custom fonts to Astra's font list (Working version)
 */
function astra_child_add_custom_fonts_to_astra( $fonts ) {
    // Temporarily disabled to avoid array conversion errors
    return $fonts;
}
// Disable this filter to prevent errors
// add_filter( 'astra_system_fonts', 'astra_child_add_custom_fonts_to_astra' );

/**
 * Register Google Fonts with Astra
 */
function astra_child_register_google_fonts( $fonts ) {
    // Temporarily disabled to avoid array conversion errors
    return $fonts;
}
// Disable this filter to prevent errors
// add_filter( 'astra_google_fonts', 'astra_child_register_google_fonts' );

/**
 * Set default fonts for Astra (Proper method)
 */
function astra_child_set_default_fonts() {
    // Temporarily disabled to avoid array conversion errors
    // Fonts are loaded via CSS and work through the stylesheet
}
// Disable this action to prevent errors
// add_action( 'init', 'astra_child_set_default_fonts' );

/**
 * Set default typography for dental practice
 */
function astra_child_default_typography() {
    // Fonts are loaded via CSS @import and available in customizer
    // No need to set defaults programmatically
}
add_action( 'after_setup_theme', 'astra_child_default_typography' ); 