// Main JavaScript functionality
(function() {
    'use strict';
    
    // Main site functionality
    const SiteModule = {
        // Initialize all site features
        init: function() {
            this.initNavigation();
            this.initImageHandling();
            this.initScrollEffects();
            this.initErrorHandling();
        },
        
        // Navigation enhancements
        initNavigation: function() {
            const nav = document.querySelector('.navbar');
            if (nav) {
                // Add scroll class for styling
                window.addEventListener('scroll', function() {
                    if (window.scrollY > 50) {
                        nav.classList.add('scrolled');
                    } else {
                        nav.classList.remove('scrolled');
                    }
                });
            }
        },
        
        // Image error handling and optimization
        initImageHandling: function() {
            const images = document.querySelectorAll('img');
            
            // Get base URL for multi-domain support
            const getBaseUrl = () => {
                const metaBaseUrl = document.querySelector('meta[name="base-url"]');
                return metaBaseUrl ? metaBaseUrl.content : '';
            };
            
            images.forEach(img => {
                // Handle image load errors
                img.addEventListener('error', function() {
                    if (!this.classList.contains('image-fallback')) {
                        const baseUrl = getBaseUrl();
                        const fallbackSrc = this.getAttribute('data-fallback') || 
                                           this.closest('[data-fallback]')?.getAttribute('data-fallback') ||
                                           `${baseUrl}/assets/img/default-post-image.svg`;
                        
                        this.src = fallbackSrc;
                        this.classList.add('image-fallback');
                        this.alt = this.alt || 'Image not available';
                    }
                });
                
                // Handle successful loads
                img.addEventListener('load', function() {
                    this.classList.add('loaded');
                });
            });
        },
        
        // Smooth scroll effects
        initScrollEffects: function() {
            // Smooth scroll for anchor links
            const anchorLinks = document.querySelectorAll('a[href^="#"]');
            
            anchorLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    const targetId = this.getAttribute('href').substring(1);
                    const targetElement = document.getElementById(targetId);
                    
                    if (targetElement) {
                        e.preventDefault();
                        targetElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        },
        
        // Global error handling
        initErrorHandling: function() {
            window.addEventListener('error', function(event) {
                console.error('JavaScript error:', event.error);
                // You could send this to analytics or error reporting service
            });
            
            // Handle promise rejections
            window.addEventListener('unhandledrejection', function(event) {
                console.error('Unhandled promise rejection:', event.reason);
            });
        }
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            SiteModule.init();
        });
    } else {
        SiteModule.init();
    }
    
    // Export module for external use
    window.SiteModule = SiteModule;
    
})();