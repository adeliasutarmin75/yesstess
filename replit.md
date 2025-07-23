# Jekyll Home Design Blog - Project Documentation

## Project Overview
A Jekyll-powered blog platform specifically designed for home design and interior inspiration content. The site features automated article generation, optimized image handling, and comprehensive AdSense preparation.

### Current Status: Active Development
- **Created**: January 2025
- **Last Major Update**: January 23, 2025
- **Environment**: Jekyll 4.x with Ruby/Python hybrid workflow

## Recent Changes

### ✓ Python Article Generator System Optimization (Jul 23, 2025)
- Fixed Python import dependencies and API integration
- Updated GitHub Actions workflow to use correct Article folder path
- Enhanced UpdateArticle.py with proper API key loading from both environment and files
- Created comprehensive test scripts for validating all components
- Verified all 43 API keys and 41 keywords are properly loaded
- Confirmed Python environment and dependencies are fully functional

### ✓ GitHub Actions Workflow Verification (Jul 23, 2025)
- Corrected all path references from `_Article` to `Article` in workflow
- Verified workflow components: rate limiting, usage tracking, and file handling
- Added manual testing capabilities with test_generator.py and workflow_test.py
- Confirmed automatic scheduling (5 times daily) and manual trigger options
- Enhanced error handling and API quota management

### ✓ Image Optimization System (Jan 23, 2025)
- Fixed popular posts image display with proper baseurl handling
- Added support for both internal and external images with fallbacks
- Created external image error handling with graceful degradation
- Enhanced responsive image component with better external URL support
- Added dedicated CSS for image optimization and loading states

### ✓ AdSense-Ready Page Structure (Jan 23, 2025)
- Created essential pages: Terms of Service, Cookie Policy, Sitemap, Archive
- Updated navigation to include all new pages
- Configured email format for multi-domain support
- Enhanced legal compliance for AdSense approval requirements

## Technical Architecture

### Frontend Stack
- **Jekyll 4.x**: Static site generator
- **SCSS/CSS**: Responsive styling with optimization focus
- **Bootstrap 5.1.3**: UI framework
- **Feather Icons & Font Awesome**: Icon systems
- **Google Fonts (Inter)**: Typography

### Backend/Automation
- **Python 3.11**: Article generation scripts
- **GitHub Actions**: Automated workflows
- **Gemini AI**: Content generation
- **Multiple APIs**: Image sourcing (Unsplash, Pixabay, Pexels)

### Performance Optimizations
- Compressed HTML/CSS/JS output
- Lazy loading for images
- Resource hints and preloading
- Optimized asset delivery
- Error fallback systems

## Key Features

### Content Management
- Automated article generation with AI
- Smart image handling (internal/external)
- Category and tag organization
- SEO optimization
- Social media integration

### User Experience
- Responsive design across all devices
- Dark mode support
- Fast loading times
- Accessible navigation
- Search functionality

### AdSense Preparation
- Complete legal page coverage
- Privacy policy with cookie handling
- Terms of service
- Site architecture documentation
- Email contact system

## Configuration

### Site Settings
- **Base URL**: `/ezz-terss`
- **Domain**: `adeliasutarmin75.github.io`
- **Email**: `info@adeliasutarmin75.github.io`
- **Timezone**: Asia/Jakarta

### Widget Configuration
- Popular posts: Enabled (5 posts)
- Categories: Enabled
- Tags: Disabled (performance)
- Search: Enabled
- Advertisement: Enabled but inactive

## File Structure

```
├── _config.yml              # Main Jekyll configuration
├── _data/
│   └── navigation.yml       # Site navigation menu
├── _includes/
│   ├── sidebar.html         # Enhanced with image optimization
│   ├── responsive-image.html # External/internal image handler
│   └── head.html           # CSS/JS includes
├── _layouts/                # Page templates
├── _pages/                 # Static pages (About, Contact, Legal)
├── _posts/                 # Blog posts
├── _sass/                  # SCSS styling
├── assets/
│   ├── css/                # Generated CSS files
│   ├── img/                # Site images
│   └── js/                 # JavaScript files
├── _Article/               # Python automation scripts
└── .github/workflows/      # GitHub Actions
```

## User Preferences

### Content Style
- Focus on home design and interior inspiration
- Professional tone with practical advice
- Visual-heavy content with external image support
- Budget-conscious tips and DIY approaches

### Technical Preferences
- Clean, minimal code structure
- Performance-first optimizations
- Comprehensive error handling
- Multi-domain flexibility
- SEO and monetization ready

## Workflow Management

### Article Generation
- **Automatic**: 5 times daily via GitHub Actions (2 AM, 6 AM, 10 AM, 2 PM, 6 PM UTC)
- **Manual**: Via workflow_dispatch with custom options
- **Test Mode**: Available for debugging without API usage
- **Custom Topics**: Manual topic specification supported
- **Python Script**: UpdateArticle.py with 43 API keys and 41 keywords loaded
- **Rate Limiting**: Maximum 2 articles per day with usage tracking

### Development Process
- Local Jekyll development server
- Live reloading for changes
- Asset optimization pipeline
- Automated deployment via GitHub Pages
- Python testing tools: test_generator.py, manual_test.py, workflow_test.py

## Troubleshooting Notes

### Common Issues Fixed
1. **Image Loading**: External images now have proper fallbacks
2. **Base URL**: All links properly use relative_url filter  
3. **Navigation**: All pages accessible via main menu
4. **Legal Compliance**: Complete page coverage for AdSense

### Performance Considerations
- Image optimization CSS reduces loading artifacts
- Error handling prevents broken image displays
- Lazy loading minimizes initial page load time
- Compressed assets reduce bandwidth usage

## Next Steps & Roadmap

### Immediate Priorities
- [ ] Test external image loading across different networks
- [ ] Validate AdSense compliance with all legal pages
- [ ] Test GitHub workflow with different trigger modes
- [ ] Optimize SEO for all new pages

### Future Enhancements
- [ ] Advanced image optimization (WebP conversion)
- [ ] Enhanced search functionality
- [ ] Comment system integration
- [ ] Newsletter signup system
- [ ] Social media automation

---

**Last Updated**: January 23, 2025 at 04:10 UTC  
**Next Review**: When major features added or user feedback received