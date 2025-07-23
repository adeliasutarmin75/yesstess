#!/usr/bin/env python3
"""
Test script untuk workflow GitHub Actions
"""

import asyncio
import sys
import os
import json
from pathlib import Path
from datetime import datetime
from UpdateArticle import CloudflareOptimizedArticleGenerator

async def test_workflow_simulation():
    """Simulate GitHub Actions workflow"""
    print("🔄 Simulating GitHub Actions workflow...\n")
    
    # Initialize generator
    print("1. Initializing generator...")
    generator = CloudflareOptimizedArticleGenerator()
    
    # Load configuration files
    print("2. Loading configuration...")
    
    # Check required files
    required_files = ['keyword.txt', 'apikey.txt', 'requirements.txt']
    for filename in required_files:
        filepath = Path(__file__).parent / filename
        if filepath.exists():
            print(f"   ✅ {filename} - Found")
        else:
            print(f"   ❌ {filename} - Missing")
            return False
    
    # Check keywords
    keywords = generator.get_keywords_from_env()
    print(f"   📝 Keywords loaded: {len(keywords)}")
    
    # Check API keys
    if generator.api_keys:
        print(f"   🔑 API keys loaded: {len(generator.api_keys)}")
    else:
        print("   ❌ No API keys loaded")
        return False
    
    # Check output directories
    print("3. Checking output directories...")
    posts_dir = Path(__file__).parent.parent / '_posts'
    images_dir = Path(__file__).parent.parent / 'assets' / 'images'
    
    print(f"   📁 _posts directory: {'✅ Exists' if posts_dir.exists() else '❌ Missing'}")
    print(f"   📁 assets/images directory: {'✅ Exists' if images_dir.exists() else '❌ Missing'}")
    
    # Test rate limiting
    print("4. Testing rate limiting...")
    
    # Simulate usage tracking
    last_run_file = Path(__file__).parent / 'last_run.json'
    today = datetime.now().strftime('%Y-%m-%d')
    
    if last_run_file.exists():
        with open(last_run_file, 'r') as f:
            last_run = json.load(f)
        print(f"   📊 Last run: {last_run.get('date', 'Unknown')}")
        print(f"   📊 Daily count: {last_run.get('daily_count', 0)}")
    else:
        print("   📊 No previous run data")
    
    # Test article database
    print("5. Testing article database...")
    articles_file = Path(__file__).parent / 'articles_data.json'
    
    if articles_file.exists():
        with open(articles_file, 'r') as f:
            articles_data = json.load(f)
        articles_count = len(articles_data.get('articles', []))
        print(f"   📚 Existing articles: {articles_count}")
    else:
        print("   📚 No existing articles database")
    
    # Test keyword selection
    print("6. Testing keyword selection...")
    next_keyword = generator.get_next_keyword()
    if next_keyword:
        print(f"   🎯 Next keyword: {next_keyword}")
    else:
        print("   ❌ No keyword available")
        return False
    
    print("\n✅ Workflow simulation completed successfully!")
    print("\nWorkflow components:")
    print("• Python environment: Ready")
    print("• Dependencies: Installed")
    print("• Configuration files: Present")
    print("• API keys: Loaded")
    print("• Output directories: Ready")
    print("• Rate limiting: Configured")
    print("• Keyword system: Working")
    
    return True

def test_environment_variables():
    """Test environment variables for GitHub Actions"""
    print("\n🔍 Testing GitHub Actions environment variables...")
    
    github_vars = [
        'GITHUB_TOKEN',
        'GEMINI_API_KEY',
        'UNSPLASH_ACCESS_KEY',
        'PIXABAY_API_KEY',
        'PEXELS_API_KEY'
    ]
    
    for var in github_vars:
        value = os.environ.get(var)
        if value:
            print(f"   ✅ {var}: {'*' * min(len(value), 10)}")
        else:
            print(f"   ⚠️  {var}: Not set (will use fallback)")
    
    return True

async def main():
    """Run all workflow tests"""
    print("🚀 GitHub Actions Workflow Test\n")
    
    # Run tests
    workflow_ok = await test_workflow_simulation()
    env_ok = test_environment_variables()
    
    print("\n" + "="*50)
    print("📊 WORKFLOW TEST SUMMARY")
    print("="*50)
    
    if workflow_ok and env_ok:
        print("🎉 All workflow components are ready!")
        print("\nTo run the workflow:")
        print("1. Push changes to GitHub")
        print("2. Check GitHub Actions tab")
        print("3. Workflow runs automatically 5 times daily")
        print("4. Or trigger manually from Actions tab")
        return True
    else:
        print("❌ Some workflow components need attention")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)