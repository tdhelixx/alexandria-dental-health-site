<?php
/**
 * The front page template file
 *
 * This template is used for the homepage
 */

get_header(); ?>

<main id="primary" class="site-main">
    
    <!-- Hero Section -->
    <section class="dental-hero">
        <div class="container">
            <h1><?php echo esc_html( get_theme_mod( 'hero_title', 'Welcome to Alexandria Dental Health & Smile Studio' ) ); ?></h1>
            <p><?php echo esc_html( get_theme_mod( 'hero_subtitle', 'Expert dental care in Alexandria, VA with Dr. Mazhari and our caring team.' ) ); ?></p>
            <a href="<?php echo esc_url( get_page_link( get_page_by_path( 'contact-us' ) ) ); ?>" class="btn btn-primary">Schedule Your Appointment</a>
        </div>
    </section>

    <div class="container">
        
        <?php if ( have_posts() ) : ?>
            <?php while ( have_posts() ) : the_post(); ?>
                
                <?php if ( ! empty( get_the_content() ) ) : ?>
                    <section class="homepage-content">
                        <div class="entry-content">
                            <?php the_content(); ?>
                        </div>
                    </section>
                <?php endif; ?>
                
            <?php endwhile; ?>
        <?php endif; ?>
        
        <!-- Services Overview -->
        <section class="services-overview">
            <h2 class="text-center">Our Dental Services</h2>
            <p class="text-center">Comprehensive dental care for the entire family</p>
            
            <div class="services-grid">
                
                <div class="service-card">
                    <img src="<?php echo get_template_directory_uri(); ?>/assets/images/cosmetic-dentistry-icon.svg" alt="Cosmetic Dentistry" onerror="this.style.display='none'">
                    <h3>Cosmetic Dentistry</h3>
                    <p>Transform your smile with veneers, teeth whitening, and smile makeovers.</p>
                    <a href="<?php echo esc_url( get_page_link( get_page_by_path( 'cosmetic-dentistry' ) ) ); ?>" class="btn">Learn More</a>
                </div>
                
                <div class="service-card">
                    <img src="<?php echo get_template_directory_uri(); ?>/assets/images/dental-implants-icon.svg" alt="Dental Implants" onerror="this.style.display='none'">
                    <h3>Dental Implants</h3>
                    <p>Permanent tooth replacement solution for missing teeth.</p>
                    <a href="<?php echo esc_url( get_page_link( get_page_by_path( 'dental-implants' ) ) ); ?>" class="btn">Learn More</a>
                </div>
                
                <div class="service-card">
                    <img src="<?php echo get_template_directory_uri(); ?>/assets/images/preventative-care-icon.svg" alt="Preventative Care" onerror="this.style.display='none'">
                    <h3>Preventative Care</h3>
                    <p>Regular cleanings, exams, and preventative treatments.</p>
                    <a href="<?php echo esc_url( get_page_link( get_page_by_path( 'preventative' ) ) ); ?>" class="btn">Learn More</a>
                </div>
                
                <div class="service-card">
                    <img src="<?php echo get_template_directory_uri(); ?>/assets/images/invisalign-icon.svg" alt="Invisalign" onerror="this.style.display='none'">
                    <h3>Invisalign</h3>
                    <p>Straighten your teeth with clear, removable aligners.</p>
                    <a href="<?php echo esc_url( get_page_link( get_page_by_path( 'invisalign' ) ) ); ?>" class="btn">Learn More</a>
                </div>
                
                <div class="service-card">
                    <img src="<?php echo get_template_directory_uri(); ?>/assets/images/restorative-icon.svg" alt="Restorative Dentistry" onerror="this.style.display='none'">
                    <h3>Restorative Dentistry</h3>
                    <p>Crowns, bridges, and fillings to restore your smile.</p>
                    <a href="<?php echo esc_url( get_page_link( get_page_by_path( 'restorative' ) ) ); ?>" class="btn">Learn More</a>
                </div>
                
                <div class="service-card">
                    <img src="<?php echo get_template_directory_uri(); ?>/assets/images/emergency-dental-icon.svg" alt="Emergency Dentistry" onerror="this.style.display='none'">
                    <h3>Emergency Dentistry</h3>
                    <p>Urgent dental care when you need it most.</p>
                    <a href="<?php echo esc_url( get_page_link( get_page_by_path( 'emergency-dentistry' ) ) ); ?>" class="btn">Learn More</a>
                </div>
                
            </div>
            
            <div class="text-center mt-40">
                <a href="<?php echo esc_url( get_page_link( get_page_by_path( 'services' ) ) ); ?>" class="btn">View All Services</a>
            </div>
        </section>
        
        <!-- About Preview -->
        <section class="about-preview">
            <div class="row">
                <div class="col">
                    <h2>Meet Dr. Mazhari</h2>
                    <p>Dr. Mojgan Mazhari and the team at Alexandria Dental Health & Smile Studio are committed to providing exceptional dental care in a comfortable, modern environment. We combine advanced technology with personalized care to ensure each patient receives the best possible treatment.</p>
                    <p>Our comprehensive approach to dentistry means we can address all your oral health needs under one roof, from routine cleanings to complex restorative procedures.</p>
                    <a href="<?php echo esc_url( get_page_link( get_page_by_path( 'about' ) ) ); ?>" class="btn">Learn More About Us</a>
                </div>
                <div class="col">
                    <img src="<?php echo get_template_directory_uri(); ?>/assets/images/dr-mazhari.jpg" alt="Dr. Mojgan Mazhari" class="img-fluid" onerror="this.style.display='none'">
                </div>
            </div>
        </section>
        
        <!-- Contact CTA -->
        <section class="contact-cta">
            <div class="dental-hero">
                <h2>Ready to Schedule Your Appointment?</h2>
                <p>Contact our friendly team today to begin your journey to optimal oral health.</p>
                <div class="cta-buttons">
                    <a href="<?php echo esc_url( get_page_link( get_page_by_path( 'contact-us' ) ) ); ?>" class="btn btn-primary">Contact Us</a>
                    <a href="tel:<?php echo esc_attr( str_replace( array( ' ', '-', '(', ')', '.' ), '', get_theme_mod( 'footer_phone', '(703) 123-4567' ) ) ); ?>" class="btn">Call Now</a>
                </div>
            </div>
        </section>
        
    </div>
    
</main>

<?php get_footer(); ?> 