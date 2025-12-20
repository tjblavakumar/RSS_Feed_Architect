#!/usr/bin/env python3
"""
Test enhanced error handling for blocked websites
"""

from rss_discovery import RSSDiscovery

def test_blocked_website_handling():
    """Test how the system handles blocked websites"""
    print("Testing Enhanced Error Handling for Blocked Websites")
    print("=" * 60)
    
    discovery = RSSDiscovery()
    
    # Test with Politico (known to block bots)
    blocked_url = "https://www.politico.com/"
    
    print(f"Testing blocked website: {blocked_url}")
    
    try:
        result = discovery.find_rss_feeds(blocked_url)
        
        print(f"\nResults:")
        print(f"- Error: {result.get('error')}")
        print(f"- Paywall: {result.get('is_paywall')}")
        print(f"- Feeds found: {len(result.get('feeds', []))}")
        
        if result.get('feeds'):
            print(f"\nFeeds found despite blocking:")
            for i, feed in enumerate(result['feeds'], 1):
                print(f"{i}. {feed['title']}")
                print(f"   URL: {feed['url']}")
                print(f"   Method: {feed['type']}")
        
        # Test the error message handling
        if result.get('error'):
            if "Failed to fetch page" in result['error']:
                print("\n✅ Proper error detection for blocked website")
                print("The app will show helpful guidance to users")
            else:
                print(f"\n⚠️ Different error type: {result['error']}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")

def test_working_website():
    """Test with a website that should work"""
    print("\n\nTesting Working Website for Comparison")
    print("=" * 45)
    
    discovery = RSSDiscovery()
    
    # Test with a site that should work
    working_url = "https://techcrunch.com"
    
    print(f"Testing working website: {working_url}")
    
    try:
        result = discovery.find_rss_feeds(working_url)
        
        print(f"\nResults:")
        print(f"- Error: {result.get('error')}")
        print(f"- Paywall: {result.get('is_paywall')}")
        print(f"- Feeds found: {len(result.get('feeds', []))}")
        
        if result.get('feeds'):
            print(f"\nFirst 3 feeds found:")
            for i, feed in enumerate(result['feeds'][:3], 1):
                print(f"{i}. {feed['title']}")
                print(f"   Method: {feed['type']}")
        
    except Exception as e:
        print(f"❌ Error with working site: {e}")

if __name__ == "__main__":
    test_blocked_website_handling()
    test_working_website()
    
    print("\n🎯 Enhanced error handling test completed!")