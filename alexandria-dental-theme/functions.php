<?php
/**
 * Alexandria Dental Health Theme functions and definitions
 *
 * @link https://developer.wordpress.org/themes/basics/theme-functions/
 *
 * @package Alexandria_Dental_Health
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit; // Exit if accessed directly.
}

/**
 * Sets up theme defaults and registers support for various WordPress features.
 */
function alexandria_dental_setup() {
    /*
     * Make theme available for translation.
     */
    load_theme_textdomain( 'alexandria-dental', get_template_directory() . '/languages' );

    // Add default posts and comments RSS feed links to head.
    add_theme_support( 'automatic-feed-links' );

    /*
     * Let WordPress manage the document title.
     */
    add_theme_support( 'title-tag' );

    /*
     * Enable support for Post Thumbnails on posts and pages.
     */
    add_theme_support( 'post-thumbnails' );
    
    // Set default thumbnail size
    set_post_thumbnail_size( 350, 200, true );
    
    // Add additional image sizes
    add_image_size( 'hero-image', 1200, 600, true );
    add_image_size( 'service-card', 300, 200, true );

    // This theme uses wp_nav_menu() in multiple locations.
    register_nav_menus(
        array(
            'primary'        => esc_html__( 'Primary Navigation', 'alexandria-dental' ),
            'footer-services' => esc_html__( 'Footer Services', 'alexandria-dental' ),
            'footer-patient'  => esc_html__( 'Footer Patient Info', 'alexandria-dental' ),
            'footer-legal'    => esc_html__( 'Footer Legal', 'alexandria-dental' ),
        )
    );

    /*
     * Switch default core markup for search form, comment form, and comments
     * to output valid HTML5.
     */
    add_theme_support(
        'html5',
        array(
            'search-form',
            'comment-form',
            'comment-list',
            'gallery',
            'caption',
            'style',
            'script',
        )
    );

    // Add theme support for selective refresh for widgets.
    add_theme_support( 'customize-selective-refresh-widgets' );

    /**
     * Add support for core custom logo.
     */
    add_theme_support(
        'custom-logo',
        array(
            'height'      => 80,
            'width'       => 250,
            'flex-width'  => true,
            'flex-height' => true,
        )
    );
    
    // Add support for editor styles
    add_theme_support( 'editor-styles' );
    
    // Add support for responsive embeds
    add_theme_support( 'responsive-embeds' );
    
    // Add support for custom background
    add_theme_support( 'custom-background', array(
        'default-color' => 'ffffff',
    ) );
}
add_action( 'after_setup_theme', 'alexandria_dental_setup' );

/**
 * Set the content width in pixels, based on the theme's design and stylesheet.
 */
function alexandria_dental_content_width() {
    $GLOBALS['content_width'] = apply_filters( 'alexandria_dental_content_width', 1100 );
}
add_action( 'after_setup_theme', 'alexandria_dental_content_width', 0 );

/**
 * Enqueue scripts and styles.
 */
function alexandria_dental_scripts() {
    // Theme stylesheet
    wp_enqueue_style( 'alexandria-dental-style', get_stylesheet_uri(), array(), '1.0.0' );
    
    // Google Fonts
    wp_enqueue_style( 
        'alexandria-dental-fonts', 
        'https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;700;800&family=Nunito:wght@400;600;700&display=swap',
        array(),
        null
    );

    if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
        wp_enqueue_script( 'comment-reply' );
    }
}
add_action( 'wp_enqueue_scripts', 'alexandria_dental_scripts' );

/**
 * Register widget areas.
 */
function alexandria_dental_widgets_init() {
    register_sidebar(
        array(
            'name'          => esc_html__( 'Sidebar', 'alexandria-dental' ),
            'id'            => 'sidebar-1',
            'description'   => esc_html__( 'Add widgets here.', 'alexandria-dental' ),
            'before_widget' => '<section id="%1$s" class="widget %2$s">',
            'after_widget'  => '</section>',
            'before_title'  => '<h3 class="widget-title">',
            'after_title'   => '</h3>',
        )
    );
}
add_action( 'widgets_init', 'alexandria_dental_widgets_init' );

/**
 * Default menu fallback for when no menu is assigned
 */
