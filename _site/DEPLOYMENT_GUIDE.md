# Automated Article Generator - Deployment Guide

## Overview
This project provides automated article generation for Jekyll blogs using:
- **UpdateArticle.py**: Optimized Python script for serverless execution
- **Cloudflare Workers**: Scheduled execution and webhook handling
- **GitHub Actions**: Fallback execution method
- **GitHub Integration**: Direct repository updates

## Features
✅ **Serverless Optimized**: Designed for Cloudflare Workers and GitHub Actions  
✅ **GitHub Integration**: Direct commits to repository  
✅ **Image Handling**: Automatic image download and upload  
✅ **Rate Limiting**: Built-in API protection  
✅ **Daily Scheduling**: Automated daily article generation  
✅ **Webhook Support**: Manual triggering via API calls  

## Deployment Options

### Option 1: Cloudflare Workers (Recommended)

#### Prerequisites
1. Cloudflare account with Workers enabled
2. GitHub repository with Jekyll blog
3. Gemini API keys for content generation

#### Setup Steps

1. **Install Wrangler CLI**
   ```bash
   npm install -g wrangler
   wrangler login
   ```

2. **Create KV Namespace**
   ```bash
   wrangler kv:namespace create "ARTICLES_KV"
   wrangler kv:namespace create "ARTICLES_KV" --preview
   ```

3. **Update wrangler.toml**
   ```toml
   name = "article-generator"
   main = "cloudflare-worker.js"
   compatibility_date = "2024-01-01"
   
   [[kv_namespaces]]
   binding = "ARTICLES_KV"
   id = "your-actual-kv-id"
   preview_id = "your-preview-kv-id"
   
   [triggers]
   crons = ["0 6 * * *"]  # Daily at 6 AM UTC
   
   [vars]
   GITHUB_REPO = "username/repository-name"
   GITHUB_BRANCH = "main"
   ```

4. **Set Required Secrets**
   ```bash
   # Required secrets
   wrangler secret put GEMINI_API_KEYS
   # Enter: key1,key2,key3
   
   wrangler secret put GITHUB_TOKEN
   # Enter: your GitHub personal access token with repo permissions
   
   wrangler secret put BLOG_KEYWORDS
   # Enter: ["modern living room","contemporary kitchen","bedroom design"]
   
   # Optional secrets
   wrangler secret put UNSPLASH_ACCESS_KEY
   wrangler secret put API_SECRET
   wrangler secret put GITHUB_WEBHOOK_SECRET
   ```

5. **Deploy Worker**
   ```bash
   wrangler deploy
   ```

#### Worker Endpoints
- `GET /health` - Health check
- `POST /generate` - Manual article generation (requires Authorization header)
- `POST /webhook` - GitHub webhook handler

### Option 2: GitHub Actions Only

The GitHub Actions workflow is already configured and will run:
- **Daily at 6 AM UTC** (automatic)
- **Manual trigger** via GitHub UI
- **Webhook trigger** from external services

#### Required Repository Secrets
Set these in GitHub Settings > Secrets and variables > Actions:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `GEMINI_API_KEYS` | Comma-separated Gemini API keys | `key1,key2,key3` |
| `BLOG_KEYWORDS` | JSON array of keywords | `["modern design","kitchen ideas"]` |
| `UNSPLASH_ACCESS_KEY` | Unsplash API key (optional) | `your-unsplash-key` |
| `PIXEL_API_CONFIG` | Pixel API configuration (optional) | `[{"key":"...","endpoint":"..."}]` |

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEYS` | ✅ | Comma-separated Gemini API keys |
| `GITHUB_TOKEN` | ✅ | GitHub personal access token |
| `GITHUB_REPO` | ✅ | Repository in format `owner/repo` |
| `BLOG_KEYWORDS` | ✅ | Keywords for article generation |
| `BLOG_CONFIG` | ❌ | Blog configuration JSON |
| `UNSPLASH_ACCESS_KEY` | ❌ | For image generation |
| `PIXEL_API_CONFIG` | ❌ | Alternative image API |

### Blog Configuration
```json
{
  "category": "Interior Design",
  "author": "Admin",
  "max_daily_articles": 2
}
```

### Keywords Format
```json
[
  "modern living room design",
  "contemporary kitchen ideas",
  "bedroom decoration tips",
  "bathroom renovation guide",
  "home office setup",
  "minimalist interior design"
]
```

## API Endpoints (Cloudflare Worker)

### Manual Generation
```bash
curl -X POST https://your-worker.your-subdomain.workers.dev/generate \
  -H "Authorization: Bearer your-api-secret"
```

### Health Check
```bash
curl https://your-worker.your-subdomain.workers.dev/health
```

## Monitoring

### GitHub Actions
- Check the Actions tab in your repository
- View logs for generation status
- Download artifacts for detailed logs

### Cloudflare Workers
- Monitor via Cloudflare Dashboard
- Check Real-time Logs
- View Analytics for execution stats

## Customization

### Modify Article Generation
Edit `_Article/UpdateArticle.py`:
- Adjust prompts for different content styles
- Modify rate limits
- Change article structure
- Add custom image handling

### Modify Scheduling
- **GitHub Actions**: Edit `.github/workflows/generate-article.yml` cron expression
- **Cloudflare Workers**: Update `wrangler.toml` triggers section

### Add New Keywords
- Update the `BLOG_KEYWORDS` secret/environment variable
- Keywords are automatically rotated to avoid repetition

## Troubleshooting

### Common Issues

1. **No articles generated**
   - Check API key validity
   - Verify daily limits haven't been reached
   - Check repository permissions

2. **Image upload failures**
   - Verify GitHub token has write permissions
   - Check image API keys
   - Review file size limits

3. **Rate limiting errors**
   - Reduce generation frequency
   - Add more API keys for rotation
   - Check API quotas

### Debug Commands
```bash
# Test UpdateArticle.py locally
cd _Article
BLOG_KEYWORDS='["test keyword"]' python3 UpdateArticle.py

# Check GitHub workflow logs
# Go to GitHub > Actions > Latest run

# Check Cloudflare Worker logs
wrangler tail
```

## Security

- All API keys are stored as encrypted secrets
- GitHub token has minimal required permissions
- Worker endpoints require authentication
- No sensitive data in logs or responses

## Limits

- **Daily Articles**: 2 per day (configurable)
- **API Calls**: 50 per day per key
- **Image Downloads**: 3 per article
- **File Sizes**: GitHub repository limits apply

## Support

For issues or customization requests:
1. Check the logs in GitHub Actions or Cloudflare Dashboard
2. Verify all required secrets are set correctly
3. Test individual components using the debug commands above