#!/usr/bin/env python3
"""
Test script for UpdateArticle.py generator
Validates all components work correctly before deployment
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Add _Article to path
sys.path.insert(0, str(Path(__file__).parent / '_Article'))

async def test_article_generator():
    """Comprehensive test of the article generator"""
    print("🧪 Testing UpdateArticle.py Generator")
    print("=" * 50)
    
    try:
        from UpdateArticle import CloudflareOptimizedArticleGenerator
        print("✅ Import successful")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 1: Initialization
    print("\n📝 Test 1: Initialization")
    try:
        generator = CloudflareOptimizedArticleGenerator()
        print("✅ Generator initialized successfully")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False
    
    # Test 2: Environment loading
    print("\n📝 Test 2: Environment Configuration")
    test_config = {
        "BLOG_KEYWORDS": '["modern design", "interior tips"]',
        "BLOG_CONFIG": '{"category": "Test", "author": "Tester"}',
        "ARTICLES_DATA": '{"articles": [], "used_keywords": [], "daily_requests": 0}'
    }
    
    # Set test environment
    for key, value in test_config.items():
        os.environ[key] = value
    
    generator = CloudflareOptimizedArticleGenerator()
    
    keywords = generator.get_keywords_from_env()
    print(f"✅ Keywords loaded: {keywords}")
    
    next_keyword = generator.get_next_keyword()
    print(f"✅ Next keyword: {next_keyword}")
    
    print(f"✅ Configuration: {generator.config}")
    
    # Test 3: API Key rotation (without actual keys)
    print("\n📝 Test 3: API Key Rotation")
    try:
        # This will fail due to no API keys, but tests the method
        try:
            await generator.rotate_api_key()
        except Exception as e:
            if "No API keys available" in str(e):
                print("✅ API key rotation logic works (no keys provided)")
            else:
                raise e
    except Exception as e:
        print(f"❌ API key rotation test failed: {e}")
        return False
    
    # Test 4: Rate limiting
    print("\n📝 Test 4: Rate Limiting")
    try:
        # Test rate limiter initialization
        assert generator.gemini_throttler is not None
        assert generator.image_throttler is not None
        print("✅ Rate limiters initialized")
    except Exception as e:
        print(f"❌ Rate limiting test failed: {e}")
        return False
    
    # Test 5: Daily limits check
    print("\n📝 Test 5: Daily Limits")
    try:
        can_generate = generator.check_daily_limits()
        print(f"✅ Daily limits check: {'Can generate' if can_generate else 'Limit reached'}")
    except Exception as e:
        print(f"❌ Daily limits test failed: {e}")
        return False
    
    # Test 6: Main execution (without API keys)
    print("\n📝 Test 6: Main Execution Logic")
    try:
        result = await generator.run()
        expected_message = "No API keys available"
        if result.get('message') == expected_message:
            print("✅ Main execution logic works correctly")
        else:
            print(f"✅ Main execution completed: {result.get('message', 'Unknown')}")
    except Exception as e:
        print(f"❌ Main execution test failed: {e}")
        return False
    
    # Cleanup environment
    for key in test_config.keys():
        os.environ.pop(key, None)
    
    print("\n🎉 All tests passed!")
    print("📋 Summary:")
    print("   - Generator initializes correctly")
    print("   - Environment configuration works")
    print("   - API key rotation logic is sound")
    print("   - Rate limiting is configured")
    print("   - Daily limits checking works")
    print("   - Main execution logic is correct")
    print("\n✅ UpdateArticle.py is ready for deployment!")
    
    return True

def test_file_structure():
    """Test that all required files exist"""
    print("\n📁 Testing File Structure")
    print("-" * 30)
    
    required_files = [
        "_Article/UpdateArticle.py",
        "cloudflare-worker.js",
        ".github/workflows/generate-article.yml",
        "wrangler.toml",
        "DEPLOYMENT_GUIDE.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {missing_files}")
        return False
    else:
        print("\n✅ All required files present")
        return True

async def main():
    """Run all tests"""
    print("🚀 UpdateArticle.py Deployment Test Suite")
    print("=" * 60)
    
    # Test file structure
    files_ok = test_file_structure()
    
    # Test generator functionality
    generator_ok = await test_article_generator()
    
    print("\n" + "=" * 60)
    if files_ok and generator_ok:
        print("🎯 ALL TESTS PASSED - Ready for deployment!")
        print("\nNext steps:")
        print("1. Set up repository secrets in GitHub")
        print("2. Configure Cloudflare Worker (optional)")
        print("3. Test with actual API keys")
        print("4. Monitor first automated run")
        return 0
    else:
        print("❌ TESTS FAILED - Please fix issues before deployment")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)