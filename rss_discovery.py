import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional
import re

class RSSDiscovery:
    def __init__(self, verbose_logging: bool = True):
        self.verbose_logging = verbose_logging
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        self.paywall_keywords = [
            'subscriber-only', 'please log in to read', 'create an account to continue',
            'subscribe to continue', 'premium content', 'paywall', 'subscription required',
            'sign up to read', 'login to view', 'members only', 'paid subscription'
        ]
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page with retry logic."""
        import time
        
        # Try different approaches if the first one fails
        retry_configs = [
            # First attempt: Full headers
            {'headers': self.headers, 'timeout': 10},
            # Second attempt: Minimal headers with different User-Agent
            {'headers': {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
            }, 'timeout': 15},
            # Third attempt: Simple request
            {'headers': {
                'User-Agent': 'RSS Reader Bot 1.0'
            }, 'timeout': 20}
        ]
        
        for attempt, config in enumerate(retry_configs, 1):
            try:
                response = requests.get(url, **config)
                
                # Check for various HTTP status codes
                if response.status_code == 200:
                    return BeautifulSoup(response.content, 'html.parser')
                elif response.status_code == 403:
                    if attempt < len(retry_configs):
                        time.sleep(2)  # Wait before retry
                        continue
                elif response.status_code == 429:
                    if attempt < len(retry_configs):
                        time.sleep(5)  # Wait longer for rate limits
                        continue
                else:
                    response.raise_for_status()
                    
            except requests.exceptions.Timeout:
                if attempt < len(retry_configs):
                    continue
            except requests.exceptions.ConnectionError:
                if attempt < len(retry_configs):
                    time.sleep(1)
                    continue
            except requests.RequestException as e:
                if attempt < len(retry_configs):
                    continue
        
        return None
    
    def check_paywall(self, soup: BeautifulSoup) -> bool:
        """Check if the page appears to be behind a paywall."""
        page_text = soup.get_text().lower()
        return any(keyword in page_text for keyword in self.paywall_keywords)
    
    def find_rss_feeds(self, url: str) -> Dict:
        """
        Find RSS feeds for a given URL using multiple methods.
        Returns a dict with 'feeds', 'is_paywall', and 'error' keys.
        """
        soup = self.fetch_page(url)
        if not soup:
            # If we can't fetch the main page, try pattern discovery anyway
            pattern_rss_links = self.try_common_rss_patterns(url)
            
            if pattern_rss_links:
                return {'feeds': pattern_rss_links, 'is_paywall': False, 'error': None}
            else:
                return {'feeds': [], 'is_paywall': False, 'error': 'Failed to fetch page and no RSS patterns found'}
        
        # Check for paywall
        if self.check_paywall(soup):
            return {'feeds': [], 'is_paywall': True, 'error': None}
        
        # Look for RSS feed links using multiple methods
        rss_links = []
        
        # Method 1: Find <link> tags with RSS/Atom feeds (traditional method)
        link_tags = soup.find_all('link', {
            'rel': 'alternate',
            'type': ['application/rss+xml', 'application/atom+xml']
        })
        
        method1_count = 0
        for link in link_tags:
            href = link.get('href')
            if href:
                full_url = urljoin(url, href)
                title = link.get('title', 'RSS Feed')
                rss_links.append({
                    'url': full_url,
                    'title': title,
                    'type': 'discovered'
                })
                method1_count += 1
        
        # Method 2: Find RSS feed URLs in page content (for RSS directory pages)
        content_rss_links = self.find_rss_links_in_content(soup, url)
        method2_count = len(content_rss_links)
        rss_links.extend(content_rss_links)
        
        # Method 3: Try common RSS URL patterns
        pattern_rss_links = self.try_common_rss_patterns(url)
        method3_count = len(pattern_rss_links)
        rss_links.extend(pattern_rss_links)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_rss_links = []
        for link in rss_links:
            if link['url'] not in seen_urls:
                seen_urls.add(link['url'])
                unique_rss_links.append(link)
        
        # Summary logging
        total_found = len(unique_rss_links)
        if self.verbose_logging:
            if total_found > 0:
                print(f"✅ RSS Discovery Summary: Found {total_found} unique feeds")
                print(f"   Method 1 (HTML links): {method1_count} feeds")
                print(f"   Method 2 (Content scan): {method2_count} feeds") 
                print(f"   Method 3 (Pattern test): {method3_count} feeds")
            else:
                print("ℹ️  No RSS feeds found using any discovery method")
        
        return {'feeds': unique_rss_links, 'is_paywall': False, 'error': None}
    
    def try_common_rss_patterns(self, base_url: str) -> List[Dict]:
        """Try common RSS URL patterns to find feeds."""
        rss_links = []
        
        # Parse the base URL
        parsed_url = urlparse(base_url)
        base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # Common RSS URL patterns to try
        common_patterns = [
            '/feed/',
            '/rss/',
            '/blog/feed/',
            '/blog/rss/',
            '/rss.xml',
            '/feed.xml',
            '/atom.xml',
            '/blog/rss.xml',
            '/blog/feed.xml',
            '/blog/atom.xml',
            '/feeds/',
            '/feeds/all.xml',
            '/feeds/posts/default',
            '/index.xml',
            '/news/rss/',
            '/news/feed/',
            '/?feed=rss2',
            '/?feed=atom',
            '/wp/feed/',
            '/wordpress/feed/',
            '/feed',
            '/rss',
            '/atom'
        ]
        
        # Only show detailed pattern testing if no feeds found by other methods
        # This reduces console noise when traditional methods work
        
        for pattern in common_patterns:
            test_url = base_domain + pattern
            
            try:
                # Use lighter headers for pattern testing
                light_headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                
                # Test if the URL returns a valid RSS feed
                response = requests.head(test_url, headers=light_headers, timeout=8, allow_redirects=True)
                
                if response.status_code == 200:
                    # Check content type
                    content_type = response.headers.get('content-type', '').lower()
                    
                    if any(rss_type in content_type for rss_type in ['xml', 'rss', 'atom']):
                        # Generate a descriptive title
                        title = self.generate_pattern_title(pattern, parsed_url.netloc)
                        
                        rss_links.append({
                            'url': test_url,
                            'title': title,
                            'type': 'pattern-discovered'
                        })
                    
            except requests.RequestException:
                # Silently continue to next pattern
                continue
        
        return rss_links
    
    def generate_pattern_title(self, pattern: str, domain: str) -> str:
        """Generate a descriptive title for pattern-discovered feeds."""
        domain_clean = domain.replace('www.', '')
        
        # Map patterns to descriptive names
        pattern_names = {
            '/feed/': 'Main Feed',
            '/rss/': 'RSS Feed',
            '/blog/feed/': 'Blog Feed',
            '/blog/rss/': 'Blog RSS',
            '/rss.xml': 'RSS Feed',
            '/feed.xml': 'Main Feed',
            '/atom.xml': 'Atom Feed',
            '/blog/rss.xml': 'Blog RSS',
            '/blog/feed.xml': 'Blog Feed',
            '/blog/atom.xml': 'Blog Atom Feed',
            '/feeds/': 'All Feeds',
            '/feeds/all.xml': 'All Posts Feed',
            '/feeds/posts/default': 'Posts Feed',
            '/index.xml': 'Index Feed',
            '/news/rss/': 'News RSS',
            '/news/feed/': 'News Feed',
            '/?feed=rss2': 'RSS2 Feed',
            '/?feed=atom': 'Atom Feed',
            '/wp/feed/': 'WordPress Feed',
            '/wordpress/feed/': 'WordPress Feed',
            '/feed': 'Main Feed',
            '/rss': 'RSS Feed',
            '/atom': 'Atom Feed'
        }
        
        pattern_name = pattern_names.get(pattern, 'RSS Feed')
        return f"{domain_clean} - {pattern_name}"
    
    def find_rss_links_in_content(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Find RSS feed URLs in page content (for RSS directory pages)."""
        rss_links = []
        
        # Look for <a> tags that point to RSS feeds
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True)
            
            if href and self.is_rss_url(href):
                full_url = urljoin(base_url, href)
                
                # Use link text as title, or extract from URL if text is not descriptive
                title = text if text and len(text) > 3 else self.extract_title_from_url(href)
                
                rss_links.append({
                    'url': full_url,
                    'title': title,
                    'type': 'discovered'
                })
        
        # Also look for URLs in text content that might be RSS feeds
        page_text = soup.get_text()
        url_pattern = r'https?://[^\s<>"]+\.(?:xml|rss|atom)(?:\?[^\s<>"]*)?'
        text_urls = re.findall(url_pattern, page_text)
        
        for text_url in text_urls:
            if self.is_rss_url(text_url):
                title = self.extract_title_from_url(text_url)
                rss_links.append({
                    'url': text_url,
                    'title': title,
                    'type': 'discovered'
                })
        
        return rss_links
    
    def is_rss_url(self, url: str) -> bool:
        """Check if a URL is likely an RSS feed."""
        url_lower = url.lower()
        
        # Check for common RSS indicators
        rss_indicators = [
            '.xml', '.rss', '.atom',
            '/rss', '/feed', '/feeds',
            'rss.xml', 'feed.xml', 'atom.xml',
            'rss/', 'feed/', 'feeds/',
            'format=rss', 'type=rss', 'feed=rss'
        ]
        
        return any(indicator in url_lower for indicator in rss_indicators)
    
    def extract_title_from_url(self, url: str) -> str:
        """Extract a descriptive title from RSS URL."""
        parsed = urlparse(url)
        path = parsed.path
        
        # Try to extract meaningful parts from the path
        path_parts = [part for part in path.split('/') if part and part not in ['rss', 'feed', 'feeds', 'xml']]
        
        if path_parts:
            # Use the last meaningful part as title
            title_part = path_parts[-1].replace('-', ' ').replace('_', ' ').title()
            return f"{title_part} RSS Feed"
        else:
            # Use domain name
            domain = parsed.netloc.replace('www.', '')
            return f"{domain} RSS Feed"
    
    def extract_article_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract potential article links from the page."""
        article_links = []
        
        # Look for <a> tags that likely contain article titles
        for link in soup.find_all('a', href=True):
            text = link.get_text(strip=True)
            href = link.get('href')
            
            # Filter links with meaningful text (more than 5 words)
            if text and len(text.split()) > 5 and href:
                full_url = urljoin(base_url, href)
                
                # Skip obvious non-article links
                if not any(skip in href.lower() for skip in ['javascript:', 'mailto:', '#', 'login', 'register', 'subscribe']):
                    article_links.append({
                        'title': text[:200],  # Limit title length
                        'url': full_url
                    })
        
        # Remove duplicates and limit to reasonable number
        seen_urls = set()
        unique_links = []
        for link in article_links:
            if link['url'] not in seen_urls and len(unique_links) < 20:
                seen_urls.add(link['url'])
                unique_links.append(link)
        
        return unique_links