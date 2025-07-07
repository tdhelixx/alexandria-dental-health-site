<?php get_header(); ?>

<?php if (has_post_thumbnail()) : ?>
  <div class="banner-hero">
    <?php the_post_thumbnail('hero-image'); ?>
  </div>
<?php endif; ?>

<div class="container">
  <div class="row">
    <div class="col-md-8 content-area">
      <?php if (have_posts()) :
        while (have_posts()) : the_post(); ?>
          <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
            <div class="entry-content">
              <?php the_content(); ?>
            </div>
          </article>
        <?php endwhile;
      endif; ?>
    </div>
    <div class="col-md-4 sidebar-area">
      <?php get_sidebar(); ?>
    </div>
  </div>
</div>

<?php get_footer(); ?> 