#!/usr/bin/env python3
"""
Test the simple app functionality
"""

from db_manager import DatabaseManager
import os

def test_simple_save():
    """Test simple save functionality"""
    print("Testing Simple Save Functionality")
    print("=" * 40)
    
    # Clean database
    if os.path.exists("feed_storage.db"):
        os.remove("feed_storage.db")
    
    db = DatabaseManager()
    
    # Test save
    try:
        feed_id = db.save_feed(
            site_url="https://example.com",
            feed_url="https://example.com/rss.xml",
            user_given_name="Test Feed",
            website_nickname="Test Site",
            is_synthetic=False
        )
        print(f"✓ Feed saved with ID: {feed_id}")
        
        # Verify save
        feeds = db.get_all_feeds()
        print(f"✓ Total feeds in DB: {len(feeds)}")
        
        if feeds:
            feed = feeds[0]
            print(f"✓ Saved feed details:")
            print(f"  - Name: {feed['user_given_name']}")
            print(f"  - URL: {feed['feed_url']}")
            print(f"  - Website: {feed['website_nickname']}")
            print(f"  - Type: {'Synthetic' if feed['is_synthetic'] else 'Discovered'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_simple_save()
    if success:
        print("\n🎉 Simple save test passed!")
    else:
        print("\n❌ Simple save test failed!")
        exit(1)