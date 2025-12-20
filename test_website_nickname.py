#!/usr/bin/env python3
"""
Test script for website nickname functionality
"""

from db_manager import DatabaseManager
from urllib.parse import urlparse
import os

def get_website_nickname_from_url(url: str) -> str:
    """Extract a default website nickname from URL."""
    parsed = urlparse(url)
    domain = parsed.netloc
    # Remove www. prefix and common TLDs for cleaner names
    if domain.startswith('www.'):
        domain = domain[4:]
    # Capitalize first letter for better presentation
    return domain.replace('.', ' ').title()

def test_website_nickname_features():
    """Test the website nickname features"""
    print("Testing Website Nickname Features")
    print("=" * 50)
    
    # Test 1: URL to nickname conversion
    print("1. Testing URL to nickname conversion...")
    test_urls = [
        "https://www.bbc.com/news",
        "https://techcrunch.com",
        "https://news.ycombinator.com",
        "https://www.reddit.com/r/python"
    ]
    
    for url in test_urls:
        nickname = get_website_nickname_from_url(url)
        print(f"  {url} -> '{nickname}'")
    
    # Test 2: Database operations with website nickname
    print("\n2. Testing database operations...")
    test_db = "test_nickname.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = DatabaseManager(test_db)
    
    # Save feeds with website nicknames
    feed_id1 = db.save_feed(
        "https://techcrunch.com",
        "https://techcrunch.com/rss",
        "Main RSS Feed",
        "Tech News Hub",
        is_synthetic=False
    )
    
    feed_id2 = db.save_feed(
        "https://techcrunch.com",
        "https://techcrunch.com/startups/rss",
        "Startups Feed",
        "Tech News Hub",
        is_synthetic=False
    )
    
    feed_id3 = db.save_feed(
        "https://bbc.com",
        "https://bbc.com/news/rss",
        "BBC News Feed",
        "BBC News",
        is_synthetic=False
    )
    
    print(f"✓ Saved feeds with IDs: {feed_id1}, {feed_id2}, {feed_id3}")
    
    # Test 3: Grouped feeds retrieval
    print("\n3. Testing grouped feeds retrieval...")
    grouped_feeds = db.get_feeds_grouped_by_website()
    
    for website_nickname, feeds in grouped_feeds.items():
        print(f"  Website: '{website_nickname}' ({len(feeds)} feeds)")
        for feed in feeds:
            print(f"    - {feed['user_given_name']}: {feed['feed_url']}")
    
    # Test 4: Site URL retrieval
    print("\n4. Testing site URL retrieval...")
    site_feeds = db.get_feeds_by_site_url("https://techcrunch.com")
    print(f"✓ Found {len(site_feeds)} feeds for techcrunch.com")
    
    for feed in site_feeds:
        print(f"  - {feed['user_given_name']} (Website: {feed['website_nickname']})")
    
    # Cleanup
    os.remove(test_db)
    print("\n✓ All website nickname features test completed successfully!")

if __name__ == "__main__":
    test_website_nickname_features()