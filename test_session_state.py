#!/usr/bin/env python3
"""
Test script to verify session state handling
"""

import hashlib
from urllib.parse import urlparse

def get_url_hash(url: str) -> str:
    """Generate a short hash for URL to use in widget keys."""
    return hashlib.md5(url.encode()).hexdigest()[:8]

def normalize_url(url: str) -> str:
    """Normalize URL for consistent storage."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')

def test_key_generation():
    """Test that widget keys are generated consistently"""
    test_urls = [
        "https://example.com",
        "https://news.bbc.co.uk",
        "https://www.reddit.com/r/python"
    ]
    
    print("Testing widget key generation:")
    for url in test_urls:
        normalized = normalize_url(url)
        hash_key = get_url_hash(normalized)
        print(f"URL: {url}")
        print(f"Normalized: {normalized}")
        print(f"Hash: {hash_key}")
        print(f"Sample keys: nick_disc_{hash_key}_0, save_synth_{hash_key}")
        print("-" * 50)

if __name__ == "__main__":
    test_key_generation()
    print("✓ Key generation test completed")