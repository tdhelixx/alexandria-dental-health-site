<aside id="secondary" class="widget-area custom-sidebar" role="complementary">
    
    <!-- Special Offer Button -->
    <div class="special-offer-box">
        <a href="<?php echo esc_url(home_url('/special')); ?>" class="special-offer-link">
            <span class="special-offer-top">VIEW OUR</span>
            <span class="special-offer-main">SPECIAL OFFERS</span>
            <span class="special-offer-cta">CLICK HERE ></span>
        </a>
    </div>
    
    <!-- Contact Information -->
    <div class="sidebar-contact">
        <h3>Alexandria Dental Health & Smile Studio</h3>
        <p><strong>2847 Duke St</strong><br>
        Alexandria VA 22314<br>
        <strong>(703) 212-9622</strong></p>
    </div>
    
    <!-- Office Hours -->
    <div class="sidebar-hours">
        <h3>Office Hours</h3>
        <p><strong>Monday:</strong> 8:00 AM - 5:00 PM<br>
        <strong>Tuesday:</strong> 8:00 AM - 5:00 PM<br>
        <strong>Wednesday:</strong> 8:00 AM - 5:00 PM<br>
        <strong>Thursday:</strong> 8:00 AM - 5:00 PM<br>
        <strong>Friday:</strong> 8:00 AM - 3:00 PM<br>
        <strong>Saturday:</strong> Closed<br>
        <strong>Sunday:</strong> Closed</p>
    </div>
    
    <!-- Google Maps -->
    <div class="sidebar-map">
        <h3>Our Location</h3>
        <iframe 
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3107.2698765432109!2d-77.08123456789!3d38.80987654321!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89b7b3f8a1234567%3A0x9876543210abcdef!2s2847%20Duke%20St%2C%20Alexandria%2C%20VA%2022314%2C%20USA!5e0!3m2!1sen!2sus!4v1640995200000!5m2!1sen!2sus"
            width="100%" 
            height="250" 
            style="border:0; border-radius: 8px; margin-top: 10px; display: block;" 
            allowfullscreen="" 
            loading="lazy" 
            referrerpolicy="no-referrer-when-downgrade"
            title="Alexandria Dental Health & Smile Studio Location">
        </iframe>
    </div>
    
    <?php if (is_active_sidebar('sidebar-1')) : ?>
        <?php dynamic_sidebar('sidebar-1'); ?>
    <?php endif; ?>
    
</aside> 