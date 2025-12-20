#!/usr/bin/env python3
"""
Basic test script for RSS Architect components
"""

from db_manager import DatabaseManager
from rss_discovery import RSSDiscovery
from synthetic_rss import SyntheticRSSGenerator

def test_database():
    """Test database operations"""
    print("Testing database...")
    db = DatabaseManager("test_feed_storage.db")
    
    # Test saving a feed
    feed_id = db.save_feed(
        "https://example.com",
        "https://example.com/rss.xml",
        "Test Feed",
        is_synthetic=False
    )
    print(f"Saved feed with ID: {feed_id}")
    
    # Test retrieving feeds
    feeds = db.get_feeds_by_site_url("https://example.com")
    print(f"Retrieved {len(feeds)} feeds")
    
    # Test getting all feeds
    all_feeds = db.get_all_feeds()
    print(f"Total feeds in database: {len(all_feeds)}")
    
    print("Database test completed ✓")

def test_rss_discovery():
    """Test RSS discovery"""
    print("\nTesting RSS discovery...")
    discovery = RSSDiscovery()
    
    # Test with a known RSS site (BBC News)
    result = discovery.find_rss_feeds("https://www.bbc.com/news")
    print(f"Discovery result: {len(result.get('feeds', []))} feeds found")
    print(f"Paywall detected: {result.get('is_paywall', False)}")
    
    print("RSS discovery test completed ✓")

def test_synthetic_generation():
    """Test synthetic RSS generation"""
    print("\nTesting synthetic RSS generation...")
    generator = SyntheticRSSGenerator()
    
    # Mock article data
    articles = [
        {"title": "Sample Article One with More Than Five Words", "url": "https://example.com/article1"},
        {"title": "Another Sample Article Title That Is Long Enough", "url": "https://example.com/article2"}
    ]
    
    rss_path = generator.generate_rss_feed("https://example.com", articles)
    if rss_path:
        print(f"Generated RSS feed at: {rss_path}")
        print("Synthetic RSS generation test completed ✓")
    else:
        print("Failed to generate RSS feed")

if __name__ == "__main__":
    print("RSS Architect - Basic Component Tests")
    print("=" * 40)
    
    try:
        test_database()
        test_rss_discovery()
        test_synthetic_generation()
        print("\n🎉 All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()