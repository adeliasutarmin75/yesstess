// Performance monitoring and optimization
(function() {
    'use strict';
    
    // Performance tracking
    window.performance && window.performance.mark && window.performance.mark('script-start');
    
    // Page load time calculation
    function calculatePageLoadTime() {
        if (!window.performance || !window.performance.timing) {
            console.log('Page load time: Performance API not supported');
            return;
        }
        
        const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
        console.log('Page load time: ' + loadTime + 'ms');
        return loadTime;
    }
    
    // Image lazy loading optimization
    function optimizeImages() {
        const images = document.querySelectorAll('img[loading="lazy"]');
        
        if ('loading' in HTMLImageElement.prototype) {
            // Native lazy loading supported
            images.forEach(img => {
                img.addEventListener('load', function() {
                    this.classList.add('loaded');
                });
            });
        } else {
            // Fallback for browsers without native lazy loading
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src || img.src;
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            });
            
            images.forEach(img => imageObserver.observe(img));
        }
    }
    
    // CSS optimization
    function optimizeCSS() {
        // Remove unused CSS classes (basic implementation)
        const unusedClasses = [];
        
        // Critical CSS loading
        const criticalCSS = document.getElementById('critical-css');
        if (criticalCSS) {
            criticalCSS.rel = 'stylesheet';
        }
    }
    
    // Initialize performance optimizations
    function initPerformance() {
        // Wait for DOM content to be loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                optimizeImages();
                optimizeCSS();
                
                // Calculate page load time after everything is loaded
                window.addEventListener('load', calculatePageLoadTime);
            });
        } else {
            optimizeImages();
            optimizeCSS();
            calculatePageLoadTime();
        }
    }
    
    // Start performance monitoring
    initPerformance();
    
    // Export for other scripts
    window.PerformanceUtils = {
        calculatePageLoadTime: calculatePageLoadTime,
        optimizeImages: optimizeImages
    };
    
})();