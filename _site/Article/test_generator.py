#!/usr/bin/env python3
"""
Test script untuk memverifikasi generator artikel berfungsi dengan benar
"""

import os
import sys
import json
from pathlib import Path

def test_environment():
    """Test environment dan dependencies"""
    print("🔍 Testing environment...")
    
    # Test Python version
    print(f"Python version: {sys.version}")
    
    # Test required modules
    required_modules = [
        'google.generativeai',
        'requests',
        'markdown', 
        'frontmatter',
        'yaml',
        'slugify',
        'langdetect',
        'aiohttp',
        'aiofiles',
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError:
            print(f"❌ {module} - MISSING")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  Missing modules: {', '.join(missing_modules)}")
        return False
    
    return True

def test_files():
    """Test file requirements"""
    print("\n🔍 Testing required files...")
    
    required_files = [
        'UpdateArticle.py',
        'requirements.txt', 
        'keyword.txt',
        'apikey.txt'
    ]
    
    missing_files = []
    for filename in required_files:
        filepath = Path(__file__).parent / filename
        if filepath.exists():
            print(f"✅ {filename} - OK")
        else:
            print(f"❌ {filename} - MISSING")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def test_keywords():
    """Test keyword file"""
    print("\n🔍 Testing keywords...")
    
    keyword_file = Path(__file__).parent / 'keyword.txt'
    try:
        with open(keyword_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        keywords = [
            line.strip() for line in content.splitlines()
            if line.strip() and not line.startswith('#')
        ]
        
        print(f"✅ Found {len(keywords)} keywords")
        if keywords:
            print(f"📝 Sample keywords: {', '.join(keywords[:3])}")
        
        return len(keywords) > 0
        
    except Exception as e:
        print(f"❌ Error reading keywords: {e}")
        return False

def test_api_keys():
    """Test API keys"""
    print("\n🔍 Testing API keys...")
    
    api_file = Path(__file__).parent / 'apikey.txt'
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        keys = [line.strip() for line in content.splitlines() if line.strip()]
        print(f"✅ Found {len(keys)} API keys")
        
        return len(keys) > 0
        
    except Exception as e:
        print(f"❌ Error reading API keys: {e}")
        return False

def test_output_directory():
    """Test output directory structure"""
    print("\n🔍 Testing output directories...")
    
    # Check _posts directory
    posts_dir = Path(__file__).parent.parent / '_posts'
    if posts_dir.exists():
        print(f"✅ _posts directory exists")
        posts_count = len(list(posts_dir.glob('*.md')))
        print(f"📄 Current posts: {posts_count}")
    else:
        print(f"⚠️  _posts directory not found")
    
    # Check assets/images directory
    images_dir = Path(__file__).parent.parent / 'assets' / 'images'
    if images_dir.exists():
        print(f"✅ assets/images directory exists")
    else:
        print(f"⚠️  assets/images directory not found")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Article Generator Test\n")
    
    tests = [
        ("Environment", test_environment),
        ("Files", test_files), 
        ("Keywords", test_keywords),
        ("API Keys", test_api_keys),
        ("Output Directories", test_output_directory)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Article generator is ready.")
        return True
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)