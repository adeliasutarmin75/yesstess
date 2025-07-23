require 'json'
require 'fileutils'

module Jekyll
  # Cloudflare deployment optimization
  class CloudflareDeploy < Jekyll::Generator
    safe true
    priority :lowest

    def generate(site)
      @site = site
      
      # Generate Cloudflare Workers configuration
      generate_workers_config
      
      # Create deployment configuration
      create_deployment_config
      
      # Generate build optimization files
      generate_build_files
      
      # Create Cloudflare Pages configuration
      create_pages_config
      
      Jekyll.logger.info "Cloudflare deployment files generated"
    end

    private

    def generate_workers_config
      workers_script = <<~JS
        // Cloudflare Workers script for additional optimizations
        addEventListener('fetch', event => {
          event.respondWith(handleRequest(event.request))
        })

        async function handleRequest(request) {
          const url = new URL(request.url)
          
          // Apply additional headers for optimization
          const response = await fetch(request)
          const newResponse = new Response(response.body, response)
          
          // Add performance headers
          newResponse.headers.set('X-Content-Type-Options', 'nosniff')
          newResponse.headers.set('X-Frame-Options', 'DENY')
          newResponse.headers.set('X-XSS-Protection', '1; mode=block')
          newResponse.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
          
          // Cache optimization
          if (url.pathname.match(/\\.(css|js|png|jpg|jpeg|webp|svg|woff2?)$/)) {
            newResponse.headers.set('Cache-Control', 'public, max-age=31536000, immutable')
          } else if (url.pathname.endsWith('.html') || url.pathname === '/') {
            newResponse.headers.set('Cache-Control', 'public, max-age=3600')
          }
          
          // Compress responses
          if (request.headers.get('Accept-Encoding')?.includes('gzip')) {
            newResponse.headers.set('Content-Encoding', 'gzip')
          }
          
          return newResponse
        }
      JS

      workers_dir = File.join(@site.source, '_workers-site')
      FileUtils.mkdir_p(workers_dir)
      File.write(File.join(workers_dir, 'index.js'), workers_script)
      
      @site.static_files << Jekyll::StaticFile.new(@site, @site.source, '_workers-site', 'index.js')
    end

    def create_deployment_config
      wrangler_config = {
        name: "#{@site.config['title']&.downcase&.gsub(/[^a-z0-9]/, '-') || 'blog'}-site",
        type: "webpack",
        account_id: "YOUR_ACCOUNT_ID",
        workers_dev: true,
        route: "",
        zone_id: "YOUR_ZONE_ID",
        webpack_config: "webpack.config.js",
        site: {
          bucket: "./_site",
          entry_point: "_workers-site"
        },
        build: {
          command: "bundle exec jekyll build",
          cwd: ".",
          watch_dir: "."
        },
        env: {
          NODE_ENV: "production"
        }
      }

      File.write(File.join(@site.source, 'wrangler.toml'), wrangler_config.map { |k, v| 
        if v.is_a?(Hash)
          "[#{k}]\n" + v.map { |sk, sv| "#{sk} = #{sv.is_a?(String) ? "\"#{sv}\"" : sv}" }.join("\n")
        else
          "#{k} = #{v.is_a?(String) ? "\"#{v}\"" : v}"
        end
      }.join("\n\n"))
    end

    def generate_build_files
      # Create netlify.toml for Netlify deployment (alternative)
      netlify_config = <<~TOML
        [build]
          publish = "_site"
          command = "bundle exec jekyll build"
        
        [build.environment]
          JEKYLL_ENV = "production"
          NODE_VERSION = "18"
          RUBY_VERSION = "3.1"
        
        [[headers]]
          for = "/*"
          [headers.values]
            X-Frame-Options = "DENY"
            X-Content-Type-Options = "nosniff"
            Referrer-Policy = "strict-origin-when-cross-origin"
        
        [[headers]]
          for = "*.css"
          [headers.values]
            Cache-Control = "public, max-age=31536000, immutable"
        
        [[headers]]
          for = "*.js"
          [headers.values]
            Cache-Control = "public, max-age=31536000, immutable"
        
        [[headers]]
          for = "*.html"
          [headers.values]
            Cache-Control = "public, max-age=3600"
            
        [[headers]]
          for = "*.png"
          [headers.values]
            Cache-Control = "public, max-age=31536000"
            
        [[headers]]
          for = "*.jpg"
          [headers.values]
            Cache-Control = "public, max-age=31536000"
        
        [[redirects]]
          from = "/admin/*"
          to = "/404.html"
          status = 404
      TOML

      File.write(File.join(@site.source, 'netlify.toml'), netlify_config)

      # Create GitHub Actions workflow
      github_workflow = <<~YAML
        name: Deploy to Cloudflare Pages
        
        on:
          push:
            branches: [ main ]
          pull_request:
            branches: [ main ]
        
        jobs:
          deploy:
            runs-on: ubuntu-latest
            
            steps:
            - uses: actions/checkout@v3
            
            - name: Setup Ruby
              uses: ruby/setup-ruby@v1
              with:
                ruby-version: '3.1'
                bundler-cache: true
            
            - name: Setup Node.js
              uses: actions/setup-node@v3
              with:
                node-version: '18'
            
            - name: Install dependencies
              run: |
                bundle install
                npm install -g wrangler
            
            - name: Build Jekyll site
              run: |
                bundle exec jekyll build
                ls -la _site/
            
            - name: Deploy to Cloudflare Pages
              uses: cloudflare/pages-action@1
              with:
                apiToken: \${{ secrets.CLOUDFLARE_API_TOKEN }}
                accountId: \${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
                projectName: my-blog
                directory: _site
                gitHubToken: \${{ secrets.GITHUB_TOKEN }}
      YAML

      workflows_dir = File.join(@site.source, '.github/workflows')
      FileUtils.mkdir_p(workflows_dir)
      File.write(File.join(workflows_dir, 'deploy.yml'), github_workflow)
    end

    def create_pages_config
      # Create _redirects file for Cloudflare Pages
      redirects_content = <<~REDIRECTS
        # Redirects for Cloudflare Pages
        /admin/* /404.html 404
        /wp-admin/* /404.html 404
        /old-blog/* / 301
        
        # Headers for performance
        /*
          X-Frame-Options: DENY
          X-Content-Type-Options: nosniff
          X-XSS-Protection: 1; mode=block
          Referrer-Policy: strict-origin-when-cross-origin
          Permissions-Policy: camera=(), microphone=(), geolocation=()
      REDIRECTS

      File.write(File.join(@site.source, '_redirects'), redirects_content)
      @site.static_files << Jekyll::StaticFile.new(@site, @site.source, '', '_redirects')
    end
  end

  # Build optimization hook
  class BuildOptimizer < Jekyll::Hook
    def self.register
      Jekyll::Hooks.register :site, :post_write do |site|
        optimize_build(site.dest)
      end
    end

    private

    def self.optimize_build(dest_dir)
      # Generate asset manifest
      generate_asset_manifest(dest_dir)
      
      # Create sitemap if not exists
      create_sitemap(dest_dir) unless File.exist?(File.join(dest_dir, 'sitemap.xml'))
      
      # Optimize HTML files
      optimize_html_files(dest_dir)
      
      Jekyll.logger.info "Build optimization completed"
    end

    def self.generate_asset_manifest(dest_dir)
      assets = {}
      
      Dir.glob(File.join(dest_dir, 'assets/**/*')).each do |file|
        next unless File.file?(file)
        
        relative_path = file.gsub(dest_dir, '')
        file_size = File.size(file)
        
        assets[relative_path] = {
          size: file_size,
          type: File.extname(file),
          modified: File.mtime(file).to_i
        }
      end
      
      File.write(File.join(dest_dir, 'assets-manifest.json'), JSON.pretty_generate(assets))
    end

    def self.create_sitemap(dest_dir)
      sitemap_content = <<~XML
        <?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
          <url>
            <loc>#{ENV['SITE_URL'] || 'https://your-site.com'}/</loc>
            <changefreq>weekly</changefreq>
            <priority>1.0</priority>
          </url>
        </urlset>
      XML
      
      File.write(File.join(dest_dir, 'sitemap.xml'), sitemap_content)
    end

    def self.optimize_html_files(dest_dir)
      Dir.glob(File.join(dest_dir, '**/*.html')).each do |html_file|
        content = File.read(html_file)
        
        # Add loading indicators
        content.gsub!(/<body([^>]*)>/) do |match|
          attrs = $1
          "#{match}\n<div class=\"resource-loading\"></div>"
        end
        
        # Add performance monitoring
        content.gsub!(/<\/body>/) do |match|
          performance_script = <<~JS
            <script>
              // Performance monitoring
              window.addEventListener('load', function() {
                if (window.performance) {
                  const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
                  console.log('Page load time: ' + loadTime + 'ms');
                }
              });
            </script>
            #{match}
          JS
        end
        
        File.write(html_file, content)
      end
    end
  end

  # Register the build optimizer
  BuildOptimizer.register
end