function alexandria_dental_default_menu() {
    echo '<ul id="primary-menu" class="primary-menu">';
    
    // Home
    echo '<li><a href="' . esc_url( home_url( '/' ) ) . '">Home</a></li>';
    
    // About
    $about_page = get_page_by_path('about');
    if ( $about_page ) {
        echo '<li><a href="' . esc_url( get_permalink( $about_page->ID ) ) . '">About</a></li>';
    }
    
    // Services dropdown
    echo '<li class="menu-item-has-children"><a href="#" onclick="return false;">Services</a>';
    echo '<ul class="sub-menu">';
    
    $service_pages = array(
        'cosmetic-dentistry' => 'Cosmetic Dentistry',
        'restorative' => 'Restorative',
        'preventative' => 'Preventative',
        'dental-implants' => 'Dental Implants',
        'invisalign' => 'Invisalign',
        'teeth-whitening' => 'Teeth Whitening',
        'dental-crowns' => 'Dental Crowns',
        'veneers' => 'Veneers'
    );
    
    foreach ( $service_pages as $slug => $title ) {
        $page = get_page_by_path( $slug );
        if ( $page ) {
            echo '<li><a href="' . esc_url( get_permalink( $page->ID ) ) . '">' . esc_html( $title ) . '</a></li>';
        }
    }
    echo '</ul></li>';
    
    // Patient Information dropdown
    echo '<li class="menu-item-has-children"><a href="#" onclick="return false;">Patient Information</a>';
    echo '<ul class="sub-menu">';
    
    $patient_pages = array(
        'patient-information' => 'Patient Information',
        'dental-insurance-accepted' => 'Insurance',
        'office-tour' => 'Office Tour',
        'testimonials' => 'Testimonials'
    );
    
    foreach ( $patient_pages as $slug => $title ) {
        $page = get_page_by_path( $slug );
        if ( $page ) {
            echo '<li><a href="' . esc_url( get_permalink( $page->ID ) ) . '">' . esc_html( $title ) . '</a></li>';
        }
    }
    echo '</ul></li>';
    
    // Blog
    if ( get_option( 'page_for_posts' ) ) {
        $blog_page_id = get_option( 'page_for_posts' );
        echo '<li><a href="' . esc_url( get_permalink( $blog_page_id ) ) . '">Blog</a></li>';
    } else {
        echo '<li><a href="' . esc_url( home_url( '/blog/' ) ) . '">Blog</a></li>';
    }
    
    // Contact
    $contact_page = get_page_by_path('contact-us');
    if ( $contact_page ) {
        echo '<li><a href="' . esc_url( get_permalink( $contact_page->ID ) ) . '">Contact</a></li>';
    }
    
    echo '</ul>';
}

/**
 * Add custom excerpt length.
 */
function alexandria_dental_excerpt_length( $length ) {
    return 25;
}
add_filter( 'excerpt_length', 'alexandria_dental_excerpt_length', 999 );

/**
 * Add custom excerpt more text.
 */
function alexandria_dental_excerpt_more( $more ) {
    return '...';
}
add_filter( 'excerpt_more', 'alexandria_dental_excerpt_more' );

/**
 * Customizer additions.
 */
