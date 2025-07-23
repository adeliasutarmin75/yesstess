require 'json'
require 'digest'

module Jekyll
  # Plugin for Cloudflare performance optimization
  class CloudflareOptimizer < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      @site = site
      
      # Generate service worker for caching
      generate_service_worker
      
      # Generate manifest for PWA
      generate_manifest
      
      # Optimize HTML for Cloudflare
      optimize_html_pages
      
      # Generate performance headers
      generate_headers_file
      
      # Generate cache manifest
      generate_cache_manifest
      
      Jekyll.logger.info "Cloudflare optimization completed"
    end

    private

    def generate_service_worker
      service_worker_content = <<~JS
        const CACHE_NAME = 'blog-v1';
        const urlsToCache = [
          '/',
          '/assets/css/styles.css',
          '/assets/js/main.js',
          '/offline.html'
        ];

        self.addEventListener('install', function(event) {
          event.waitUntil(
            caches.open(CACHE_NAME)
              .then(function(cache) {
                return cache.addAll(urlsToCache);
              })
          );
        });

        self.addEventListener('fetch', function(event) {
          event.respondWith(
            caches.match(event.request)
              .then(function(response) {
                if (response) {
                  return response;
                }
                return fetch(event.request);
              }
            )
          );
        });
      JS

      @site.static_files << Jekyll::StaticFile.new(@site, @site.source, '', 'sw.js')
      File.write(File.join(@site.source, 'sw.js'), service_worker_content)
    end

    def generate_manifest
      manifest = {
        name: @site.config['title'] || 'My Blog',
        short_name: @site.config['title'] || 'Blog',
        description: @site.config['description'] || 'A fast blog',
        start_url: '/',
        display: 'standalone',
        background_color: '#ffffff',
        theme_color: '#007bff',
        icons: [
          {
            src: '/assets/img/icon-192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/assets/img/icon-512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }

      File.write(File.join(@site.source, 'manifest.json'), JSON.pretty_generate(manifest))
      @site.static_files << Jekyll::StaticFile.new(@site, @site.source, '', 'manifest.json')
    end

    def optimize_html_pages
      @site.pages.each do |page|
        if page.output_ext == '.html'
          # Add performance hints to head
          page.content = add_performance_hints(page.content) if page.content
        end
      end
    end

    def add_performance_hints(content)
      performance_hints = <<~HTML
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://cdnjs.cloudflare.com">
        <link rel="dns-prefetch" href="//cdn.jsdelivr.net">
        <link rel="preload" href="/assets/css/styles.css" as="style">
        <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
      HTML
      
      content.gsub(/<head>/, "<head>\n#{performance_hints}")
    end

    def generate_headers_file
      headers_content = <<~HEADERS
        /*
          Cache-Control: public, max-age=31536000, immutable
          X-Frame-Options: DENY
          X-Content-Type-Options: nosniff
          Referrer-Policy: strict-origin-when-cross-origin
          Permissions-Policy: camera=(), microphone=(), geolocation=()

        /*.css
          Cache-Control: public, max-age=31536000, immutable
          Content-Type: text/css

        /*.js
          Cache-Control: public, max-age=31536000, immutable
          Content-Type: application/javascript

        /*.html
          Cache-Control: public, max-age=3600
          Content-Type: text/html; charset=utf-8

        /sw.js
          Cache-Control: no-cache
          Content-Type: application/javascript

        /*.webp
          Cache-Control: public, max-age=31536000
          Content-Type: image/webp

        /*.jpg
        /*.jpeg
        /*.png
        /*.svg
          Cache-Control: public, max-age=31536000
      HEADERS

      File.write(File.join(@site.source, '_headers'), headers_content)
      @site.static_files << Jekyll::StaticFile.new(@site, @site.source, '', '_headers')
    end

    def generate_cache_manifest
      cache_data = {
        version: Time.now.to_i,
        assets: collect_assets,
        pages: collect_pages
      }
      
      File.write(File.join(@site.source, 'cache-manifest.json'), JSON.pretty_generate(cache_data))
      @site.static_files << Jekyll::StaticFile.new(@site, @site.source, '', 'cache-manifest.json')
    end

    def collect_assets
      assets = []
      Dir.glob(File.join(@site.source, 'assets/**/*')).each do |file|
        if File.file?(file)
          relative_path = file.gsub(@site.source, '')
          assets << {
            path: relative_path,
            hash: Digest::MD5.hexdigest(File.read(file))[0..7]
          }
        end
      end
      assets
    end

    def collect_pages
      pages = []
      @site.pages.each do |page|
        if page.output_ext == '.html'
          pages << {
            url: page.url,
            title: page.data['title'] || 'Page'
          }
        end
      end
      pages
    end
  end

  # Minification and compression plugin
  class AssetMinifier < Jekyll::Generator
    safe true
    priority :lowest

    def generate(site)
      return unless Jekyll.env == 'production'
      
      minify_css_files(site)
      minify_js_files(site)
      compress_images(site)
      
      Jekyll.logger.info "Asset minification completed"
    end

    private

    def minify_css_files(site)
      css_files = Dir.glob(File.join(site.dest, '**/*.css'))
      css_files.each do |file|
        content = File.read(file)
        minified = content
          .gsub(/\/\*.*?\*\//m, '') # Remove comments
          .gsub(/\s+/, ' ')         # Collapse whitespace
          .gsub(/;\s*}/, '}')       # Remove unnecessary semicolons
          .gsub(/\s*{\s*/, '{')     # Clean braces
          .gsub(/;\s*/, ';')        # Clean semicolons
          .strip
        
        File.write(file, minified)
      end
    end

    def minify_js_files(site)
      js_files = Dir.glob(File.join(site.dest, '**/*.js'))
      js_files.each do |file|
        next if file.include?('sw.js') # Skip service worker
        
        content = File.read(file)
        minified = content
          .gsub(/\/\/.*$/, '')      # Remove single-line comments
          .gsub(/\/\*.*?\*\//m, '') # Remove multi-line comments
          .gsub(/\s+/, ' ')         # Collapse whitespace
          .gsub(/;\s*}/, '}')       # Clean up
          .strip
        
        File.write(file, minified)
      end
    end

    def compress_images(site)
      # Basic image optimization would go here
      # For now, just log that we would optimize images
      image_files = Dir.glob(File.join(site.dest, '**/*.{jpg,jpeg,png,svg}'))
      Jekyll.logger.info "Found #{image_files.length} images for optimization"
    end
  end

  # Critical CSS inliner
  class CriticalCSSInliner < Jekyll::Generator
    safe true
    priority :lowest

    def generate(site)
      return unless Jekyll.env == 'production'
      
      critical_css = extract_critical_css
      inline_critical_css(site, critical_css) if critical_css
      
      Jekyll.logger.info "Critical CSS inlined"
    end

    private

    def extract_critical_css
      css_file = File.join(@site.dest, 'assets/css/styles.css')
      return nil unless File.exist?(css_file)
      
      css_content = File.read(css_file)
      
      # Extract critical CSS (basic approach - above the fold styles)
      critical_rules = []
      
      # Include base styles
      critical_rules << css_content.match(/body\s*{[^}]*}/m)&.to_s
      critical_rules << css_content.match(/\.header[^{]*{[^}]*}/m)&.to_s
      critical_rules << css_content.match(/\.navigation[^{]*{[^}]*}/m)&.to_s
      critical_rules << css_content.match(/\.hero[^{]*{[^}]*}/m)&.to_s
      
      critical_rules.compact.join("\n")
    end

    def inline_critical_css(site, critical_css)
      site.pages.each do |page|
        next unless page.output_ext == '.html'
        
        if page.output && page.output.include?('<head>')
          page.output = page.output.gsub(
            '</head>',
            "<style>#{critical_css}</style>\n</head>"
          )
        end
      end
    end
  end
end