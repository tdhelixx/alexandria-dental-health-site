<?php
/*
Plugin Name: Alexandria Sidebar
Description: Adds a custom sidebar for use with Elementor Sidebar widget.
Version: 1.0
*/

function alexandria_sidebar_init() {
    register_sidebar([
        'name'          => 'Main Page Sidebar',
        'id'            => 'main_page_sidebar',
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ]);
}
add_action('widgets_init', 'alexandria_sidebar_init');
