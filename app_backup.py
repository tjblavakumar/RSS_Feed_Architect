import streamlit as st
from db_manager import DatabaseManager
from rss_discovery import RSSDiscovery
from synthetic_rss import SyntheticRSSGenerator
from urllib.parse import urlparse
import validators
import hashlib

def get_website_nickname_from_url(url: str) -> str:
    """Extract a default website nickname from URL."""
    parsed = urlparse(url)
    domain = parsed.netloc
    # Remove www. prefix and common TLDs for cleaner names
    if domain.startswith('www.'):
        domain = domain[4:]
    # Capitalize first letter for better presentation
    return domain.replace('.', ' ').title()

# Initialize components
@st.cache_resource
def init_components():
    return DatabaseManager(), RSSDiscovery(), SyntheticRSSGenerator()

def get_url_hash(url: str) -> str:
    """Generate a short hash for URL to use in widget keys."""
    return hashlib.md5(url.encode()).hexdigest()[:8]

def normalize_url(url: str) -> str:
    """Normalize URL for consistent storage."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')

def scan_feed_page():
    """Display the scan feed page."""
    st.header("🔍 Scan for RSS Feeds")
    
    # Debug info
    st.write("Debug: Scan feed page loaded")
    
    # Initialize components
    try:
        db_manager, rss_discovery, rss_generator = init_components()
        st.write("Debug: Components initialized successfully")
    except Exception as e:
        st.error(f"Error initializing components: {e}")
        return
    
    # URL and Website Nickname inputs
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        url_input = st.text_input(
            "🌐 Enter Website URL",
            placeholder="https://example.com",
            help="Enter any website URL to discover or generate RSS feeds"
        )
    
    with col2:
        # Auto-populate website nickname
        website_nickname = ""
        if url_input and validators.url(url_input if url_input.startswith(('http://', 'https://')) else 'https://' + url_input):
            normalized_url = normalize_url(url_input)
            website_nickname = get_website_nickname_from_url(normalized_url)
        
        website_nickname = st.text_input(
            "🏷️ Website Nickname",
            value=website_nickname,
            placeholder="e.g., Tech News, My Blog",
            help="Give this website a memorable name"
        )
    
    with col3:
        st.write("")  # Spacing
        scan_button = st.button("🔍 Scan for Feeds", type="primary")
    
    # Process URL when button is clicked
    if scan_button and url_input and website_nickname:
        if not validators.url(url_input if url_input.startswith(('http://', 'https://')) else 'https://' + url_input):
            st.error("Please enter a valid URL")
            return
        
        if not website_nickname.strip():
            st.error("Please enter a Website Nickname")
            return
        
        normalized_url = normalize_url(url_input)
        
        # Check existing feeds first
        existing_feeds = db_manager.get_feeds_by_site_url(normalized_url)
        
        if existing_feeds:
            st.success(f"✅ Found {len(existing_feeds)} saved feed(s) in database!")
            
            st.subheader("📋 Previously Saved Feeds")
            for feed in existing_feeds:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{feed['user_given_name'] or 'Unnamed Feed'}**")
                    st.code(feed['feed_url'])
                    st.caption(f"Website: {feed['website_nickname']} | Type: {'Synthetic' if feed['is_synthetic'] else 'Discovered'}")
                with col2:
                    st.markdown("✅ **Saved**")
            
            st.divider()
        
        # Scan for new feeds
        with st.spinner("🔍 Scanning website for RSS feeds..."):
            result = rss_discovery.find_rss_feeds(normalized_url)
            
            if result['error']:
                st.error(f"❌ Error: {result['error']}")
                return
            
            if result['is_paywall']:
                st.warning("⚠️ **Notice:** This website appears to be behind a paywall.")
                return
            
            discovered_feeds = result['feeds']
            
            # Filter out already saved feeds
            existing_feed_urls = {feed['feed_url'] for feed in existing_feeds}
            new_discovered_feeds = [feed for feed in discovered_feeds if feed['url'] not in existing_feed_urls]
            
            if new_discovered_feeds:
                st.success(f"✅ Found {len(new_discovered_feeds)} new RSS feed(s)!")
                display_discovered_feeds_table(new_discovered_feeds, normalized_url, website_nickname, db_manager)
            
            elif discovered_feeds:
                st.info("ℹ️ All discovered feeds are already saved in your database.")
            
            else:
                # Generate synthetic feed
                st.info("🔍 No RSS feeds found. Generating synthetic feed from page content...")
                
                with st.spinner("🤖 Analyzing page content..."):
                    soup = rss_discovery.fetch_page(normalized_url)
                    if soup:
                        articles = rss_discovery.extract_article_links(soup, normalized_url)
                        
                        if articles:
                            st.success(f"✅ Generated synthetic feed with {len(articles)} articles!")
                            display_synthetic_feed_option(articles, normalized_url, website_nickname, db_manager)
                        else:
                            st.warning("⚠️ Could not extract meaningful content for RSS generation.")
                    else:
                        st.error("❌ Failed to analyze page content.")
    
    elif scan_button:
        if not url_input:
            st.error("Please enter a Website URL")
        if not website_nickname:
            st.error("Please enter a Website Nickname")

def display_discovered_feeds_table(feeds, normalized_url, website_nickname, db_manager):
    """Display discovered feeds in a simple table format."""
    st.subheader("📡 Newly Discovered Feeds")
    
    # Simple table headers
    col1, col2, col3, col4 = st.columns([0.5, 3, 2, 1])
    with col1:
        st.markdown("**#**")
    with col2:
        st.markdown("**Feed Title & URL**")
    with col3:
        st.markdown("**Feed Nickname**")
    with col4:
        st.markdown("**Action**")
    
    st.divider()
    
    # Display each feed in a form to handle saves properly
    for i, feed in enumerate(feeds):
        with st.form(f"feed_form_{i}"):
            col1, col2, col3, col4 = st.columns([0.5, 3, 2, 1])
            
            with col1:
                st.markdown(f"**{i+1}**")
            
            with col2:
                st.markdown(f"**{feed['title']}**")
                st.code(feed['url'])
            
            with col3:
                nickname = st.text_input(
                    "Feed Nickname",
                    value=feed['title'][:30] + "..." if len(feed['title']) > 30 else feed['title'],
                    key=f"nick_form_{i}",
                    label_visibility="collapsed"
                )
            
            with col4:
                save_clicked = st.form_submit_button("💾 Save")
                
                if save_clicked:
                    try:
                        st.write("Saving feed...")
                        feed_id = db_manager.save_feed(
                            normalized_url,
                            feed['url'],
                            nickname,
                            website_nickname,
                            is_synthetic=False
                        )
                        st.success(f"✅ Saved '{nickname}' with ID {feed_id}!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        import traceback
                        st.error(f"Details: {traceback.format_exc()}")

def display_synthetic_feed_option(articles, normalized_url, website_nickname, db_manager):
    """Display synthetic feed option."""
    st.subheader("🤖 Synthetic Feed Option")
    
    # Show preview of articles
    with st.expander("📄 Preview Articles", expanded=True):
        for i, article in enumerate(articles[:5], 1):
            st.markdown(f"**{i}.** {article['title']}")
            st.caption(article['url'])
    
    # Save synthetic feed using form
    with st.form("synthetic_feed_form"):
        col1, col2, col3, col4 = st.columns([0.5, 3, 2, 1])
        
        with col1:
            st.markdown("**1**")
        
        with col2:
            st.markdown("**Synthetic RSS Feed**")
            st.code(f"Generated from {normalized_url}")
        
        with col3:
            synthetic_nickname = st.text_input(
                "Feed Nickname",
                value="Synthetic Feed",
                label_visibility="collapsed"
            )
        
        with col4:
            save_clicked = st.form_submit_button("💾 Save")
            
            if save_clicked:
                try:
                    st.write("Saving synthetic feed...")
                    synthetic_url = f"{normalized_url}/synthetic-rss.xml"
                    feed_id = db_manager.save_feed(
                        normalized_url,
                        synthetic_url,
                        synthetic_nickname,
                        website_nickname,
                        is_synthetic=True
                    )
                    st.success(f"✅ Saved '{synthetic_nickname}' with ID {feed_id}!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    import traceback
                    st.error(f"Details: {traceback.format_exc()}")

def view_feeds_page():
    """Display the view feeds page."""
    st.header("📚 View Saved Feeds")
    
    db_manager, _, _ = init_components()
    
    # Get all feeds grouped by website nickname
    grouped_feeds = db_manager.get_feeds_grouped_by_website()
    
    if not grouped_feeds:
        st.info("No saved feeds yet. Go to 'Scan Feed' to add some feeds!")
        return
    
    # Display feeds grouped by website nickname
    for website_nickname, feeds in grouped_feeds.items():
        with st.expander(f"🌐 {website_nickname} ({len(feeds)} feeds)", expanded=True):
            for i, feed in enumerate(feeds):
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    st.markdown(f"**{i+1}. {feed['user_given_name'] or 'Unnamed Feed'}**")
                    st.code(feed['feed_url'])
                    st.caption(f"Type: {'🤖 Synthetic' if feed['is_synthetic'] else '🔍 Discovered'} | Saved: {feed['timestamp']}")
                
                with col2:
                    if st.button("🗑️ Delete", key=f"delete_feed_{feed['id']}"):
                        if db_manager.delete_feed(feed['id']):
                            st.success("Feed deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete feed")
                
                if i < len(feeds) - 1:  # Add divider between feeds
                    st.divider()

def main():
    try:
        st.set_page_config(
            page_title="RSS Architect",
            page_icon="📡",
            layout="wide"
        )
        
        # Header
        st.title("📡 RSS Architect")
        st.markdown("*Discover or synthesize RSS feeds from any website*")
        
        # Top Navigation
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.button("🔍 Scan Feed", type="primary", use_container_width=True):
                st.session_state.current_page = "scan"
        
        with col2:
            if st.button("📚 View Feeds", type="secondary", use_container_width=True):
                st.session_state.current_page = "view"
        
        # Initialize current page if not set
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "scan"
        
        st.divider()
        
        # Display the appropriate page
        if st.session_state.current_page == "scan":
            scan_feed_page()
        else:
            view_feeds_page()
            
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        import traceback
        st.error(f"Full error: {traceback.format_exc()}")

if __name__ == "__main__":
    main()