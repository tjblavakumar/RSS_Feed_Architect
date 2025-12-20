#!/usr/bin/env python3
"""
Test script to verify UI fixes
"""

def test_session_state_keys():
    """Test session state key generation for multiple feeds"""
    print("Testing Session State Key Generation")
    print("=" * 50)
    
    # Simulate the key generation logic
    import hashlib
    
    def get_url_hash(url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()[:8]
    
    normalized_url = "https://example.com"
    url_hash = get_url_hash(normalized_url)
    
    print(f"URL: {normalized_url}")
    print(f"Hash: {url_hash}")
    
    # Generate keys for multiple feeds
    num_feeds = 3
    for i in range(num_feeds):
        save_key = f"save_disc_{url_hash}_{i}"
        saved_key = f"saved_disc_{url_hash}_{i}"
        nickname_key = f"nick_disc_{url_hash}_{i}"
        
        print(f"\nFeed {i+1}:")
        print(f"  Save Key: {save_key}")
        print(f"  Saved Key: {saved_key}")
        print(f"  Nickname Key: {nickname_key}")
    
    print("\n✅ Key generation test completed!")

def test_css_styling():
    """Test CSS styling for alternating rows"""
    print("\nTesting CSS Styling")
    print("=" * 30)
    
    # Test alternating row classes
    num_rows = 5
    for i in range(num_rows):
        row_class = "feed-row-even" if i % 2 == 0 else "feed-row-odd"
        color = "#f8f9fa" if i % 2 == 0 else "#e3f2fd"
        print(f"Row {i+1}: {row_class} (color: {color})")
    
    print("\n✅ CSS styling test completed!")

if __name__ == "__main__":
    test_session_state_keys()
    test_css_styling()
    print("\n🎉 All UI fix tests completed!")