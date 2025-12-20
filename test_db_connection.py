#!/usr/bin/env python3
"""
Test database connection and operations
"""

from db_manager import DatabaseManager
import os

def test_db_operations():
    """Test basic database operations"""
    print("Testing Database Operations")
    print("=" * 40)
    
    # Test with default database name
    print("1. Testing with default database...")
    try:
        db = DatabaseManager()
        print("✓ Database manager created successfully")
        
        # Test saving a feed
        feed_id = db.save_feed(
            "https://test.com",
            "https://test.com/rss.xml",
            "Test Feed",
            "Test Website",
            is_synthetic=False
        )
        print(f"✓ Feed saved with ID: {feed_id}")
        
        # Test retrieving feeds
        feeds = db.get_all_feeds()
        print(f"✓ Retrieved {len(feeds)} feeds")
        
        # Test grouped retrieval
        grouped = db.get_feeds_grouped_by_website()
        print(f"✓ Grouped feeds: {len(grouped)} websites")
        
        for website, feed_list in grouped.items():
            print(f"  - {website}: {len(feed_list)} feeds")
        
        print("✓ All database operations successful!")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return False

def test_db_schema():
    """Test database schema"""
    print("\n2. Testing database schema...")
    try:
        db = DatabaseManager("test_schema.db")
        
        # Check if we can save with all required fields
        feed_id = db.save_feed(
            site_url="https://example.com",
            feed_url="https://example.com/rss.xml", 
            user_given_name="Example Feed",
            website_nickname="Example Site",
            is_synthetic=False
        )
        
        print(f"✓ Schema test successful, feed ID: {feed_id}")
        
        # Clean up
        if os.path.exists("test_schema.db"):
            os.remove("test_schema.db")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema error: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success1 = test_db_operations()
    success2 = test_db_schema()
    
    if success1 and success2:
        print("\n🎉 All database tests passed!")
    else:
        print("\n❌ Some database tests failed!")
        exit(1)