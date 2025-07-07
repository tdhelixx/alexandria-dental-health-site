<?php get_header(); ?>

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
            <?php if (get_post_type() == 'post') : ?>
              <header class="entry-header">
                <?php the_title('<h1 class="entry-title">', '</h1>'); ?>
                <div class="entry-meta">
                  <span class="posted-on"><?php echo get_the_date(); ?></span>
                  <span class="byline"> | <?php the_author_posts_link(); ?></span>
                </div>
              </header>
            <?php endif; ?>
            <?php if (has_post_thumbnail()) {
              echo '<div class="post-thumbnail">';
              the_post_thumbnail('large');
              echo '</div>';
            } ?>
            <div class="entry-content">
              <?php the_content(); ?>
            </div>
            <?php if (get_post_type() == 'post') : ?>
              <footer class="entry-footer">
                <?php the_category(', '); ?>
                <?php the_tags('<span class="tag-links">', ', ', '</span>'); ?>
              </footer>
            <?php endif; ?>
          </article>
        <?php endwhile;
      endif; ?>
    </div>
    <aside class="sidebar-area col-md-4">
      <?php get_sidebar(); ?>
    </aside>
  </div>
</div>

<?php get_footer(); ?> 