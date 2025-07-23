// Performance Boost Script - Optimized for Speed
(function() {
  'use strict';
  
  // Critical performance optimizations
  const perfBoost = {
    // Preload resources on hover
    initPrefetch: function() {
      const links = document.querySelectorAll('a[href^="/"], a[href^="./"]');
      const prefetchedUrls = new Set();
      
      links.forEach(link => {
        let prefetchTimer;
        
        link.addEventListener('mouseenter', function() {
          const url = this.href;
          
          prefetchTimer = setTimeout(() => {
            if (!prefetchedUrls.has(url)) {
              const prefetchLink = document.createElement('link');
              prefetchLink.rel = 'prefetch';
              prefetchLink.href = url;
              document.head.appendChild(prefetchLink);
              prefetchedUrls.add(url);
            }
          }, 100); // 100ms delay for better UX
        });
        
        link.addEventListener('mouseleave', function() {
          clearTimeout(prefetchTimer);
        });
      });
    },
    
    // Lazy load images with intersection observer
    initLazyImages: function() {
      const images = document.querySelectorAll('img[data-src]');
      
      if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              const img = entry.target;
              img.src = img.dataset.src;
              img.classList.remove('lazy');
              img.classList.add('loaded');
              observer.unobserve(img);
            }
          });
        }, {
          rootMargin: '50px 0px',
          threshold: 0.01
        });
        
        images.forEach(img => {
          imageObserver.observe(img);
        });
      } else {
        // Fallback for older browsers
        images.forEach(img => {
          img.src = img.dataset.src;
          img.classList.remove('lazy');
          img.classList.add('loaded');
        });
      }
    },
    
    // Optimize CSS animations
    optimizeAnimations: function() {
      const style = document.createElement('style');
      style.textContent = `
        .post-card, .pagination-btn, .search-result-item {
          will-change: transform;
          backface-visibility: hidden;
          perspective: 1000px;
        }
        
        .post-card:hover {
          transform: translateZ(0) translateY(-5px);
        }
        
        .pagination-btn:hover {
          transform: translateZ(0) translateY(-3px);
        }
        
        .search-result-item:hover {
          transform: translateZ(0) translateY(-2px);
        }
        
        @media (prefers-reduced-motion: reduce) {
          .post-card, .pagination-btn, .search-result-item {
            transition: none !important;
          }
        }
      `;
      document.head.appendChild(style);
    },
    
    // Optimize fonts loading
    optimizeFonts: function() {
      const fontLink = document.createElement('link');
      fontLink.rel = 'preconnect';
      fontLink.href = 'https://fonts.googleapis.com';
      fontLink.crossOrigin = 'anonymous';
      document.head.appendChild(fontLink);
      
      const fontLink2 = document.createElement('link');
      fontLink2.rel = 'preconnect';
      fontLink2.href = 'https://fonts.gstatic.com';
      fontLink2.crossOrigin = 'anonymous';
      document.head.appendChild(fontLink2);
    },
    
    // Cache DOM queries
    cacheDOM: function() {
      window.domCache = {
        body: document.body,
        header: document.querySelector('header'),
        main: document.querySelector('main'),
        footer: document.querySelector('footer'),
        postCards: document.querySelectorAll('.post-card'),
        searchInput: document.querySelector('#search-input'),
        backToTop: document.querySelector('#back-to-top')
      };
    },
    
    // Optimize scroll performance
    optimizeScroll: function() {
      let ticking = false;
      
      function updateScrollPosition() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const backToTop = window.domCache.backToTop;
        
        if (backToTop) {
          if (scrollTop > 300) {
            backToTop.classList.add('show');
          } else {
            backToTop.classList.remove('show');
          }
        }
        
        ticking = false;
      }
      
      function requestTick() {
        if (!ticking) {
          requestAnimationFrame(updateScrollPosition);
          ticking = true;
        }
      }
      
      window.addEventListener('scroll', requestTick, { passive: true });
    },
    
    // Optimize search performance
    optimizeSearch: function() {
      const searchInput = window.domCache.searchInput;
      if (!searchInput) return;
      
      let searchTimeout;
      
      searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          // Debounced search logic here
          const query = this.value.trim();
          if (query.length >= 2) {
            // Trigger search
            window.dispatchEvent(new CustomEvent('searchQuery', { detail: query }));
          }
        }, 300);
      });
    },
    
    // Initialize all optimizations
    init: function() {
      // Wait for DOM to be ready
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
          this.cacheDOM();
          this.initPrefetch();
          this.initLazyImages();
          this.optimizeAnimations();
          this.optimizeFonts();
          this.optimizeScroll();
          this.optimizeSearch();
        });
      } else {
        this.cacheDOM();
        this.initPrefetch();
        this.initLazyImages();
        this.optimizeAnimations();
        this.optimizeFonts();
        this.optimizeScroll();
        this.optimizeSearch();
      }
    }
  };
  
  // Initialize performance optimizations
  perfBoost.init();
  
  // Service Worker registration
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
      navigator.serviceWorker.register('/sw.js').then(function(registration) {
        console.log('SW registered: ', registration);
      }).catch(function(registrationError) {
        console.log('SW registration failed: ', registrationError);
      });
    });
  }
  
  // Critical CSS loading
  const criticalCSS = document.createElement('link');
  criticalCSS.rel = 'preload';
  criticalCSS.href = '/critical.css';
  criticalCSS.as = 'style';
  criticalCSS.onload = function() {
    this.onload = null;
    this.rel = 'stylesheet';
  };
  document.head.appendChild(criticalCSS);
  
  // AdSense optimization disabled
  
})();