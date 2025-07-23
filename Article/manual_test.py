#!/usr/bin/env python3
"""
Manual test untuk menjalankan generator artikel sekali
"""

import asyncio
import sys
import os
from pathlib import Path
from UpdateArticle import CloudflareOptimizedArticleGenerator

async def main():
    print("🚀 Starting manual article generation test...\n")
    
    # Initialize generator
    print("Initializing generator...")
    generator = CloudflareOptimizedArticleGenerator()
    
    # Load API keys from file
    api_file = Path(__file__).parent / 'apikey.txt'
    if api_file.exists():
        with open(api_file, 'r') as f:
            keys = [line.strip() for line in f.readlines() if line.strip()]
        generator.api_keys = keys
        print(f"✅ Loaded {len(keys)} API keys")
    else:
        print("❌ No apikey.txt file found")
        return
    
    # Get keywords
    keywords = generator.get_keywords_from_env()
    if not keywords:
        print("❌ No keywords found")
        return
    
    print(f"✅ Loaded {len(keywords)} keywords")
    
    # Select test keyword
    test_keyword = "modern living room design"
    print(f"📝 Testing with keyword: {test_keyword}")
    
    # Test title generation
    print("\n1. Testing title generation...")
    title_prompt = f"""
    Create an engaging, SEO-optimized title for an article about "{test_keyword}".
    
    Requirements:
    - 50-60 characters
    - Include the keyword naturally
    - Make it compelling and clickable
    - Target home design enthusiasts
    
    Return only the title, no quotes or additional text.
    """
    
    try:
        title = await generator.generate_with_gemini(title_prompt)
        print(f"✅ Generated title: {title}")
    except Exception as e:
        print(f"❌ Title generation failed: {e}")
        return
    
    # Test outline creation
    print("\n2. Testing outline creation...")
    try:
        outline = await generator.create_article_outline(test_keyword, title)
        if outline:
            print("✅ Article outline created successfully")
            print(f"   Sections: {len(outline.get('structure', {}).get('sections', []))}")
        else:
            print("❌ Outline creation failed")
            return
    except Exception as e:
        print(f"❌ Outline creation failed: {e}")
        return
    
    # Test image search
    print("\n3. Testing image search...")
    try:
        images = await generator.search_images_optimized(test_keyword, 2)
        print(f"✅ Found {len(images)} images")
        for i, img in enumerate(images):
            print(f"   Image {i+1}: {img[:50]}...")
    except Exception as e:
        print(f"❌ Image search failed: {e}")
    
    print("\n🎉 Manual test completed successfully!")
    print("\nThe generator components are working properly.")
    print("Ready for full article generation workflow.")

if __name__ == "__main__":
    asyncio.run(main())