#!/usr/bin/env python3
"""
Debug script to test the save functionality
"""

from db_manager import DatabaseManager
import os

def test_multiple_feed_saves():
    """Test saving multiple feeds with the same website nickname"""
    print("Testing Multiple Feed Save Functionality")
    print("=" * 50)
    
    # Create test database
    test_db = "test_multiple_saves.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = DatabaseManager(test_db)
    
    # Test saving multiple feeds for the same website
    website_nickname = "Test News Site"
    site_url = "https://example.com"
    
    print(f"Saving feeds for website nickname: '{website_nickname}'")
    print(f"Site URL: {site_url}")
    
    # Save first feed
    print("\n1. Saving first feed...")
    try:
        feed_id1 = db.save_feed(
            site_url,
            "https://example.com/rss1.xml",
            "First RSS Feed",
            website_nickname,
            is_synthetic=False
        )
        print(f"✓ First feed saved with ID: {feed_id1}")
    except Exception as e:
        print(f"❌ Error saving first feed: {e}")
        return False
    
    # Save second feed
    print("\n2. Saving second feed...")
    try:
        feed_id2 = db.save_feed(
            site_url,
            "https://example.com/rss2.xml",
            "Second RSS Feed",
            website_nickname,
            is_synthetic=False
        )
        print(f"✓ Second feed saved with ID: {feed_id2}")
    except Exception as e:
        print(f"❌ Error saving second feed: {e}")
        return False
    
    # Save third feed
    print("\n3. Saving third feed...")
    try:
        feed_id3 = db.save_feed(
            site_url,
            "https://example.com/rss3.xml",
            "Third RSS Feed",
            website_nickname,
            is_synthetic=True
        )
        print(f"✓ Third feed saved with ID: {feed_id3}")
    except Exception as e:
        print(f"❌ Error saving third feed: {e}")
        return False
    
    # Verify all feeds are saved
    print("\n4. Verifying saved feeds...")
    all_feeds = db.get_all_feeds()
    print(f"Total feeds in database: {len(all_feeds)}")
    
    for feed in all_feeds:
        print(f"  - ID: {feed['id']}, Name: {feed['user_given_name']}, Website: {feed['website_nickname']}")
    
    # Test grouped retrieval
    print("\n5. Testing grouped retrieval...")
    grouped_feeds = db.get_feeds_grouped_by_website()
    
    for website_nick, feeds in grouped_feeds.items():
        print(f"Website: '{website_nick}' ({len(feeds)} feeds)")
        for feed in feeds:
            print(f"  - {feed['user_given_name']}: {feed['feed_url']}")
    
    # Test site URL retrieval
    print("\n6. Testing site URL retrieval...")
    site_feeds = db.get_feeds_by_site_url(site_url)
    print(f"Feeds for {site_url}: {len(site_feeds)}")
    
    for feed in site_feeds:
        print(f"  - {feed['user_given_name']} (Website: {feed['website_nickname']})")
    
    # Cleanup
    os.remove(test_db)
    
    print("\n✅ Multiple feed save test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_multiple_feed_saves()
    if not success:
        print("\n❌ Test failed!")
        exit(1)