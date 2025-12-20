#!/usr/bin/env python3
"""
Test RSS discovery specifically for Politico website
"""

from rss_discovery import RSSDiscovery

def test_politico_access():
    """Test accessing Politico website with enhanced headers"""
    print("Testing Politico Website Access")
    print("=" * 40)
    
    discovery = RSSDiscovery()
    
    # Test the main Politico URL
    url = "https://www.politico.com/"
    
    print(f"Testing URL: {url}")
    print("Attempting to fetch page with enhanced headers and retry logic...")
    
    try:
        soup = discovery.fetch_page(url)
        
        if soup:
            print("✅ Successfully fetched Politico page!")
            print(f"Page title: {soup.title.string if soup.title else 'No title found'}")
            
            # Try to find any RSS-related content
            rss_links = soup.find_all('a', href=True)
            rss_count = 0
            
            for link in rss_links:
                href = link.get('href', '').lower()
                if any(rss_term in href for rss_term in ['rss', 'feed', 'xml']):
                    print(f"Found potential RSS link: {link.get('href')}")
                    rss_count += 1
                    if rss_count >= 5:  # Limit output
                        break
            
            if rss_count == 0:
                print("No obvious RSS links found in page content")
                
        else:
            print("❌ Failed to fetch Politico page")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")

def test_politico_full_discovery():
    """Test full RSS discovery on Politico"""
    print("\n\nTesting Full RSS Discovery on Politico")
    print("=" * 45)
    
    discovery = RSSDiscovery()
    
    url = "https://www.politico.com/"
    
    try:
        result = discovery.find_rss_feeds(url)
        
        print(f"Discovery Results:")
        print(f"- Error: {result.get('error')}")
        print(f"- Paywall: {result.get('is_paywall')}")
        print(f"- Feeds found: {len(result.get('feeds', []))}")
        
        if result.get('feeds'):
            print(f"\nDiscovered RSS Feeds:")
            for i, feed in enumerate(result['feeds'], 1):
                print(f"{i}. {feed['title']}")
                print(f"   URL: {feed['url']}")
                print(f"   Method: {feed['type']}")
                print()
        else:
            print("\nNo RSS feeds discovered")
            
    except Exception as e:
        print(f"❌ Error during full discovery: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")

def test_alternative_politico_urls():
    """Test alternative Politico URLs that might work better"""
    print("\n\nTesting Alternative Politico URLs")
    print("=" * 40)
    
    discovery = RSSDiscovery()
    
    # Try some alternative URLs that might be less protected
    alternative_urls = [
        "https://www.politico.com/rss",
        "https://www.politico.com/feed",
        "https://www.politico.com/rss/",
        "https://www.politico.com/feed/",
        "https://rss.politico.com/",
        "https://feeds.politico.com/"
    ]
    
    for url in alternative_urls:
        print(f"\nTrying: {url}")
        try:
            import requests
            response = requests.head(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }, timeout=10)
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                print(f"Content-Type: {content_type}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_politico_access()
    test_politico_full_discovery()
    test_alternative_politico_urls()
    
    print("\n🎯 Politico RSS discovery test completed!")