    </main>
    <footer class="site-footer" role="contentinfo">
        <div class="container">
            <div class="footer-content" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; padding: 20px 0; border-top: 1px solid rgba(255,255,255,0.1);">
                
                <!-- Copyright -->
                <div class="site-info">
                    &copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. All rights reserved.
                </div>
                
                <!-- Simple Footer Navigation -->
                <nav class="footer-navigation" aria-label="<?php esc_attr_e('Footer Menu', 'alexandria-dental-theme'); ?>">
                    <?php
                    wp_nav_menu(array(
                        'theme_location' => 'footer',
                        'menu_class'     => 'footer-menu',
                        'container'      => false,
                        'fallback_cb'    => 'alexandria_dental_simple_footer_menu',
                    ));
                    ?>
                </nav>
                
            </div>
        </div>
    </footer>
</div><!-- .fl-page -->
<?php wp_footer(); ?>
</body>
</html>

<?php
/**
 * Simple footer menu fallback
 */
function alexandria_dental_simple_footer_menu() {
    echo '<ul class="footer-menu">';
    
    $footer_pages = array(
        'about' => 'About',
        'services' => 'Services',
        'contact-us' => 'Contact',
        'privacy-policy' => 'Privacy Policy',
        'terms-service' => 'Terms of Service'
    );
    
    foreach ( $footer_pages as $slug => $title ) {
        $page = get_page_by_path( $slug );
        if ( $page ) {
            echo '<li><a href="' . esc_url( get_permalink( $page->ID ) ) . '">' . esc_html( $title ) . '</a></li>';
        }
    }
    
    echo '</ul>';
}
?> 