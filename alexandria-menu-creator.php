<?php
/**
 * Plugin Name: Alexandria Dental Menu Creator
 * Plugin URI: https://alexandriadental.com
 * Description: One-click navigation menu creator for Alexandria Dental Health website
 * Version: 1.0.0
 * Author: Alexandria Dental Health
 * License: GPL v2 or later
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

class Alexandria_Menu_Creator {
    
    public function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_init', array($this, 'handle_menu_creation'));
    }
    
    /**
     * Add admin menu page
     */
    public function add_admin_menu() {
        add_management_page(
            'Alexandria Menu Creator',
            'Create Navigation Menu',
            'manage_options',
            'alexandria-menu-creator',
            array($this, 'admin_page')
        );
    }
    
    /**
     * Handle menu creation when form is submitted
     */
    public function handle_menu_creation() {
        if (!isset($_POST['create_alexandria_menu']) || !isset($_POST['_wpnonce'])) {
            return;
        }
        
        // Verify nonce
        if (!wp_verify_nonce($_POST['_wpnonce'], 'create_alexandria_menu')) {
            wp_die('Security check failed');
        }
        
        // Check permissions
        if (!current_user_can('manage_options')) {
            wp_die('You do not have sufficient permissions');
        }
        
        $this->create_navigation_menu();
        
        // Redirect with success message
        wp_redirect(add_query_arg('menu_created', '1', admin_url('tools.php?page=alexandria-menu-creator')));
        exit;
    }
    
    /**
     * Admin page content
     */
    public function admin_page() {
        ?>
        <div class="wrap">
            <h1>🦷 Alexandria Dental Menu Creator</h1>
            
            <?php if (isset($_GET['menu_created'])): ?>
                <div class="notice notice-success">
                    <p><strong>🎉 Success!</strong> Your navigation menu has been created!</p>
                    <p>
                        <a href="<?php echo home_url(); ?>" target="_blank" class="button">View Site</a>
                        <a href="<?php echo admin_url('nav-menus.php'); ?>" class="button button-primary">Edit Menus</a>
                    </p>
                </div>
            <?php endif; ?>
            
            <div class="card" style="max-width: 800px;">
                <h2>Create Professional Navigation Menu</h2>
                <p>This will create a complete navigation menu structure for your dental practice website including:</p>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                    <div>
                        <h3>🏠 Main Menu (6 items)</h3>
                        <ul style="margin-bottom: 20px;">
                            <li><strong>Home</strong></li>
                            <li><strong>About</strong> (6 sub-items)</li>
                            <li><strong>Patients</strong> (15 sub-items)</li>
                            <li><strong>Services</strong> (35+ sub-items)</li>
                            <li><strong>Conditions</strong> (8 sub-items)</li>
                            <li><strong>Contact</strong></li>
                        </ul>
                        
                        <h4>🎯 Complete Mega-Menu with:</h4>
                        <ul>
                            <li><strong>80+ total menu items</strong></li>
                            <li><strong>4 levels deep</strong> in some areas</li>
                            <li><strong>Perfect dental practice organization</strong></li>
                        </ul>
                    </div>
                    <div>
                        <h3>🦷 Services Structure</h3>
                        <ul style="font-size: 14px;">
                            <li><strong>Comprehensive</strong> (11 items)
                                <ul><li>Cleanings, Exams, Fillings, TMJ, etc.</li></ul>
                            </li>
                            <li><strong>Cosmetic</strong> (9 items)
                                <ul><li>Invisalign, Veneers, Whitening, etc.</li></ul>
                            </li>
                            <li><strong>Restorative</strong> (7 items)
                                <ul><li>Implants, Crowns, Bridges, etc.</li></ul>
                            </li>
                            <li><strong>Preventative</strong> (1 item)</li>
                            <li><strong>Family Dentistry</strong></li>
                            <li><strong>Emergency</strong></li>
                        </ul>
                        
                        <h4>📋 Plus:</h4>
                        <ul style="font-size: 14px;">
                            <li><strong>Patient FAQs</strong> (12 items)</li>
                            <li><strong>About sections</strong> (6 items)</li>
                            <li><strong>Conditions</strong> (8 items)</li>
                        </ul>
                    </div>
                </div>
                
                <div style="background: #f0f6fc; padding: 15px; border-left: 4px solid #0073aa; margin: 20px 0;">
                    <h4>⚠️ Important Notes:</h4>
                    <ul>
                        <li>This will <strong>replace</strong> any existing "Primary Menu"</li>
                        <li>The menu will be automatically assigned to your theme's primary navigation location</li>
                        <li><strong>Includes CSS fixes</strong> for proper 3rd & 4th level dropdown positioning</li>
                        <li>Multi-level dropdowns will appear to the <strong>right</strong> of parent items</li>
                        <li>You can edit the menu afterwards in <em>Appearance → Menus</em></li>
                        <li>This plugin can be deactivated after creating the menu</li>
                    </ul>
                </div>
                
                <form method="post" style="margin-top: 30px;">
                    <?php wp_nonce_field('create_alexandria_menu'); ?>
                    <p>
                        <button type="submit" name="create_alexandria_menu" class="button button-primary button-hero">
                            🚀 Create Navigation Menu
                        </button>
                    </p>
                </form>
            </div>
            
            <div class="card" style="max-width: 800px; margin-top: 20px;">
                <h3>🔧 After Creating Menu</h3>
                <p>Once your menu is created, you can:</p>
                <ul>
                    <li><strong>Edit it:</strong> Go to <em>Appearance → Menus</em></li>
                    <li><strong>Add more items:</strong> Add additional pages or custom links</li>
                    <li><strong>Reorder items:</strong> Drag and drop to reorganize</li>
                    <li><strong>Create more dropdowns:</strong> Add Patient Information submenu</li>
                    <li><strong>Deactivate this plugin:</strong> It's no longer needed after menu creation</li>
                </ul>
            </div>
        </div>
        
        <style>
        .card h3 { margin-top: 0; color: #23282d; }
        .card ul { margin: 10px 0; }
        .card li { margin: 5px 0; }
        .button-hero { font-size: 16px !important; padding: 10px 20px !important; height: auto !important; }
        </style>
        <?php
    }
    
    /**
     * Create the navigation menu
     */
    private function create_navigation_menu() {
        // Delete existing "Primary Menu" if it exists
        $existing_menu = wp_get_nav_menu_object('Primary Menu');
        if ($existing_menu) {
            wp_delete_nav_menu($existing_menu->term_id);
        }
        
        // Create new menu
        $menu_id = wp_create_nav_menu('Primary Menu');
        if (is_wp_error($menu_id)) {
            wp_die('Error creating menu: ' . $menu_id->get_error_message());
        }
        
        // Complete Alexandria Dental Health Menu Structure
        $menu_items = array(
            // ===== MAIN MENU ITEMS =====
            array(
                'title' => 'Home',
                'url' => home_url('/'),
                'parent' => 0
            ),
            array(
                'title' => 'About',
                'url' => home_url('/about/'),
                'parent' => 0,
                'is_parent' => true
            ),
            array(
                'title' => 'Patients',
                'url' => '#',
                'parent' => 0,
                'is_parent' => true
            ),
            array(
                'title' => 'Services',
                'url' => home_url('/services/'),
                'parent' => 0,
                'is_parent' => true
            ),
            array(
                'title' => 'Conditions',
                'url' => home_url('/concerns/'),
                'parent' => 0,
                'is_parent' => true
            ),
            array(
                'title' => 'Contact',
                'url' => home_url('/contact-us/'),
                'parent' => 0
            ),
            
            // ===== ABOUT SUBMENU =====
            array(
                'title' => 'Meet the Doctor',
                'url' => home_url('/us/'),
                'parent' => 'About'
            ),
            array(
                'title' => 'Advanced Technology',
                'url' => home_url('/advanced-technology/'),
                'parent' => 'About'
            ),
            array(
                'title' => 'Smile Gallery',
                'url' => home_url('/smile-gallery/'),
                'parent' => 'About'
            ),
            array(
                'title' => 'Testimonials',
                'url' => home_url('/testimonials/'),
                'parent' => 'About'
            ),
            array(
                'title' => 'Office Tour',
                'url' => home_url('/office-tour/'),
                'parent' => 'About'
            ),
            array(
                'title' => 'Blog',
                'url' => home_url('/blog/'),
                'parent' => 'About'
            ),
            
            // ===== PATIENTS SUBMENU =====
            array(
                'title' => 'Insurance',
                'url' => home_url('/dental-insurance-accepted/'),
                'parent' => 'Patients'
            ),
            array(
                'title' => 'Patient Information',
                'url' => home_url('/patient-information/'),
                'parent' => 'Patients'
            ),
            array(
                'title' => 'FAQs & Information',
                'url' => '#',
                'parent' => 'Patients',
                'is_parent' => true
            ),
            
            // ===== FAQS & INFORMATION SUB-SUBMENU =====
            array(
                'title' => 'Dental Crowns FAQ\'s',
                'url' => home_url('/dental-crowns-faqs/'),
                'parent' => 'FAQs & Information'
            ),
            array(
                'title' => 'Dental Implant Benefits',
                'url' => home_url('/dental-implant-benefits/'),
                'parent' => 'FAQs & Information'
            ),
            array(
                'title' => 'Dentures Cleaning & Care',
                'url' => home_url('/dentures-cleaning-and-care/'),
                'parent' => 'FAQs & Information'
            ),
            array(
                'title' => 'How to Brush Your Teeth',
                'url' => home_url('/how-to-brush-your-teeth/'),
                'parent' => 'FAQs & Information'
            ),
            array(
                'title' => 'How to Brush Your Teeth with Braces',
                'url' => home_url('/how-to-brush-teeth-with-braces/'),
                'parent' => 'FAQs & Information'
            ),
            array(
                'title' => 'How to Floss Your Teeth',
                'url' => home_url('/how-to-floss-your-teeth/'),
                'parent' => 'FAQs & Information'
            ),
            array(
                'title' => 'Importance of Baby Teeth',
                'url' => home_url('/importance-of-baby-teeth/'),
                'parent' => 'FAQs & Information'
            ),
            array(
                'title' => 'Root Canal Symptoms',
                'url' => home_url('/root-canal-symptoms/'),
                'parent' => 'FAQs & Information'
            ),
            array(
                'title' => 'Root Canal Recovery',
                'url' => home_url('/root-canal-recovery/'),
                'parent' => 'FAQs & Information'
            ),
            array(
                'title' => 'Symptoms of Gum Disease',
                'url' => home_url('/gum-disease-symptoms/'),
                'parent' => 'FAQs & Information'
            ),
            array(
                'title' => 'What is Cosmetic Dentistry?',
                'url' => home_url('/cosmetic-dentistry/'),
                'parent' => 'FAQs & Information'
            ),
            array(
                'title' => 'What To Do in a Dental Emergency',
                'url' => home_url('/emergency-dentistry/'),
                'parent' => 'FAQs & Information'
            ),
            
            // ===== SERVICES SUBMENU =====
            array(
                'title' => 'Comprehensive',
                'url' => home_url('/general-dentistry-services/'),
                'parent' => 'Services',
                'is_parent' => true
            ),
            array(
                'title' => 'Cosmetic',
                'url' => home_url('/cosmetic-restorative/'),
                'parent' => 'Services',
                'is_parent' => true
            ),
            array(
                'title' => 'Family Dentistry',
                'url' => home_url('/family-dentist/'),
                'parent' => 'Services'
            ),
            array(
                'title' => 'Emergency',
                'url' => home_url('/emergency-dental-information/'),
                'parent' => 'Services'
            ),
            array(
                'title' => 'Preventative',
                'url' => home_url('/preventative/'),
                'parent' => 'Services',
                'is_parent' => true
            ),
            array(
                'title' => 'Restorative',
                'url' => home_url('/restorative/'),
                'parent' => 'Services',
                'is_parent' => true
            ),
            
            // ===== COMPREHENSIVE SUB-SUBMENU =====
            array(
                'title' => 'Cavity Treatment',
                'url' => home_url('/dental-cavities-solutions/'),
                'parent' => 'Comprehensive'
            ),
            array(
                'title' => 'Cleanings',
                'url' => home_url('/dental-cleanings/'),
                'parent' => 'Comprehensive'
            ),
            array(
                'title' => 'Exams',
                'url' => home_url('/dental-exams/'),
                'parent' => 'Comprehensive'
            ),
            array(
                'title' => 'Fillings',
                'url' => home_url('/dental-fillings/'),
                'parent' => 'Comprehensive'
            ),
            array(
                'title' => 'Functional Orthodontics',
                'url' => home_url('/functional-orthodontics/'),
                'parent' => 'Comprehensive'
            ),
            array(
                'title' => 'Gingivitis Treatment',
                'url' => home_url('/dental-gingivitis-prevention/'),
                'parent' => 'Comprehensive'
            ),
            array(
                'title' => 'Periodontal Therapy',
                'url' => home_url('/periodontal-therapy/'),
                'parent' => 'Comprehensive'
            ),
            array(
                'title' => 'Sedation Dentistry',
                'url' => home_url('/sedation-dentistry/'),
                'parent' => 'Comprehensive'
            ),
            array(
                'title' => 'Sleep Apnea',
                'url' => home_url('/sleep-apnea/'),
                'parent' => 'Comprehensive'
            ),
            array(
                'title' => 'TMJ Treatment',
                'url' => home_url('/tmj-treatment/'),
                'parent' => 'Comprehensive'
            ),
            array(
                'title' => 'Tooth Extractions',
                'url' => home_url('/tooth-extractions/'),
                'parent' => 'Comprehensive'
            ),
            
            // ===== COSMETIC SUB-SUBMENU =====
            array(
                'title' => 'Cosmetic Bonding',
                'url' => home_url('/tooth-bonding/'),
                'parent' => 'Cosmetic'
            ),
            array(
                'title' => 'Gum Lifts',
                'url' => home_url('/gum-lifts/'),
                'parent' => 'Cosmetic'
            ),
            array(
                'title' => 'Invisalign',
                'url' => home_url('/invisalign/'),
                'parent' => 'Cosmetic',
                'is_parent' => true
            ),
            array(
                'title' => 'Lumineers',
                'url' => home_url('/lumineers/'),
                'parent' => 'Cosmetic'
            ),
            array(
                'title' => 'Removable Dental Appliances',
                'url' => home_url('/removable-dental-appliances/'),
                'parent' => 'Cosmetic'
            ),
            array(
                'title' => 'Six Month Smiles',
                'url' => home_url('/six-month-smiles/'),
                'parent' => 'Cosmetic'
            ),
            array(
                'title' => 'Snap On Smile',
                'url' => home_url('/snap-on-smile/'),
                'parent' => 'Cosmetic'
            ),
            array(
                'title' => 'Teeth Whitening',
                'url' => home_url('/teeth-whitening/'),
                'parent' => 'Cosmetic'
            ),
            array(
                'title' => 'Veneers',
                'url' => home_url('/veneers/'),
                'parent' => 'Cosmetic',
                'is_parent' => true
            ),
            
            // ===== INVISALIGN SUB-SUB-SUBMENU =====
            array(
                'title' => 'Invisalign Teen',
                'url' => home_url('/invisalign-teen/'),
                'parent' => 'Invisalign'
            ),
            
            // ===== VENEERS SUB-SUB-SUBMENU =====
            array(
                'title' => 'Getting Veneers',
                'url' => home_url('/getting-veneers/'),
                'parent' => 'Veneers'
            ),
            
            // ===== PREVENTATIVE SUB-SUBMENU =====
            array(
                'title' => 'Mouth Guards',
                'url' => home_url('/mouth-guards/'),
                'parent' => 'Preventative'
            ),
            
            // ===== RESTORATIVE SUB-SUBMENU =====
            array(
                'title' => 'Dental Bridges',
                'url' => home_url('/dental-bridges/'),
                'parent' => 'Restorative'
            ),
            array(
                'title' => 'Dental Crowns',
                'url' => home_url('/dental-crowns/'),
                'parent' => 'Restorative'
            ),
            array(
                'title' => 'Dental Implants',
                'url' => home_url('/dental-implants/'),
                'parent' => 'Restorative',
                'is_parent' => true
            ),
            array(
                'title' => 'Dentures',
                'url' => home_url('/dentures/'),
                'parent' => 'Restorative',
                'is_parent' => true
            ),
            array(
                'title' => 'Full Mouth Reconstruction',
                'url' => home_url('/full-mouth-reconstruction/'),
                'parent' => 'Restorative'
            ),
            array(
                'title' => 'Gum Disease Treatment',
                'url' => home_url('/gum-disease-treatment/'),
                'parent' => 'Restorative'
            ),
            array(
                'title' => 'Root Canal Therapy',
                'url' => home_url('/root-canal-therapy/'),
                'parent' => 'Restorative'
            ),
            
            // ===== DENTAL IMPLANTS SUB-SUB-SUBMENU =====
            array(
                'title' => 'What to Expect from Dental Implants',
                'url' => home_url('/about-dental-implants/'),
                'parent' => 'Dental Implants'
            ),
            
            // ===== DENTURES SUB-SUB-SUBMENU =====
            array(
                'title' => 'Implant Supported Dentures',
                'url' => home_url('/implant-supported-dentures/'),
                'parent' => 'Dentures'
            ),
            
            // ===== CONDITIONS SUBMENU =====
            array(
                'title' => 'Chipped/Broken Tooth',
                'url' => home_url('/chipped-tooth-repair/'),
                'parent' => 'Conditions'
            ),
            array(
                'title' => 'Crooked Teeth',
                'url' => home_url('/crooked-teeth/'),
                'parent' => 'Conditions'
            ),
            array(
                'title' => 'Dental Anxiety',
                'url' => home_url('/dental-anxiety/'),
                'parent' => 'Conditions'
            ),
            array(
                'title' => 'Headache Therapy',
                'url' => home_url('/headache-therapy/'),
                'parent' => 'Conditions'
            ),
            array(
                'title' => 'Jaw Pain',
                'url' => home_url('/jaw-pain/'),
                'parent' => 'Conditions'
            ),
            array(
                'title' => 'Missing Teeth',
                'url' => home_url('/missing-teeth/'),
                'parent' => 'Conditions'
            ),
            array(
                'title' => 'Teeth Grinding',
                'url' => home_url('/teeth-grinding/'),
                'parent' => 'Conditions'
            ),
            array(
                'title' => 'Tooth Pain',
                'url' => home_url('/tooth-pain/'),
                'parent' => 'Conditions'
            )
        );
        
        // Track parent IDs
        $parent_ids = array();
        $menu_order = 1;
        
        // Add all menu items
        foreach ($menu_items as $item) {
            $parent_id = 0;
            
            // Handle parent relationships
            if ($item['parent'] !== 0 && isset($parent_ids[$item['parent']])) {
                $parent_id = $parent_ids[$item['parent']];
            }
            
            // Add menu item
            $menu_item_id = wp_update_nav_menu_item($menu_id, 0, array(
                'menu-item-title' => $item['title'],
                'menu-item-url' => $item['url'],
                'menu-item-status' => 'publish',
                'menu-item-type' => 'custom',
                'menu-item-parent-id' => $parent_id,
                'menu-item-position' => $menu_order
            ));
            
            if (!is_wp_error($menu_item_id)) {
                // Store parent ID for children
                if (isset($item['is_parent']) && $item['is_parent']) {
                    $parent_ids[$item['title']] = $menu_item_id;
                }
            }
            
            $menu_order++;
        }
        
        // Assign menu to Primary Navigation location
        $locations = get_theme_mod('nav_menu_locations');
        $locations['primary'] = $menu_id;
        set_theme_mod('nav_menu_locations', $locations);
        
        // Add CSS for proper multi-level dropdown positioning
        $this->add_menu_css();
    }
    
    /**
     * Add CSS for proper multi-level dropdown positioning
     */
    private function add_menu_css() {
        $css = "
        <style id='alexandria-menu-fixes'>
        /* Fix for multi-level dropdown positioning */
        .primary-menu .sub-menu .sub-menu {
            left: 100% !important;
            top: 0 !important;
            margin-left: 0 !important;
        }
        
        /* Ensure 3rd level dropdowns appear to the right */
        .primary-menu .menu-item-has-children .sub-menu .menu-item-has-children .sub-menu {
            left: 100% !important;
            top: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Fix for 4th level dropdowns */
        .primary-menu .sub-menu .sub-menu .sub-menu {
            left: 100% !important;
            top: 0 !important;
        }
        
        /* Make sure dropdowns don't overlap parent text */
        .primary-menu .menu-item-has-children {
            position: relative !important;
        }
        
        .primary-menu .sub-menu {
            position: absolute !important;
            z-index: 9999 !important;
        }
        
        /* Alternative selectors for different themes */
        #primary-menu .sub-menu .sub-menu,
        .main-navigation .sub-menu .sub-menu,
        .site-navigation .sub-menu .sub-menu {
            left: 100% !important;
            top: 0 !important;
        }
        
        /* Hover state to show dropdowns */
        .primary-menu .menu-item-has-children:hover > .sub-menu,
        #primary-menu .menu-item-has-children:hover > .sub-menu,
        .main-navigation .menu-item-has-children:hover > .sub-menu {
            display: block !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        
        /* Mobile responsive - stack on mobile */
        @media (max-width: 768px) {
            .primary-menu .sub-menu .sub-menu {
                left: 0 !important;
                top: auto !important;
                position: relative !important;
                margin-left: 20px !important;
            }
        }
        </style>";
        
        // Add CSS to wp_head
        add_action('wp_head', function() use ($css) {
            echo $css;
        });
        
        // Also add CSS to admin_head for customizer preview
        add_action('admin_head', function() use ($css) {
            echo $css;
        });
    }
}

// Initialize the plugin
new Alexandria_Menu_Creator();

/**
 * Plugin deactivation cleanup
 */
register_deactivation_hook(__FILE__, function() {
    // Plugin can be safely deactivated after menu is created
    // Menu will remain in WordPress
}); 