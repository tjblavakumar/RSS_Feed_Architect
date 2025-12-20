import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "feed_storage.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS FeedMaster (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_url TEXT NOT NULL,
                    feed_url TEXT NOT NULL,
                    user_given_name TEXT,
                    website_nickname TEXT,
                    is_synthetic BOOLEAN NOT NULL DEFAULT 0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Add website_nickname column if it doesn't exist (for existing databases)
            try:
                cursor.execute("ALTER TABLE FeedMaster ADD COLUMN website_nickname TEXT")
                conn.commit()
            except sqlite3.OperationalError:
                # Column already exists
                pass
    
    def get_feeds_by_site_url(self, site_url: str) -> List[Dict]:
        """Get all feeds for a given site URL."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, site_url, feed_url, user_given_name, website_nickname, is_synthetic, timestamp
                FROM FeedMaster 
                WHERE site_url = ?
            """, (site_url,))
            
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def save_feed(self, site_url: str, feed_url: str, user_given_name: str, website_nickname: str, is_synthetic: bool = False) -> int:
        """Save a new feed to the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO FeedMaster (site_url, feed_url, user_given_name, website_nickname, is_synthetic, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (site_url, feed_url, user_given_name, website_nickname, is_synthetic, datetime.now()))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_feeds(self) -> List[Dict]:
        """Get all saved feeds."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, site_url, feed_url, user_given_name, website_nickname, is_synthetic, timestamp
                FROM FeedMaster 
                ORDER BY website_nickname, timestamp DESC
            """)
            
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_feeds_grouped_by_website(self) -> Dict[str, List[Dict]]:
        """Get all feeds grouped by website nickname."""
        feeds = self.get_all_feeds()
        grouped = {}
        
        for feed in feeds:
            website_nick = feed['website_nickname'] or 'Unnamed Website'
            if website_nick not in grouped:
                grouped[website_nick] = []
            grouped[website_nick].append(feed)
        
        return grouped
    
    def feed_exists(self, feed_url: str) -> bool:
        """Check if a feed URL already exists in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM FeedMaster WHERE feed_url = ?
            """, (feed_url,))
            count = cursor.fetchone()[0]
            return count > 0
    
    def get_existing_feed(self, feed_url: str) -> Optional[Dict]:
        """Get existing feed details by feed URL."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, site_url, feed_url, user_given_name, website_nickname, is_synthetic, timestamp
                FROM FeedMaster 
                WHERE feed_url = ?
            """, (feed_url,))
            
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def delete_feed(self, feed_id: int) -> bool:
        """Delete a feed by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM FeedMaster WHERE id = ?", (feed_id,))
            conn.commit()
            return cursor.rowcount > 0