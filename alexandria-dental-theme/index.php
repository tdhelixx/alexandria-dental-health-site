<?php
/**
 * The main template file
 *
 * This is the most generic template file in a WordPress theme
 * and one of the two required files for a theme (the other being style.css).
 * It is used to display a page when nothing more specific matches a query.
 */

get_header(); ?>

<?php if (have_posts()) : while (have_posts()) : the_post(); ?>
  <?php if (has_post_thumbnail()) : ?>
    <div class="banner-hero" style="width:100%;margin:0 auto 40px auto;max-width:100vw;overflow:hidden;">
      <?php the_post_thumbnail('hero-image', ['style' => 'width:100%;height:auto;display:block;margin:0 auto;']); ?>
    </div>
  <?php endif; ?>
  <?php rewind_posts(); // Reset loop for main content below ?>
<?php break; endwhile; endif; ?>

<div class="container">
  <div class="row">
    <div class="content-area col-md-8">
      <?php if (have_posts()) :
        while (have_posts()) : the_post(); ?>
          <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
            <?php if (is_home() || is_archive() || (is_singular() && get_post_type() == 'post')) : ?>
              <header class="entry-header">
                <?php if (is_singular()) {
                  the_title('<h1 class="entry-title">', '</h1>');
                } else {
                  the_title('<h2 class="entry-title"><a href="' . esc_url(get_permalink()) . '" rel="bookmark">', '</a></h2>');
                } ?>
              </header>
            <?php endif; ?>
            <div class="entry-content">
              <?php the_content(); ?>
            </div>
            <?php if (is_single() && has_post_thumbnail()) {
              echo '<div class="post-thumbnail">';
              the_post_thumbnail('large');
              echo '</div>';
            } ?>
          </article>
        <?php endwhile;
      else : ?>
        <p><?php esc_html_e('Sorry, no content found.', 'alexandria-dental-theme'); ?></p>
      <?php endif; ?>
    </div>
    <aside class="sidebar-area col-md-4">
      <?php get_sidebar(); ?>
    </aside>
  </div>
</div>

<?php get_footer(); ?> 