function alexandria_dental_customize_register( $wp_customize ) {
    
    // Footer Settings Section
    $wp_customize->add_section( 'alexandria_dental_footer', array(
        'title'    => __( 'Footer Settings', 'alexandria-dental' ),
        'priority' => 130,
    ) );
    
    // Footer Address
    $wp_customize->add_setting( 'footer_address', array(
        'default'           => '',
        'sanitize_callback' => 'wp_kses_post',
    ) );
    
    $wp_customize->add_control( 'footer_address', array(
        'label'    => __( 'Practice Address', 'alexandria-dental' ),
        'section'  => 'alexandria_dental_footer',
        'type'     => 'textarea',
    ) );
    
    // Footer Phone
    $wp_customize->add_setting( 'footer_phone', array(
        'default'           => '',
        'sanitize_callback' => 'sanitize_text_field',
    ) );
    
    $wp_customize->add_control( 'footer_phone', array(
        'label'   => __( 'Practice Phone', 'alexandria-dental' ),
        'section' => 'alexandria_dental_footer',
        'type'    => 'text',
    ) );
    
    // Footer Email
    $wp_customize->add_setting( 'footer_email', array(
        'default'           => '',
        'sanitize_callback' => 'sanitize_email',
    ) );
    
    $wp_customize->add_control( 'footer_email', array(
        'label'   => __( 'Practice Email', 'alexandria-dental' ),
        'section' => 'alexandria_dental_footer',
        'type'    => 'email',
    ) );
    
    // Footer Hours
    $wp_customize->add_setting( 'footer_hours', array(
        'default'           => '',
        'sanitize_callback' => 'wp_kses_post',
    ) );
    
    $wp_customize->add_control( 'footer_hours', array(
        'label'   => __( 'Office Hours', 'alexandria-dental' ),
        'section' => 'alexandria_dental_footer',
        'type'    => 'textarea',
    ) );
    
    // Footer Disclaimer
    $wp_customize->add_setting( 'footer_disclaimer', array(
        'default'           => '',
        'sanitize_callback' => 'sanitize_text_field',
    ) );
    
    $wp_customize->add_control( 'footer_disclaimer', array(
        'label'   => __( 'Footer Disclaimer', 'alexandria-dental' ),
        'section' => 'alexandria_dental_footer',
        'type'    => 'textarea',
    ) );
}
add_action( 'customize_register', 'alexandria_dental_customize_register' );

/**
 * Add SEO meta tags
 */
function alexandria_dental_seo_meta() {
    if ( is_home() || is_front_page() ) {
        echo '<meta name="description" content="' . esc_attr( get_bloginfo( 'description' ) ) . '">' . "\n";
    } elseif ( is_single() || is_page() ) {
        global $post;
        if ( ! empty( $post->post_excerpt ) ) {
            echo '<meta name="description" content="' . esc_attr( wp_strip_all_tags( $post->post_excerpt ) ) . '">' . "\n";
        } else {
            $content = wp_strip_all_tags( $post->post_content );
            $excerpt = substr( $content, 0, 160 );
            echo '<meta name="description" content="' . esc_attr( $excerpt ) . '...">' . "\n";
        }
    }
}
add_action( 'wp_head', 'alexandria_dental_seo_meta' );

/**
 * Add page slug to body class
 */
function alexandria_dental_body_classes( $classes ) {
    global $post;
    
    if ( is_page() && $post ) {
        $classes[] = 'page-' . $post->post_name;
    }
    
    if ( is_single() && $post ) {
        $classes[] = 'post-' . $post->post_name;
    }
    
    return $classes;
}
add_filter( 'body_class', 'alexandria_dental_body_classes' );

/**
 * Remove WordPress version from head for security
 */
remove_action( 'wp_head', 'wp_generator' );

/**
 * Add support for Block Editor (Gutenberg)
 */
function alexandria_dental_gutenberg_support() {
    // Add support for editor color palette
    add_theme_support( 'editor-color-palette', array(
        array(
            'name'  => __( 'Primary Purple', 'alexandria-dental' ),
            'slug'  => 'primary-purple',
            'color' => '#32192f',
        ),
        array(
            'name'  => __( 'Accent Mauve', 'alexandria-dental' ),
            'slug'  => 'accent-mauve',
            'color' => '#a27295',
        ),
        array(
            'name'  => __( 'Hover Teal', 'alexandria-dental' ),
            'slug'  => 'hover-teal',
            'color' => '#72b7bc',
        ),
        array(
            'name'  => __( 'Bright Orange', 'alexandria-dental' ),
            'slug'  => 'bright-orange',
            'color' => '#ffae00',
        ),
    ) );
    
    // Add support for font sizes
    add_theme_support( 'editor-font-sizes', array(
        array(
            'name' => __( 'Small', 'alexandria-dental' ),
            'size' => 14,
            'slug' => 'small'
        ),
        array(
            'name' => __( 'Normal', 'alexandria-dental' ),
            'size' => 16,
            'slug' => 'normal'
        ),
        array(
            'name' => __( 'Large', 'alexandria-dental' ),
            'size' => 20,
            'slug' => 'large'
        ),
        array(
            'name' => __( 'Huge', 'alexandria-dental' ),
            'size' => 28,
            'slug' => 'huge'
        )
    ) );
}
add_action( 'after_setup_theme', 'alexandria_dental_gutenberg_support' ); 