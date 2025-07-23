#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimized Article Generator for Cloudflare Workers + GitHub Integration
Enhanced for deployment compatibility and serverless execution
"""

import os
import re
import time
import json
import random
import datetime
import requests
import markdown
import asyncio
import aiohttp
import aiofiles
from pathlib import Path
import xml.etree.ElementTree as ET
import frontmatter
import yaml
from slugify import slugify
from langdetect import detect
import google.generativeai as genai
from urllib.parse import quote_plus
import logging
from typing import List, Dict, Optional, Tuple
from asyncio_throttle.throttler import Throttler
import base64

# Set up logging for serverless environment
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class CloudflareOptimizedArticleGenerator:
    """
    Optimized for Cloudflare Workers deployment with GitHub integration
    Designed to work with environment variables and minimal file dependencies
    """
    
    def __init__(self, config_data: Optional[Dict] = None):
        self.config = config_data or {}
        self.api_keys = []
        self.pixel_apis = []
        self.articles_data = []
        self.used_keywords = set()
        self.current_api_index = 0
        self.daily_requests = 0
        self.max_daily_requests = 50
        
        # Rate limiters optimized for serverless
        self.gemini_throttler = Throttler(rate_limit=8, period=60)
        self.image_throttler = Throttler(rate_limit=3, period=60)
        
        # GitHub integration settings
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.github_repo = os.environ.get('GITHUB_REPO')  # format: username/repo
        self.github_branch = os.environ.get('GITHUB_BRANCH', 'main')
        
        self.load_from_environment()
    
    def load_from_environment(self):
        """Load all configuration from environment variables"""
        try:
            # Load API keys from environment or file
            gemini_keys = os.environ.get('GEMINI_API_KEYS', '').split(',')
            self.api_keys = [key.strip() for key in gemini_keys if key.strip()]
            
            # Fallback to apikey.txt file
            if not self.api_keys:
                api_file = Path(__file__).parent / 'apikey.txt'
                if api_file.exists():
                    with open(api_file, 'r', encoding='utf-8') as f:
                        file_keys = [line.strip() for line in f.readlines() if line.strip()]
                    self.api_keys = file_keys
                    logger.info(f"Loaded {len(file_keys)} API keys from apikey.txt")
            
            # Load Pixel API configurations
            pixel_config = os.environ.get('PIXEL_API_CONFIG', '')
            if pixel_config:
                try:
                    pixel_data = json.loads(pixel_config)
                    self.pixel_apis = pixel_data if isinstance(pixel_data, list) else []
                except json.JSONDecodeError:
                    logger.warning("Invalid PIXEL_API_CONFIG format")
            
            # Load configuration settings
            config_json = os.environ.get('BLOG_CONFIG', '{}')
            try:
                env_config = json.loads(config_json)
                self.config.update(env_config)
            except json.JSONDecodeError:
                logger.warning("Invalid BLOG_CONFIG format")
            
            # Load existing articles data
            articles_json = os.environ.get('ARTICLES_DATA', '{}')
            try:
                articles_data = json.loads(articles_json)
                self.articles_data = articles_data.get('articles', [])
                self.used_keywords = set(articles_data.get('used_keywords', []))
                self.daily_requests = articles_data.get('daily_requests', 0)
            except json.JSONDecodeError:
                logger.warning("Invalid ARTICLES_DATA format")
            
            logger.info(f"Environment loaded: {len(self.api_keys)} API keys, {len(self.articles_data)} articles")
            
        except Exception as e:
            logger.error(f"Error loading environment configuration: {e}")
    
    def get_keywords_from_env(self) -> List[str]:
        """Load keywords from keyword.txt file or environment variable"""
        # Try to load from keyword.txt file first
        keyword_file = Path(__file__).parent / 'keyword.txt'
        if keyword_file.exists():
            try:
                with open(keyword_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                keywords = [
                    keyword.strip() for keyword in content.splitlines()
                    if keyword.strip() and not keyword.startswith('#')
                ]
                if keywords:
                    logger.info(f"Loaded {len(keywords)} keywords from keyword.txt")
                    return keywords
            except Exception as e:
                logger.error(f"Error reading keyword.txt: {e}")
        
        # Fallback to environment variable
        keywords_data = os.environ.get('BLOG_KEYWORDS', '')
        if keywords_data:
            try:
                # Support both JSON array and newline-separated format
                if keywords_data.startswith('['):
                    return json.loads(keywords_data)
                else:
                    return [k.strip() for k in keywords_data.split('\n') if k.strip()]
            except json.JSONDecodeError:
                return keywords_data.split(',')
        
        logger.warning("No keywords found in keyword.txt or BLOG_KEYWORDS environment")
        return []
    
    def get_next_keyword(self) -> Optional[str]:
        """Get next unused keyword from environment"""
        keywords = self.get_keywords_from_env()
        available_keywords = [k for k in keywords if k not in self.used_keywords]
        
        if not available_keywords:
            self.used_keywords = set()  # Reset if all used
            available_keywords = keywords
        
        return random.choice(available_keywords) if available_keywords else None
    
    async def rotate_api_key(self) -> str:
        """Safely rotate API keys"""
        if not self.api_keys:
            raise Exception("No API keys available in environment")
        
        key = self.api_keys[self.current_api_index % len(self.api_keys)]
        self.current_api_index += 1
        return key
    
    async def generate_with_gemini(self, prompt: str, model_name: str = 'gemini-1.5-flash') -> str:
        """Generate content with Gemini API using optimized rate limiting"""
        async with self.gemini_throttler:
            try:
                api_key = await self.rotate_api_key()
                genai.configure(api_key=api_key)
                
                model = genai.GenerativeModel(model_name)
                
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
                ]
                
                generation_config = genai.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    max_output_tokens=4000,
                )
                
                response = model.generate_content(
                    prompt,
                    safety_settings=safety_settings,
                    generation_config=generation_config
                )
                
                self.daily_requests += 1
                return response.text.strip() if response.text else ""
                
            except Exception as e:
                logger.error(f"Error with Gemini API: {e}")
                await asyncio.sleep(1)
                return ""
    
    async def search_images_optimized(self, query: str, count: int = 2) -> List[str]:
        """Optimized image search for serverless environment"""
        images = []
        
        # Use Unsplash as primary source (most reliable for serverless)
        unsplash_key = os.environ.get('UNSPLASH_ACCESS_KEY')
        if unsplash_key:
            try:
                async with aiohttp.ClientSession() as session:
                    headers = {'Authorization': f'Client-ID {unsplash_key}'}
                    params = {'query': query, 'per_page': count, 'orientation': 'landscape'}
                    
                    async with session.get(
                        'https://api.unsplash.com/search/photos',
                        headers=headers,
                        params=params,
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            for photo in data.get('results', []):
                                img_url = photo.get('urls', {}).get('regular')
                                if img_url:
                                    images.append(img_url)
                                    if len(images) >= count:
                                        break
            except Exception as e:
                logger.error(f"Error with Unsplash API: {e}")
        
        return images[:count]
    
    async def upload_image_to_github(self, image_url: str, filename: str) -> Optional[str]:
        """Upload image directly to GitHub repository"""
        if not self.github_token or not self.github_repo:
            logger.warning("GitHub configuration missing")
            return None
        
        try:
            # Download image
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        
                        # Upload to GitHub
                        github_path = f"assets/images/{filename}"
                        github_url = f"https://api.github.com/repos/{self.github_repo}/contents/{github_path}"
                        
                        headers = {
                            'Authorization': f'token {self.github_token}',
                            'Accept': 'application/vnd.github.v3+json'
                        }
                        
                        data = {
                            'message': f'Add image: {filename}',
                            'content': base64.b64encode(image_data).decode('utf-8'),
                            'branch': self.github_branch
                        }
                        
                        async with session.put(github_url, headers=headers, json=data) as upload_response:
                            if upload_response.status in [200, 201]:
                                logger.info(f"Image uploaded to GitHub: {filename}")
                                return f"/assets/images/{filename}"
                            else:
                                logger.error(f"GitHub upload failed: {upload_response.status}")
            
        except Exception as e:
            logger.error(f"Error uploading image to GitHub: {e}")
        
        return None
    
    async def create_article_outline(self, keyword: str, title: str) -> Dict:
        """Create structured article outline"""
        outline_prompt = f"""
        Create a comprehensive article outline for "{title}" targeting "{keyword}".
        
        Return JSON format:
        {{
            "keyword_analysis": {{
                "search_intent": "informational/commercial/navigational",
                "target_audience": "target readers description",
                "main_topics": ["topic1", "topic2", "topic3"]
            }},
            "structure": {{
                "introduction": {{
                    "hook": "engaging opening",
                    "overview": "article coverage",
                    "value": "reader benefits"
                }},
                "sections": [
                    {{
                        "heading": "H2 heading",
                        "content_points": ["point1", "point2"],
                        "needs_image": true/false
                    }}
                ],
                "conclusion": {{
                    "summary": "key takeaways",
                    "action": "next steps"
                }}
            }},
            "seo": {{
                "meta_description": "compelling description",
                "keywords": ["primary", "secondary"],
                "estimated_length": 1500
            }}
        }}
        
        Return only valid JSON.
        """
        
        response = await self.generate_with_gemini(outline_prompt, 'gemini-1.5-pro')
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error("Failed to parse outline JSON")
            return {}
    
    async def generate_article_content(self, outline: Dict, keyword: str, title: str) -> str:
        """Generate complete article content based on outline"""
        try:
            content_prompt = f"""
            Write a comprehensive article titled "{title}" for the keyword "{keyword}".
            
            Follow this structure: {json.dumps(outline.get('structure', {}), indent=2)}
            Target audience: {outline.get('keyword_analysis', {}).get('target_audience', 'general readers')}
            
            Requirements:
            - 1200-1500 words total
            - Professional, engaging tone
            - Use proper markdown formatting
            - Include practical examples
            - Natural keyword integration (3-5 times)
            - Add bullet points and lists where appropriate
            - Include clear H2 and H3 headings
            
            Write the complete article in markdown format.
            """
            
            content = await self.generate_with_gemini(content_prompt, 'gemini-1.5-pro')
            return content.strip() if content else ""
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return ""
    
    async def save_article_to_github(self, article: Dict) -> bool:
        """Save article directly to GitHub repository"""
        if not self.github_token or not self.github_repo:
            logger.error("GitHub configuration missing")
            return False
        
        try:
            # Create filename
            date_str = datetime.datetime.now().strftime('%Y-%m-%d')
            filename = f"{date_str}-{article['slug']}.md"
            github_path = f"_posts/{filename}"
            
            # Create post content with frontmatter
            post = frontmatter.Post(
                article['content'],
                **article['frontmatter']
            )
            post_content = frontmatter.dumps(post)
            
            # Upload to GitHub
            github_url = f"https://api.github.com/repos/{self.github_repo}/contents/{github_path}"
            
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            data = {
                'message': f'Add new article: {article["title"]}',
                'content': base64.b64encode(post_content.encode('utf-8')).decode('utf-8'),
                'branch': self.github_branch
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.put(github_url, headers=headers, json=data) as response:
                    if response.status in [200, 201]:
                        logger.info(f"Article saved to GitHub: {filename}")
                        return True
                    else:
                        logger.error(f"GitHub save failed: {response.status}")
                        error_text = await response.text()
                        logger.error(f"Error details: {error_text}")
                        return False
        
        except Exception as e:
            logger.error(f"Error saving to GitHub: {e}")
            return False
    
    async def generate_complete_article(self, keyword: str) -> Optional[Dict]:
        """Generate a complete article optimized for serverless execution"""
        try:
            logger.info(f"Starting article generation for: {keyword}")
            
            # Generate title
            title_prompt = f"""
            Create an SEO-optimized, engaging title for "{keyword}".
            Requirements: Under 60 characters, includes keyword, professional, click-worthy.
            Return only the title.
            """
            
            title = await self.generate_with_gemini(title_prompt)
            if not title:
                return None
            
            logger.info(f"Generated title: {title}")
            
            # Create outline
            outline = await self.create_article_outline(keyword, title)
            if not outline:
                return None
            
            # Generate content
            content = await self.generate_article_content(outline, keyword, title)
            if not content:
                return None
            
            # Handle images
            featured_image = ""
            sections_with_images = [s for s in outline.get('structure', {}).get('sections', []) 
                                  if s.get('needs_image', False)]
            
            if sections_with_images:
                image_query = f"{keyword} interior design"
                image_urls = await self.search_images_optimized(image_query, 1)
                
                if image_urls:
                    filename = f"{slugify(keyword)}-featured.jpg"
                    uploaded_path = await self.upload_image_to_github(image_urls[0], filename)
                    if uploaded_path:
                        featured_image = uploaded_path
            
            # Create article data
            article_slug = slugify(title)
            article_date = datetime.datetime.now()
            
            seo_data = outline.get('seo', {})
            
            frontmatter_data = {
                'layout': 'post',
                'title': title,
                'description': seo_data.get('meta_description', title),
                'date': article_date.strftime('%Y-%m-%d %H:%M:%S +0000'),
                'categories': [self.config.get('category', 'Interior Design')],
                'tags': seo_data.get('keywords', [keyword]) + keyword.split()[:2],
                'author': self.config.get('author', 'Admin'),
                'featured_image': featured_image,
                'seo': {
                    'title': title,
                    'description': seo_data.get('meta_description', title),
                    'keywords': ', '.join(seo_data.get('keywords', [keyword]))
                }
            }
            
            article = {
                'title': title,
                'slug': article_slug,
                'keyword': keyword,
                'content': content,
                'frontmatter': frontmatter_data,
                'created_at': article_date.isoformat(),
                'word_count': len(content.split()),
                'outline': outline
            }
            
            logger.info(f"Article generated successfully: {title} ({article['word_count']} words)")
            return article
            
        except Exception as e:
            logger.error(f"Error in article generation: {e}")
            return None
    
    def check_daily_limits(self) -> bool:
        """Check if generation is within daily limits"""
        today = datetime.date.today().isoformat()
        today_articles = [a for a in self.articles_data if a.get('created_at', '').startswith(today)]
        
        max_daily = self.config.get('max_daily_articles', 2)
        
        if len(today_articles) >= max_daily:
            logger.info(f"Daily article limit reached: {len(today_articles)}/{max_daily}")
            return False
        
        if self.daily_requests >= self.max_daily_requests:
            logger.info(f"API limit reached: {self.daily_requests}/{self.max_daily_requests}")
            return False
        
        return True
    
    async def run(self) -> Dict:
        """Main execution method optimized for serverless"""
        result = {
            'success': False,
            'message': '',
            'article': None,
            'stats': {
                'api_calls': self.daily_requests,
                'articles_today': 0
            }
        }
        
        try:
            logger.info("Starting CloudflareOptimizedArticleGenerator")
            
            if not self.api_keys:
                result['message'] = "No API keys available"
                return result
            
            if not self.check_daily_limits():
                result['message'] = "Daily limits reached"
                return result
            
            # Get keyword
            keyword = self.get_next_keyword()
            if not keyword:
                result['message'] = "No keywords available"
                return result
            
            # Generate article
            article = await self.generate_complete_article(keyword)
            if not article:
                result['message'] = "Failed to generate article"
                return result
            
            # Save to GitHub
            if await self.save_article_to_github(article):
                # Update tracking data
                self.articles_data.append(article)
                self.used_keywords.add(keyword)
                
                result['success'] = True
                result['message'] = f"Successfully created: {article['title']}"
                result['article'] = {
                    'title': article['title'],
                    'slug': article['slug'],
                    'keyword': keyword,
                    'word_count': article['word_count']
                }
                result['stats']['api_calls'] = self.daily_requests
                
                logger.info(f"✅ Article generation completed: {article['title']}")
            else:
                result['message'] = "Failed to save article to GitHub"
            
        except Exception as e:
            logger.error(f"Error in main execution: {e}")
            result['message'] = f"Execution error: {str(e)}"
        
        return result


# Serverless entry point
async def lambda_handler(event=None, context=None):
    """AWS Lambda / Cloudflare Workers compatible handler"""
    generator = CloudflareOptimizedArticleGenerator()
    result = await generator.run()
    
    return {
        'statusCode': 200 if result['success'] else 500,
        'body': json.dumps(result, indent=2),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

# Standard execution
async def main():
    """Standard async main for direct execution"""
    generator = CloudflareOptimizedArticleGenerator()
    result = await generator.run()
    
    print(json.dumps(result, indent=2))
    
    if result['success']:
        print("✅ Article generation completed successfully!")
        return 0
    else:
        print(f"❌ Article generation failed: {result['message']}")
        return 1

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)