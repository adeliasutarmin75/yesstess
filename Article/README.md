# Professional SEO Article Generator

An advanced Jekyll article generation system optimized for GitHub Actions and Cloudflare deployment. This system automatically generates high-quality, SEO-optimized articles using AI with professional structure analysis and strategic content creation.

## 🚀 Features

- **Professional Article Structure**: AI-powered outline analysis and structured content generation
- **Strategic Image Integration**: Smart image placement only where needed
- **SEO Optimization**: Meta descriptions, focus keywords, and internal linking
- **Rate Limiting**: Safe API usage to prevent account bans
- **GitHub Actions Integration**: Automated scheduling with safety limits
- **Cloudflare Ready**: Optimized for static site deployment

## 📁 File Structure

```
_Article/
├── .nojekyll                    # Disables Jekyll processing
├── CONFIG.txt                   # Configuration settings
├── apikey.txt                   # Gemini API keys (one per line)
├── keyword.txt                  # Article keywords (one per line)
├── pixel.txt                    # Image API configurations
├── requirements.txt             # Python dependencies
├── seo_generator_finals.py      # Main generator script
├── test_generator.py           # Test script
├── articles_data.json          # Generated articles database
└── README.md                   # This file
```

## ⚙️ Configuration

### CONFIG.txt Settings

- **ARTICLES_PER_DAY**: Maximum articles per day (default: 2)
- **PROFESSIONAL_TONE**: Enable professional writing style
- **STRATEGIC_IMAGE_PLACEMENT**: Only add images where needed
- **RATE_LIMIT_REQUESTS**: Daily API request limit (default: 50)
- **AUTO_GENERATE_OUTLINE**: Enable structure analysis

### API Keys Setup

1. **Gemini API Keys** (`apikey.txt`):
   - Add one API key per line
   - Supports multiple keys for rotation
   - Can also use `GEMINI_API_KEY` environment variable

2. **Image APIs** (`pixel.txt`):
   - Format: `API_KEY|ENDPOINT_URL|DAILY_LIMIT`
   - Supports Pixel, Unsplash, Pixabay, Pexels

### Keywords (`keyword.txt`)

Add one keyword/topic per line:
```
digital marketing strategies
SEO optimization techniques
content marketing best practices
```

## 🤖 GitHub Actions Setup

The system runs automatically via GitHub Actions with these schedules:
- 2 AM UTC
- 6 AM UTC  
- 10 AM UTC
- 2 PM UTC
- 6 PM UTC

### Required Secrets

Set these in your repository secrets:

```
GEMINI_API_KEY=your-gemini-api-key
PIXEL_API_KEYS=key1|endpoint1|limit1,key2|endpoint2|limit2
UNSPLASH_ACCESS_KEY=your-unsplash-key (optional)
PIXABAY_API_KEY=your-pixabay-key (optional)
PEXELS_API_KEY=your-pexels-key (optional)
```

### Safety Features

- **Daily Limits**: Maximum 2 articles per day
- **Rate Limiting**: 50 API requests per day
- **Error Recovery**: Automatic retry with fallback
- **Usage Tracking**: Monitors API usage and limits

## 🏗️ Article Generation Process

1. **Keyword Selection**: Picks unused keyword from list
2. **Title Generation**: Creates SEO-optimized title
3. **Structure Analysis**: Analyzes keyword and creates detailed outline
4. **Content Generation**: 
   - Professional introduction
   - Structured main sections (H2/H3 headings)
   - Conclusion with call-to-action
5. **Image Integration**: Strategic placement only where needed
6. **SEO Optimization**: Meta descriptions, keywords, internal linking
7. **Quality Control**: Professional tone and formatting

## 🧪 Testing

Run the test script to verify setup:

```bash
cd _Article
python test_generator.py
```

## 🛡️ Safety Features

- **Account Protection**: Conservative API limits
- **Error Handling**: Comprehensive error recovery
- **Rate Limiting**: Built-in throttling
- **Usage Tracking**: Monitors daily usage
- **Fallback Systems**: Multiple API sources

## 📊 Output Format

Generated articles include:

- **Frontmatter**: Jekyll-compatible metadata
- **SEO Elements**: Title, description, keywords
- **Professional Structure**: H2/H3 headings, bullet points
- **Internal Links**: Related articles (when available)
- **Images**: Strategic placement with proper alt tags
- **Word Count**: 3000-5000 words per article

## 🔧 Manual Usage

Generate a single article manually:

```bash
cd _Article
python seo_generator_finals.py
```

## 📈 Monitoring

The system creates:

- `articles_data.json`: Article database with metadata
- `last_run.json`: Usage tracking and limits
- Detailed logging with timestamps
- GitHub Actions summaries

## 🚀 Deployment

Works with:

- **GitHub Pages**: Automatic Jekyll building
- **Cloudflare Pages**: Static site deployment  
- **Netlify**: JAMstack deployment
- **Any Static Host**: Pre-built _site folder

## 🆘 Troubleshooting

### Common Issues

1. **No API Keys**: Add keys to `apikey.txt` or set environment variable
2. **Daily Limit Reached**: System automatically skips until next day
3. **No Keywords**: Add topics to `keyword.txt`
4. **Generation Fails**: Check API key validity and rate limits

### Log Analysis

Check these files for debugging:
- GitHub Actions logs
- `articles_data.json` for generation history
- `last_run.json` for usage tracking

## 📝 License

This system is designed for personal and commercial use with proper API key management and rate limiting compliance.