require 'json'

module Jekyll
  # Performance boost plugin for faster loading
  class PerformanceBoost < Jekyll::Generator
    safe true
    priority :high

    def generate(site)
      @site = site
      
      # Generate preload hints
      generate_preload_hints
      
      # Create resource hints
      create_resource_hints
      
      # Generate lazy loading scripts
      generate_lazy_loading
      
      # Create offline page
      create_offline_page
      
      Jekyll.logger.info "Performance boost applied"
    end

    private

    def generate_preload_hints
      preload_js = <<~JS
        // Resource preloading and prefetching
        (function() {
          // Preload critical resources
          const criticalResources = [
            '/assets/css/styles.css',
            '/assets/js/main.js'
          ];
          
          criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = resource;
            link.as = resource.endsWith('.css') ? 'style' : 'script';
            document.head.appendChild(link);
          });
          
          // Prefetch on hover
          document.addEventListener('mouseover', function(e) {
            const link = e.target.closest('a');
            if (link && link.hostname === window.location.hostname) {
              const prefetchLink = document.createElement('link');
              prefetchLink.rel = 'prefetch';
              prefetchLink.href = link.href;
              document.head.appendChild(prefetchLink);
            }
          });
          
          // Intersection Observer for lazy loading
          if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
              entries.forEach(entry => {
                if (entry.isIntersecting) {
                  const img = entry.target;
                  if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                  }
                }
              });
            });
            
            document.querySelectorAll('img[data-src]').forEach(img => {
              observer.observe(img);
            });
          }
        })();
      JS

      File.write(File.join(@site.source, 'assets/js/performance.js'), preload_js)
      @site.static_files << Jekyll::StaticFile.new(@site, @site.source, 'assets/js', 'performance.js')
    end

    def create_resource_hints
      hints_content = <<~HTML
        <!-- DNS Prefetch -->
        <link rel="dns-prefetch" href="//fonts.googleapis.com">
        <link rel="dns-prefetch" href="//cdnjs.cloudflare.com">
        <link rel="dns-prefetch" href="//cdn.jsdelivr.net">
        
        <!-- Preconnect -->
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        
        <!-- Early Hints -->
        <link rel="preload" href="/assets/css/styles.css" as="style">
        <link rel="preload" href="/assets/js/performance.js" as="script">
        
        <!-- Module Preload -->
        <link rel="modulepreload" href="/assets/js/modules/main.js">
      HTML

      File.write(File.join(@site.source, '_includes/resource-hints.html'), hints_content)
    end

    def generate_lazy_loading
      lazy_css = <<~CSS
        /* Lazy loading styles */
        img[data-src] {
          opacity: 0;
          transition: opacity 0.3s;
        }
        
        img.loaded {
          opacity: 1;
        }
        
        /* Loading placeholder */
        .img-placeholder {
          background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
          background-size: 200% 100%;
          animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
          0% { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
        
        /* Critical resource loading */
        .resource-loading {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 3px;
          background: linear-gradient(90deg, #007bff, #0056b3);
          z-index: 9999;
          transform: scaleX(0);
          transform-origin: left;
          transition: transform 0.3s ease;
        }
        
        .resource-loading.active {
          transform: scaleX(1);
        }
      CSS

      File.write(File.join(@site.source, 'assets/css/lazy-loading.css'), lazy_css)
      @site.static_files << Jekyll::StaticFile.new(@site, @site.source, 'assets/css', 'lazy-loading.css')
    end

    def create_offline_page
      offline_html = <<~HTML
        ---
        layout: default
        title: Offline
        permalink: /offline.html
        ---
        
        <div class="container text-center py-5">
          <h1 class="display-4 mb-4">You're Offline</h1>
          <p class="lead mb-4">Please check your internet connection and try again.</p>
          <button onclick="window.location.reload()" class="btn btn-primary">
            Try Again
          </button>
        </div>
        
        <script>
          // Register service worker
          if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
              navigator.serviceWorker.register('/sw.js')
                .then(function(registration) {
                  console.log('SW registered: ', registration);
                })
                .catch(function(registrationError) {
                  console.log('SW registration failed: ', registrationError);
                });
            });
          }
        </script>
      HTML

      File.write(File.join(@site.source, 'offline.html'), offline_html)
    end
  end

  # Image optimization hook
  class ImageOptimizer < Jekyll::Hook
    def self.register
      Jekyll::Hooks.register :site, :post_write do |site|
        optimize_images(site.dest)
      end
    end

    private

    def self.optimize_images(dest_dir)
      # Find all images
      image_files = Dir.glob(File.join(dest_dir, '**/*.{jpg,jpeg,png,svg}'))
      
      image_files.each do |image_path|
        # Add lazy loading attributes to HTML files referencing images
        update_html_with_lazy_loading(dest_dir, image_path)
      end
      
      Jekyll.logger.info "Processed #{image_files.length} images for optimization"
    end

    def self.update_html_with_lazy_loading(dest_dir, image_path)
      image_name = File.basename(image_path)
      
      Dir.glob(File.join(dest_dir, '**/*.html')).each do |html_file|
        content = File.read(html_file)
        
        # Replace img tags with lazy loading
        content.gsub!(/<img([^>]+)src="([^"]*#{Regexp.escape(image_name)}[^"]*)"([^>]*)>/) do |match|
          attrs_before = $1
          src = $2
          attrs_after = $3
          
          # Skip if already has data-src
          next match if match.include?('data-src')
          
          # Add lazy loading attributes
          %(<img#{attrs_before}data-src="#{src}" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'%3E%3C/svg%3E" class="img-placeholder"#{attrs_after}>)
        end
        
        File.write(html_file, content)
      end
    end
  end

  # Register the image optimizer
  ImageOptimizer.register
end