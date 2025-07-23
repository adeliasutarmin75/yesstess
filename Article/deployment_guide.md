# Deployment Guide - Professional Article Generator

## Quick Setup Checklist

### 1. Repository Setup
- [x] Copy `_Article/` folder to your Jekyll repository
- [x] Move `.github/workflows/auto-article-generator.yml` to repository root
- [x] Ensure `_Article/.nojekyll` exists for Cloudflare compatibility

### 2. Configuration Files
- [x] `_Article/CONFIG.txt` - Professional settings configured
- [x] `_Article/requirements.txt` - Python dependencies ready
- [x] `_Article/keyword.txt` - Add your article topics (one per line)
- [x] `_Article/pixel.txt` - Configure image APIs

### 3. GitHub Secrets Required
Set these in your repository Settings > Secrets and variables > Actions:

```
GEMINI_API_KEY=your-gemini-api-key-here
```

Optional (for enhanced image support):
```
PIXEL_API_KEYS=key1|endpoint1|limit1,key2|endpoint2|limit2
UNSPLASH_ACCESS_KEY=your-unsplash-key
PIXABAY_API_KEY=your-pixabay-key  
PEXELS_API_KEY=your-pexels-key
```

### 4. API Keys Setup

#### Gemini API Key (Required)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to repository secrets as `GEMINI_API_KEY`
4. Or add to `_Article/apikey.txt` (one key per line)

#### Image APIs (Optional)
- **Pixels API**: [pixels.com/api](https://pixels.com/api)
- **Unsplash**: [unsplash.com/developers](https://unsplash.com/developers) 
- **Pixabay**: [pixabay.com/api/docs](https://pixabay.com/api/docs/)
- **Pexels**: [pexels.com/api](https://pexels.com/api/)

### 5. Deployment Platforms

#### GitHub Pages
- No additional setup required
- GitHub Actions will build and deploy automatically
- Articles appear in `_posts/` folder

#### Cloudflare Pages
1. Connect your GitHub repository
2. Build settings:
   - Build command: `bundle exec jekyll build`
   - Build output: `_site`
3. Environment variables: Add your API keys

#### Netlify
- Use existing `netlify.toml` configuration
- Add environment variables in Netlify dashboard
- Automatic deployments on git push

### 6. Schedule Configuration

The system runs 5 times daily:
- 2 AM UTC
- 6 AM UTC
- 10 AM UTC
- 2 PM UTC
- 6 PM UTC

Maximum 2 articles generated per day for safety.

### 7. Manual Testing

Test the system locally:
```bash
cd _Article
python test_generator.py
```

Generate a single article manually:
```bash
cd _Article
python seo_generator_finals.py
```

### 8. Monitoring

Check these files for system status:
- `_Article/articles_data.json` - Generated articles database
- `_Article/last_run.json` - Usage tracking
- GitHub Actions logs - Execution details

## Safety Features

- **Rate Limiting**: Maximum 50 API requests per day
- **Daily Limits**: Maximum 2 articles per day
- **Error Recovery**: Automatic retry with fallbacks
- **Usage Tracking**: Monitors API usage and prevents overuse
- **Professional Quality**: Multi-stage generation with structure analysis

## Troubleshooting

### Common Issues

1. **No API Key Error**
   - Add `GEMINI_API_KEY` to GitHub secrets
   - Or add keys to `_Article/apikey.txt`

2. **Daily Limit Reached**
   - System automatically skips until next day
   - Check `_Article/last_run.json` for reset time

3. **No Keywords**
   - Add topics to `_Article/keyword.txt`
   - One keyword/topic per line

4. **Generation Fails**
   - Check GitHub Actions logs
   - Verify API key validity
   - Check rate limits

### Debug Steps

1. Run test script: `python _Article/test_generator.py`
2. Check configuration: Verify all files exist
3. Test API keys: Ensure valid and not expired
4. Review logs: GitHub Actions > Your workflow > Latest run

## Professional Features

- **Structure Analysis**: AI analyzes keywords and creates detailed outlines
- **Professional Writing**: Multi-stage content generation
- **Strategic Images**: Only adds images where needed based on analysis
- **SEO Optimization**: Meta descriptions, focus keywords, internal linking
- **Quality Control**: Professional tone and formatting

## Support

For technical issues:
1. Check `_Article/README.md` for detailed documentation
2. Review GitHub Actions logs for specific errors
3. Test locally with debug scripts
4. Verify API key permissions and limits