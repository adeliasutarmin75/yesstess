document.addEventListener('DOMContentLoaded', function() {
  // Function to load all lazy images
  function loadLazyImages() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            const image = entry.target;
            image.src = image.dataset.src;
            image.classList.add('loaded');
            imageObserver.unobserve(image);
          }
        });
      }, { rootMargin: '50px 0px' });

      lazyImages.forEach(function(image) {
        imageObserver.observe(image);
      });
    } else {
      // Fallback for browsers without intersection observer
      lazyImages.forEach(function(image) {
        image.src = image.dataset.src;
        image.classList.add('loaded');
      });
    }
  }
  
  // Specifically target popular post images in sidebar
  function enhanceSidebarImages() {
    const popularPostImages = document.querySelectorAll('.popular-post-item .post-thumbnail img');
    
    popularPostImages.forEach(function(img) {
      // Ensure proper sizing and display
      img.style.display = 'block';
      
      // Add load event listener to remove placeholder when loaded
      img.addEventListener('load', function() {
        if (this.src !== this.dataset.src && this.dataset.src) {
          this.src = this.dataset.src;
          this.classList.add('loaded');
          
          // Remove fallback classes once properly loaded
          if (this.classList.contains('image-fallback')) {
            this.classList.remove('image-fallback');
          }
        }
      });
      
      // Force load images that might not be visible yet
      if (img.dataset.src) {
        // Create a new image to preload
        const tempImage = new Image();
        tempImage.onload = function() {
          img.src = img.dataset.src;
          img.classList.add('loaded');
        };
        tempImage.src = img.dataset.src;
      }
    });
  }

  // Initialize both functions
  loadLazyImages();
  enhanceSidebarImages();
  
  // Run again after a short delay to catch any late-rendering elements
  setTimeout(function() {
    loadLazyImages();
    enhanceSidebarImages();
  }, 1000);
});