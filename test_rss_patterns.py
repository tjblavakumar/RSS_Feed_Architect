#!/usr/bin/env python3
"""
Test RSS discovery with common URL patterns
"""

from rss_discovery import RSSDiscovery

def test_pattern_discovery():
    """Test RSS pattern discovery on various websites"""
    print("Testing RSS Pattern Discovery")
    print("=" * 50)
    
    discovery = RSSDiscovery()
    
    # Test websites that likely have RSS feeds
    test_sites = [
        "https://techcrunch.com",
        "https://www.bbc.com",
        "https://www.cnn.com",
        "https://blog.github.com",
        "https://stackoverflow.blog"
    ]
    
    for site in test_sites:
        print(f"\nTesting: {site}")
        print("-" * 40)
        
        try:
            # Test just the pattern discovery method
            pattern_feeds = discovery.try_common_rss_patterns(site)
            
            print(f"Pattern discovery found: {len(pattern_feeds)} feeds")
            
            for feed in pattern_feeds:
                print(f"  ✓ {feed['title']}")
                print(f"    URL: {feed['url']}")
            
            if not pattern_feeds:
                print("  No feeds found via patterns")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

def test_pattern_title_generation():
    """Test pattern title generation"""
    print("\n\nTesting Pattern Title Generation")
    print("=" * 40)
    
    discovery = RSSDiscovery()
    
    test_cases = [
        ("/feed/", "example.com"),
        ("/blog/rss/", "techblog.com"),
        ("/rss.xml", "news.site.com"),
        ("/feeds/all.xml", "www.myblog.org")
    ]
    
    for pattern, domain in test_cases:
        title = discovery.generate_pattern_title(pattern, domain)
        print(f"Pattern: {pattern} + Domain: {domain} = '{title}'")

def test_full_discovery_with_patterns():
    """Test full discovery including patterns"""
    print("\n\nTesting Full Discovery (All Methods)")
    print("=" * 45)
    
    discovery = RSSDiscovery()
    
    # Test with a site that might have RSS feeds
    test_url = "https://techcrunch.com"
    
    print(f"Testing full discovery on: {test_url}")
    
    try:
        result = discovery.find_rss_feeds(test_url)
        
        print(f"\nResults:")
        print(f"- Error: {result.get('error')}")
        print(f"- Paywall: {result.get('is_paywall')}")
        print(f"- Total feeds found: {len(result.get('feeds', []))}")
        
        if result.get('feeds'):
            print(f"\nAll Discovered Feeds:")
            for i, feed in enumerate(result['feeds'], 1):
                print(f"{i}. {feed['title']}")
                print(f"   URL: {feed['url']}")
                print(f"   Discovery Method: {feed['type']}")
                print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")

if __name__ == "__main__":
    test_pattern_discovery()
    test_pattern_title_generation()
    test_full_discovery_with_patterns()
    
    print("\n🎉 RSS pattern discovery tests completed!")