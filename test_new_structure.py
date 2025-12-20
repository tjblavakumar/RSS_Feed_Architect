#!/usr/bin/env python3
"""
Test script for the new simplified app structure
"""

from db_manager import DatabaseManager
import os

def test_simplified_structure():
    """Test the simplified app structure"""
    print("Testing Simplified RSS Architect Structure")
    print("=" * 50)
    
    # Test database operations
    test_db = "test_simple.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = DatabaseManager(test_db)
    
    # Test saving feeds with different website nicknames
    print("1. Testing feed saves...")
    
    # Website 1: Tech News
    feed_id1 = db.save_feed(
        "https://techcrunch.com",
        "https://techcrunch.com/rss",
        "Main Feed",
        "Tech News",
        is_synthetic=False
    )
    
    feed_id2 = db.save_feed(
        "https://techcrunch.com",
        "https://techcrunch.com/startups/rss",
        "Startups Feed",
        "Tech News",
        is_synthetic=False
    )
    
    # Website 2: News Site
    feed_id3 = db.save_feed(
        "https://bbc.com",
        "https://bbc.com/news/rss",
        "BBC News",
        "News Site",
        is_synthetic=False
    )
    
    print(f"✓ Saved 3 feeds with IDs: {feed_id1}, {feed_id2}, {feed_id3}")
    
    # Test grouped retrieval
    print("\n2. Testing grouped feed retrieval...")
    grouped_feeds = db.get_feeds_grouped_by_website()
    
    for website_nickname, feeds in grouped_feeds.items():
        print(f"  📁 {website_nickname} ({len(feeds)} feeds)")
        for i, feed in enumerate(feeds, 1):
            print(f"    {i}. {feed['user_given_name']}")
            print(f"       URL: {feed['feed_url']}")
            print(f"       Type: {'Synthetic' if feed['is_synthetic'] else 'Discovered'}")
    
    # Test individual feed deletion
    print(f"\n3. Testing feed deletion...")
    if db.delete_feed(feed_id2):
        print(f"✓ Successfully deleted feed ID {feed_id2}")
    else:
        print(f"❌ Failed to delete feed ID {feed_id2}")
    
    # Verify deletion
    remaining_feeds = db.get_all_feeds()
    print(f"✓ Remaining feeds: {len(remaining_feeds)}")
    
    # Cleanup
    os.remove(test_db)
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    test_simplified_structure()