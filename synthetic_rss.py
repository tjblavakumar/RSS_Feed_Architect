from feedgenerator import Rss201rev2Feed
from datetime import datetime
from urllib.parse import urlparse
from typing import List, Dict
import tempfile
import os

class SyntheticRSSGenerator:
    def __init__(self):
        pass
    
    def generate_rss_feed(self, site_url: str, articles: List[Dict]) -> str:
        """
        Generate a synthetic RSS feed from article links.
        Returns the path to the generated RSS file.
        """
        if not articles:
            return None
        
        # Parse site info
        parsed_url = urlparse(site_url)
        site_name = parsed_url.netloc
        
        # Create RSS feed
        feed = Rss201rev2Feed(
            title=f"Synthetic RSS for {site_name}",
            link=site_url,
            description=f"Auto-generated RSS feed from {site_name}",
            language="en-us",
            author_email="rss-architect@example.com",
            author_name="RSS Architect",
            feed_url=f"{site_url}/synthetic-rss.xml",
            ttl=60
        )
        
        # Add articles as feed items
        for article in articles:
            feed.add_item(
                title=article['title'],
                link=article['url'],
                description=f"Article from {site_name}: {article['title']}",
                pubdate=datetime.now(),
                unique_id=article['url']
            )
        
        # Generate RSS XML
        rss_content = feed.writeString('utf-8')
        
        # Save to temporary file and return path
        temp_dir = tempfile.gettempdir()
        rss_filename = f"synthetic_rss_{site_name.replace('.', '_')}.xml"
        rss_path = os.path.join(temp_dir, rss_filename)
        
        with open(rss_path, 'w', encoding='utf-8') as f:
            f.write(rss_content)
        
        return rss_path
    
    def create_synthetic_feed_url(self, site_url: str, articles: List[Dict]) -> str:
        """
        Create a synthetic RSS feed and return a data URL or file path.
        For demo purposes, we'll return a data URL with the RSS content.
        """
        if not articles:
            return None
        
        parsed_url = urlparse(site_url)
        site_name = parsed_url.netloc
        
        feed = Rss201rev2Feed(
            title=f"Synthetic RSS for {site_name}",
            link=site_url,
            description=f"Auto-generated RSS feed from {site_name}",
            language="en-us",
            author_email="rss-architect@example.com",
            author_name="RSS Architect",
            feed_url=f"{site_url}/synthetic-rss.xml",
            ttl=60
        )
        
        for article in articles:
            feed.add_item(
                title=article['title'],
                link=article['url'],
                description=f"Article from {site_name}: {article['title']}",
                pubdate=datetime.now(),
                unique_id=article['url']
            )
        
        rss_content = feed.writeString('utf-8')
        
        # For this demo, we'll return the content as a data URL
        # In production, you might want to serve this from a web server
        return f"data:application/rss+xml;base64,{rss_content.encode('utf-8').hex()}"