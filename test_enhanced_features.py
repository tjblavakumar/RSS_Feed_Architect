#!/usr/bin/env python3
"""
Test script for enhanced features
"""

from db_manager import DatabaseManager
import os

def test_enhanced_workflow():
    """Test the enhanced workflow features"""
    print("Testing Enhanced RSS Architect Features")
    print("=" * 50)
    
    # Create test database
    test_db = "test_enhanced.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = DatabaseManager(test_db)
    
    # Test 1: Save some feeds
    print("1. Testing feed saving...")
    feed_id1 = db.save_feed(
        "https://example.com",
        "https://example.com/rss.xml",
        "Example RSS Feed",
        is_synthetic=False
    )
    
    feed_id2 = db.save_feed(
        "https://example.com",
        "https://example.com/atom.xml",
        "Example Atom Feed",
        is_synthetic=False
    )
    
    print(f"✓ Saved feeds with IDs: {feed_id1}, {feed_id2}")
    
    # Test 2: Retrieve feeds by site URL
    print("\n2. Testing feed retrieval...")
    existing_feeds = db.get_feeds_by_site_url("https://example.com")
    print(f"✓ Retrieved {len(existing_feeds)} feeds for example.com")
    
    for feed in existing_feeds:
        print(f"  - {feed['user_given_name']}: {feed['feed_url']}")
    
    # Test 3: Test URL normalization and hashing
    print("\n3. Testing URL processing...")
    from app import normalize_url, get_url_hash
    
    test_urls = [
        "example.com",
        "https://example.com",
        "https://example.com/",
        "https://example.com/path"
    ]
    
    for url in test_urls:
        normalized = normalize_url(url)
        hash_key = get_url_hash(normalized)
        print(f"  {url} -> {normalized} (hash: {hash_key})")
    
    # Cleanup
    os.remove(test_db)
    print("\n✓ All enhanced features test completed successfully!")

if __name__ == "__main__":
    test_enhanced_workflow()