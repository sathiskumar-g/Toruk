#!/usr/bin/env python3
"""Test comment fetching"""
import json
from scrapers.reddit import RedditScraper

# Test Reddit scraper
scraper = RedditScraper()

print("🔍 Testing Reddit Comment Fetching\n")

# 1. Search for posts
print("Step 1: Searching Reddit...")
results = scraper.scrape("I wish there was a tool for AI", limit=2)
print(f"✅ Found {len(results)} posts\n")

# 2. Get comments from first post
if results:
    post = results[0]
    print(f"Step 2: Fetching comments from:")
    print(f"   Title: {post['title'][:60]}...")
    print(f"   URL: {post['url']}\n")
    
    comments = scraper.get_post_comments(post['url'], limit=5)
    
    print(f"✅ Found {len(comments)} comments\n")
    
    if comments:
        print("Sample comments:")
        for i, comment in enumerate(comments[:3], 1):
            print(f"\n{i}. Author: {comment['author']}")
            print(f"   Points: {comment['points']}")
            print(f"   Text: {comment['text'][:100]}...")
    
    # 3. Show full structure
    print("\n" + "="*60)
    print("Full Post Structure with Comments:")
    print("="*60)
    post['top_comments'] = comments
    print(json.dumps(post, indent=2)[:500] + "...")
else:
    print("❌ No results found")
