<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    
    <?php wp_head(); ?>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;700;800&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
    
    <!-- Favicon -->
    <?php if ( function_exists( 'has_site_icon' ) && has_site_icon() ) : ?>
        <!-- Site icon handled by WordPress -->
    <?php else : ?>
        <link rel="icon" href="<?php echo get_template_directory_uri(); ?>/assets/images/favicon.png" sizes="32x32">
        <link rel="apple-touch-icon" href="<?php echo get_template_directory_uri(); ?>/assets/images/favicon.png">
    <?php endif; ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div id="page" class="site">
    <a class="skip-link screen-reader-text" href="#main-content"><?php esc_html_e('Skip to content', 'alexandria-dental-theme'); ?></a>

    <header id="masthead" class="site-header" role="banner">
        
        <!-- Top Header Row -->
        <div class="header-top-row">
            <div class="container">
                <div class="header-top-content">
                    
                    <!-- Small Logo -->
                    <div class="site-branding-small">
                        <?php if (has_custom_logo()) {
                            $custom_logo_id = get_theme_mod('custom_logo');
                            $logo = wp_get_attachment_image_src($custom_logo_id, 'full');
                            if ($logo) {
                                echo '<a href="' . esc_url(home_url('/')) . '" rel="home">';
                                echo '<img src="' . esc_url($logo[0]) . '" alt="' . get_bloginfo('name') . '" class="header-logo-small">';
                                echo '</a>';
                            }
                        } else { ?>
                            <div class="site-logo">
                                <a href="<?php echo esc_url(home_url('/')); ?>" rel="home"><?php bloginfo('name'); ?></a>
                            </div>
                        <?php } ?>
                    </div>
                    
                    <!-- Love Your Smile Text -->
                    <div class="header-tagline">
                        <strong>Love</strong> Your Smile
                    </div>
                    
                    <!-- Special Offers Button -->
                    <div class="header-cta">
                        <a href="<?php echo esc_url(home_url('/special')); ?>" class="btn-special-top">
                            view our special offers
                        </a>
                    </div>
                    
                </div>
            </div>
        </div>
        
        <!-- Main Header Row -->
        <div class="header-main-row">
            <div class="container">
                <div class="header-main-content">
                    
                    <!-- Large Logo -->
                    <div class="site-branding-large">
                        <?php if (has_custom_logo()) {
                            $custom_logo_id = get_theme_mod('custom_logo');
                            $logo = wp_get_attachment_image_src($custom_logo_id, 'full');
                            if ($logo) {
                                echo '<a href="' . esc_url(home_url('/')) . '" rel="home">';
                                echo '<img src="' . esc_url($logo[0]) . '" alt="' . get_bloginfo('name') . '" class="header-logo-main">';
                                echo '</a>';
                            }
                        } else { ?>
                            <div class="site-logo">
                                <a href="<?php echo esc_url(home_url('/')); ?>" rel="home"><?php bloginfo('name'); ?></a>
                            </div>
                        <?php } ?>
                    </div>
                    
                    <!-- Phone Number -->
                    <div class="header-phone">
                        <a href="tel:7032129622">(703) 212-9622</a>
                    </div>
                    
                    <!-- Special Offers Button -->
                    <div class="header-special-offers">
                        <a href="<?php echo esc_url(home_url('/special')); ?>" class="btn-special-main">
                            special offers
                        </a>
                    </div>
                    
                    <!-- Schedule Online Button -->
                    <div class="header-schedule">
                        <a href="https://app.nexhealth.com/appt/Mojgan_Mazhari_DDS?lid=70251" target="_blank" rel="noopener" class="btn-schedule">
                            Schedule Online
                        </a>
                    </div>
                    
                </div>
            </div>
        </div>
        
        <!-- Navigation Row -->
        <div class="header-nav-row">
            <div class="container">
                <nav id="site-navigation" class="main-navigation" role="navigation" aria-label="<?php esc_attr_e('Primary Menu', 'alexandria-dental-theme'); ?>">
                    <button class="menu-toggle" aria-controls="primary-menu" aria-expanded="false">
                        <span class="screen-reader-text"><?php esc_html_e( 'Primary Menu', 'alexandria-dental' ); ?></span>
                        <span class="hamburger-menu">
                            <span></span>
                            <span></span>
                            <span></span>
                        </span>
                    </button>
                    
                    <?php
                    wp_nav_menu(
                        array(
                            'theme_location' => 'primary',
                            'menu_id'        => 'primary-menu',
                            'container'      => false,
                            'menu_class'     => 'primary-menu',
                            'fallback_cb'    => 'alexandria_dental_default_menu',
                        )
                    );
                    ?>
                </nav>
            </div>
        </div>
        
    </header><!-- #masthead -->

    <main id="main-content" class="site-main">

</body>
</html> 