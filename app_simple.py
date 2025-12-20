import streamlit as st
from db_manager import DatabaseManager
from rss_discovery import RSSDiscovery
from synthetic_rss import SyntheticRSSGenerator
from urllib.parse import urlparse
import validators

def get_website_nickname_from_url(url: str) -> str:
    """Extract a default website nickname from URL."""
    parsed = urlparse(url)
    domain = parsed.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain.replace('.', ' ').title()

def normalize_url(url: str) -> str:
    """Normalize URL for consistent storage."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')

def main():
    st.set_page_config(
        page_title="RSS Architect",
        page_icon="📡",
        layout="wide"
    )
    
    st.title("📡 RSS Architect")
    st.markdown("*Discover or synthesize RSS feeds from any website*")
    
    # Initialize components
    db_manager = DatabaseManager()
    rss_discovery = RSSDiscovery()
    rss_generator = SyntheticRSSGenerator()
    
    # Navigation tabs
    tab1, tab2 = st.tabs(["🔍 Scan Feed", "📚 View Feeds"])
    
    with tab1:
        st.header("Scan for RSS Feeds")
        
        # Input form
        with st.form("scan_form"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                url_input = st.text_input("Website URL", placeholder="https://example.com")
            
            with col2:
                website_nickname = st.text_input("Website Nickname", placeholder="My Site")
            
            scan_clicked = st.form_submit_button("🔍 Scan for Feeds", type="primary")
            
            if scan_clicked:
                if not url_input or not website_nickname:
                    st.error("Please enter both URL and Website Nickname")
                elif not validators.url(url_input if url_input.startswith(('http://', 'https://')) else 'https://' + url_input):
                    st.error("Please enter a valid URL")
                else:
                    # Process the URL
                    normalized_url = normalize_url(url_input)
                    
                    # Check existing feeds
                    existing_feeds = db_manager.get_feeds_by_site_url(normalized_url)
                    if existing_feeds:
                        st.success(f"Found {len(existing_feeds)} existing feeds in database")
                        for feed in existing_feeds:
                            st.write(f"- {feed['user_given_name']}: {feed['feed_url']}")
                    
                    # Scan for new feeds
                    with st.spinner("Scanning for feeds..."):
                        result = rss_discovery.find_rss_feeds(normalized_url)
                        
                        if result['error']:
                            st.error(f"Error: {result['error']}")
                        elif result['is_paywall']:
                            st.warning("This website appears to be behind a paywall.")
                        else:
                            discovered_feeds = result['feeds']
                            
                            if discovered_feeds:
                                st.success(f"Found {len(discovered_feeds)} RSS feeds!")
                                
                                # Display feeds with individual save forms
                                for i, feed in enumerate(discovered_feeds):
                                    with st.expander(f"Feed {i+1}: {feed['title']}", expanded=True):
                                        st.code(feed['url'])
                                        
                                        # Individual save form for each feed
                                        with st.form(f"save_form_{i}"):
                                            feed_nickname = st.text_input(
                                                "Feed Nickname", 
                                                value=feed['title'][:50],
                                                key=f"nickname_{i}"
                                            )
                                            
                                            save_clicked = st.form_submit_button(f"💾 Save Feed {i+1}")
                                            
                                            if save_clicked:
                                                try:
                                                    feed_id = db_manager.save_feed(
                                                        normalized_url,
                                                        feed['url'],
                                                        feed_nickname,
                                                        website_nickname,
                                                        is_synthetic=False
                                                    )
                                                    st.success(f"✅ Saved '{feed_nickname}' successfully! (ID: {feed_id})")
                                                except Exception as e:
                                                    st.error(f"❌ Failed to save: {str(e)}")
                            else:
                                # Try synthetic generation
                                st.info("No RSS feeds found. Generating synthetic feed...")
                                
                                soup = rss_discovery.fetch_page(normalized_url)
                                if soup:
                                    articles = rss_discovery.extract_article_links(soup, normalized_url)
                                    
                                    if articles:
                                        st.success(f"Generated synthetic feed with {len(articles)} articles!")
                                        
                                        # Show preview
                                        with st.expander("Preview Articles", expanded=True):
                                            for j, article in enumerate(articles[:5], 1):
                                                st.write(f"{j}. {article['title']}")
                                        
                                        # Save synthetic feed
                                        with st.form("save_synthetic"):
                                            synthetic_nickname = st.text_input(
                                                "Synthetic Feed Nickname", 
                                                value="Synthetic Feed"
                                            )
                                            
                                            save_synthetic = st.form_submit_button("💾 Save Synthetic Feed")
                                            
                                            if save_synthetic:
                                                try:
                                                    synthetic_url = f"{normalized_url}/synthetic-rss.xml"
                                                    feed_id = db_manager.save_feed(
                                                        normalized_url,
                                                        synthetic_url,
                                                        synthetic_nickname,
                                                        website_nickname,
                                                        is_synthetic=True
                                                    )
                                                    st.success(f"✅ Saved synthetic feed successfully! (ID: {feed_id})")
                                                except Exception as e:
                                                    st.error(f"❌ Failed to save synthetic feed: {str(e)}")
                                    else:
                                        st.warning("Could not extract meaningful content for RSS generation.")
                                else:
                                    st.error("Failed to analyze page content.")
    
    with tab2:
        st.header("View Saved Feeds")
        
        # Get all feeds grouped by website
        grouped_feeds = db_manager.get_feeds_grouped_by_website()
        
        if not grouped_feeds:
            st.info("No saved feeds yet. Go to 'Scan Feed' tab to add some feeds!")
        else:
            for website_nickname, feeds in grouped_feeds.items():
                with st.expander(f"🌐 {website_nickname} ({len(feeds)} feeds)", expanded=True):
                    for i, feed in enumerate(feeds, 1):
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.write(f"**{i}. {feed['user_given_name']}**")
                            st.code(feed['feed_url'])
                            st.caption(f"Type: {'🤖 Synthetic' if feed['is_synthetic'] else '🔍 Discovered'} | Saved: {feed['timestamp']}")
                        
                        with col2:
                            # Individual delete form
                            with st.form(f"delete_form_{feed['id']}"):
                                delete_clicked = st.form_submit_button("🗑️ Delete")
                                
                                if delete_clicked:
                                    if db_manager.delete_feed(feed['id']):
                                        st.success("Feed deleted!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete feed")

if __name__ == "__main__":
    main()