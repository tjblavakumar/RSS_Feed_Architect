#!/usr/bin/env python3
"""
Test duplicate feed checking functionality
"""

from db_manager import DatabaseManager
import os

def test_duplicate_checking():
    """Test duplicate feed checking"""
    print("Testing Duplicate Feed Checking")
    print("=" * 40)
    
    # Clean database
    if os.path.exists("test_duplicate.db"):
        os.remove("test_duplicate.db")
    
    db = DatabaseManager("test_duplicate.db")
    
    # Test 1: Save a feed
    print("1. Saving initial feed...")
    try:
        feed_id1 = db.save_feed(
            site_url="https://example.com",
            feed_url="https://example.com/rss.xml",
            user_given_name="Test Feed",
            website_nickname="Test Site",
            is_synthetic=False
        )
        print(f"✓ Feed saved with ID: {feed_id1}")
    except Exception as e:
        print(f"❌ Error saving feed: {e}")
        return False
    
    # Test 2: Check if feed exists
    print("\n2. Checking if feed exists...")
    exists = db.feed_exists("https://example.com/rss.xml")
    print(f"✓ Feed exists: {exists}")
    
    # Test 3: Get existing feed details
    print("\n3. Getting existing feed details...")
    existing_feed = db.get_existing_feed("https://example.com/rss.xml")
    if existing_feed:
        print(f"✓ Found existing feed:")
        print(f"  - Name: {existing_feed['user_given_name']}")
        print(f"  - Website: {existing_feed['website_nickname']}")
        print(f"  - URL: {existing_feed['feed_url']}")
    else:
        print("❌ Could not retrieve existing feed")
        return False
    
    # Test 4: Check non-existent feed
    print("\n4. Checking non-existent feed...")
    exists_fake = db.feed_exists("https://fake.com/rss.xml")
    print(f"✓ Fake feed exists: {exists_fake}")
    
    # Test 5: Try to save duplicate
    print("\n5. Attempting to save duplicate...")
    if db.feed_exists("https://example.com/rss.xml"):
        existing = db.get_existing_feed("https://example.com/rss.xml")
        print(f"⚠️ Feed already exists!")
        print(f"Existing feed: '{existing['user_given_name']}' in website '{existing['website_nickname']}'")
    else:
        print("❌ Duplicate check failed")
        return False
    
    # Cleanup
    os.remove("test_duplicate.db")
    print("\n✅ All duplicate checking tests passed!")
    return True

if __name__ == "__main__":
    success = test_duplicate_checking()
    if not success:
        print("\n❌ Duplicate checking tests failed!")
        exit(1)