#!/usr/bin/env python3
"""
Test RSS discovery with the US News RSS feeds page
"""

from rss_discovery import RSSDiscovery

def test_usnews_rss_discovery():
    """Test RSS discovery on US News RSS feeds page"""
    print("Testing RSS Discovery on US News RSS Feeds Page")
    print("=" * 60)
    
    discovery = RSSDiscovery()
    
    # Test with the US News RSS feeds page
    url = "https://www.usnews.com/info/features/rss-feeds"
    
    print(f"Testing URL: {url}")
    print("Scanning for RSS feeds...")
    
    try:
        result = discovery.find_rss_feeds(url)
        
        print(f"\nResults:")
        print(f"- Error: {result.get('error')}")
        print(f"- Paywall: {result.get('is_paywall')}")
        print(f"- Feeds found: {len(result.get('feeds', []))}")
        
        if result.get('feeds'):
            print(f"\nDiscovered RSS Feeds:")
            for i, feed in enumerate(result['feeds'], 1):
                print(f"{i}. {feed['title']}")
                print(f"   URL: {feed['url']}")
                print(f"   Type: {feed['type']}")
                print()
        else:
            print("\nNo RSS feeds found.")
            
            # Let's also test the individual methods
            print("\nTesting individual methods...")
            soup = discovery.fetch_page(url)
            if soup:
                print("✓ Page fetched successfully")
                
                # Test content RSS discovery
                content_feeds = discovery.find_rss_links_in_content(soup, url)
                print(f"✓ Content RSS discovery found: {len(content_feeds)} feeds")
                
                for feed in content_feeds[:5]:  # Show first 5
                    print(f"  - {feed['title']}: {feed['url']}")
            else:
                print("❌ Failed to fetch page")
        
        return len(result.get('feeds', []))
        
    except Exception as e:
        print(f"❌ Error during discovery: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return 0

def test_rss_url_detection():
    """Test RSS URL detection logic"""
    print("\nTesting RSS URL Detection Logic")
    print("=" * 40)
    
    discovery = RSSDiscovery()
    
    test_urls = [
        "https://www.usnews.com/rss/news",
        "https://example.com/feed.xml",
        "https://site.com/feeds/all.rss",
        "https://blog.com/atom.xml",
        "https://news.com/rss/",
        "https://regular-page.com/about",
        "https://site.com/feed/",
        "https://example.com/index.php?format=rss"
    ]
    
    for url in test_urls:
        is_rss = discovery.is_rss_url(url)
        print(f"{'✓' if is_rss else '✗'} {url}")
    
    print("\n✅ RSS URL detection test completed")

if __name__ == "__main__":
    feeds_found = test_usnews_rss_discovery()
    test_rss_url_detection()
    
    if feeds_found > 0:
        print(f"\n🎉 Success! Found {feeds_found} RSS feeds on US News page!")
    else:
        print(f"\n⚠️ No feeds found. The page might have changed or need further enhancement.")