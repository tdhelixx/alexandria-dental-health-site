<?php
/**
 * Template Name: Dental Page
 * 
 * Custom page template for Alexandria Dental Health pages
 * Ensures proper two-column layout with banner and sidebar
 *
 * @package Astra Child - Alexandria Dental Health
 */

get_header(); ?>

<div id="primary" class="content-area">
    
    <?php
    // Display featured image as full-width banner if it exists
    if ( has_post_thumbnail() ) : ?>
        <div class="dental-banner-hero">
            <?php the_post_thumbnail( 'dental-hero' ); ?>
        </div>
    <?php endif; ?>
    
    <div class="ast-container">
        <div class="ast-row">
            <div class="ast-col-lg-8 ast-col-md-8">
                <main id="main" class="site-main">
                    <?php
                    while ( have_posts() ) :
                        the_post();
                        ?>
                        <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                            
                            <?php
                            // Only show title if it's not already in the content
                            $content = get_the_content();
                            if ( strpos( $content, '<h1' ) === false ) : ?>
                                <header class="entry-header">
                                    <?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
                                </header>
                            <?php endif; ?>
                            
                            <div class="entry-content">
                                <?php
                                the_content();
                                
                                wp_link_pages( array(
                                    'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'astra-child-alexandria-dental' ),
                                    'after'  => '</div>',
                                ) );
                                ?>
                            </div>
                            
                            <?php if ( get_edit_post_link() ) : ?>
                                <footer class="entry-footer">
                                    <?php
                                    edit_post_link(
                                        sprintf(
                                            wp_kses(
                                                /* translators: %s: Name of current post. Only visible to screen readers */
                                                __( 'Edit <span class="screen-reader-text">%s</span>', 'astra-child-alexandria-dental' ),
                                                array(
                                                    'span' => array(
                                                        'class' => array(),
                                                    ),
                                                )
                                            ),
                                            get_the_title()
                                        ),
                                        '<span class="edit-link">',
                                        '</span>'
                                    );
                                    ?>
                                </footer>
                            <?php endif; ?>
                        </article>
                        
                        <?php
                        // If comments are open or we have at least one comment, load up the comment template.
                        if ( comments_open() || get_comments_number() ) :
                            comments_template();
                        endif;
                        
                    endwhile; // End of the loop.
                    ?>
                </main>
            </div>
            
            <div class="ast-col-lg-4 ast-col-md-4">
                <?php astra_child_dental_sidebar(); ?>
            </div>
        </div>
    </div>
    
</div>

<?php get_footer(); ?> 