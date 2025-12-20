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
    
    # Custom CSS for 3D navigation buttons
    st.markdown("""
    <style>
    /* Custom 3D Navigation Buttons - Enhanced Blue Styling */
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background: linear-gradient(145deg, #2196F3, #1976D2) !important;
        color: white !important;
        border: 2px solid #0D47A1 !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        box-shadow: 0 6px 12px rgba(33, 150, 243, 0.4) !important;
        width: 100% !important;
        min-height: 60px !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="column"]:nth-child(1) .stButton > button:hover {
        background: linear-gradient(145deg, #1976D2, #0D47A1) !important;
        box-shadow: 0 8px 16px rgba(33, 150, 243, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    div[data-testid="column"]:nth-child(1) .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 4px 8px rgba(33, 150, 243, 0.3) !important;
    }
    
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background: linear-gradient(145deg, #6C757D, #5A6268) !important;
        color: white !important;
        border: 2px solid #495057 !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2) !important;
        width: 100% !important;
        min-height: 60px !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="column"]:nth-child(2) .stButton > button:hover {
        background: linear-gradient(145deg, #5A6268, #495057) !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    div[data-testid="column"]:nth-child(2) .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    /* Enhanced styling for main scan button and all primary buttons */
    .scan-button .stButton > button,
    .scan-button button,
    button[kind="primary"],
    .stButton > button[kind="primary"],
    button[data-testid="baseButton-primary"],
    .stFormSubmitButton > button,
    button[data-testid="stFormSubmitButton"] {
        background: linear-gradient(145deg, #2196F3, #1976D2) !important;
        color: white !important;
        border: 2px solid #0D47A1 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 8px rgba(33, 150, 243, 0.4) !important;
        transition: all 0.3s ease !important;
        min-height: 45px !important;
    }
    
    .scan-button .stButton > button:hover,
    .scan-button button:hover,
    button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    .stFormSubmitButton > button:hover,
    button[data-testid="stFormSubmitButton"]:hover {
        background: linear-gradient(145deg, #1976D2, #0D47A1) !important;
        box-shadow: 0 6px 12px rgba(33, 150, 243, 0.6) !important;
        transform: translateY(-1px) !important;
    }
    
    .scan-button .stButton > button:active,
    .scan-button button:active,
    button[kind="primary"]:active,
    .stButton > button[kind="primary"]:active,
    button[data-testid="baseButton-primary"]:active,
    .stFormSubmitButton > button:active,
    button[data-testid="stFormSubmitButton"]:active {
        transform: translateY(0px) !important;
        box-shadow: 0 3px 6px rgba(33, 150, 243, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📡 RSS Architect")
    st.markdown("*Discover or synthesize RSS feeds from any website*")
    
    # Navigation with custom 3D buttons
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        if st.button("🔍 Scan Feed", use_container_width=True, key="nav_scan"):
            st.session_state.current_page = "scan"
    
    with col2:
        if st.button("📚 View Feeds", use_container_width=True, key="nav_view"):
            st.session_state.current_page = "view"
    
    # Initialize current page if not set
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "scan"
    
    st.divider()
    
    # Initialize components
    db_manager = DatabaseManager()
    rss_discovery = RSSDiscovery()
    rss_generator = SyntheticRSSGenerator()
    
    def update_scan_state():
        """Callback to update nickname from URL before form submission processing."""
        if "scan_url" in st.session_state and "scan_nickname" in st.session_state:
            url = st.session_state.scan_url
            nickname = st.session_state.scan_nickname
            
            if url and not nickname:
                # Try to normalize and generate nickname
                # We do a quick check here, full validation happens in main flow
                normalized = normalize_url(url)
                if validators.url(normalized):
                    st.session_state.scan_nickname = get_website_nickname_from_url(normalized)
    
    # Display content based on current page
    if st.session_state.current_page == "scan":
        # SCAN FEED PAGE
        st.header("Scan for RSS Feeds")
        
        # Input section
        with st.form("scan_form"):
            # Input section
            col1, col2 = st.columns([2, 1])
            
            with col1:
                url_input = st.text_input(
                    "Website URL", 
                    placeholder="https://example.com",
                    key="scan_url"
                )
            
            with col2:
                # Make nickname optional and bind to session state
                if "scan_nickname" not in st.session_state:
                    st.session_state.scan_nickname = ""
                    
                website_nickname = st.text_input(
                    "Website Nickname", 
                    placeholder="Auto-generated if empty",
                    key="scan_nickname"
                )
            
            # Add CSS class wrapper for the scan button
            st.markdown('<div class="scan-button">', unsafe_allow_html=True)
            scan_clicked = st.form_submit_button("🔍 Scan for Feeds", type="primary")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if scan_clicked:
            if not url_input:
                st.error("Please enter a URL")
            else:
                # Normalize URL first to ensure we can generate a nickname from it
                normalized_url_temp = normalize_url(url_input)
                
                if not validators.url(normalized_url_temp):
                    st.error("Please enter a valid URL")
                else:
                    # Get nickname (it might have been updated by the callback)
                    current_nickname = st.session_state.scan_nickname
                    # If somehow still empty (e.g. invalid URL during callback but valid now?), generate it
                    if not current_nickname:
                        current_nickname = get_website_nickname_from_url(normalized_url_temp)
                    
                    # Store in session state for use in save operations
                    st.session_state.current_url = normalized_url_temp
                    st.session_state.current_website_nickname = current_nickname
                
                # Process the URL
                normalized_url = st.session_state.current_url
                
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
                        if "Failed to fetch page" in result['error']:
                            st.warning("⚠️ **Website Access Blocked**")
                            st.info("""
                            This website appears to be blocking automated requests. This is common with major news sites that have bot protection.
                            
                            **What you can try:**
                            1. Look for an RSS or Feeds page on their website
                            2. Check their footer for RSS links  
                            3. Try adding `/rss` or `/feed` to their URL manually
                            4. Search for "[website name] RSS feeds" in a search engine
                            """)
                        else:
                            st.error(f"Error: {result['error']}")
                    elif result['is_paywall']:
                        st.warning("This website appears to be behind a paywall.")
                    else:
                        discovered_feeds = result['feeds']
                        
                        if discovered_feeds:
                            st.success(f"Found {len(discovered_feeds)} RSS feeds!")
                            st.session_state.discovered_feeds = discovered_feeds
                        else:
                            st.info("No RSS feeds found for this website.")
        
        # Display discovered feeds if available
        if 'discovered_feeds' in st.session_state and st.session_state.discovered_feeds:
            st.subheader("📡 Discovered Feeds")
            
            for i, feed in enumerate(st.session_state.discovered_feeds):
                with st.expander(f"Feed {i+1}: {feed['title']}", expanded=True):
                    st.code(feed['url'])
                    
                    # Individual save form for each feed (not nested)
                    with st.form(f"save_form_{i}"):
                        feed_nickname = st.text_input(
                            "Feed Nickname", 
                            value=feed['title'][:50],
                            key=f"nickname_{i}"
                        )
                        
                        save_clicked = st.form_submit_button(f"💾 Save Feed {i+1}")
                        
                        if save_clicked:
                            try:
                                # Check if feed already exists
                                if db_manager.feed_exists(feed['url']):
                                    existing_feed = db_manager.get_existing_feed(feed['url'])
                                    st.warning(f"⚠️ Feed already exists!")
                                    st.info(f"Existing feed: '{existing_feed['user_given_name']}' in website '{existing_feed['website_nickname']}'")
                                else:
                                    feed_id = db_manager.save_feed(
                                        st.session_state.current_url,
                                        feed['url'],
                                        feed_nickname,
                                        st.session_state.current_website_nickname,
                                        is_synthetic=False
                                    )
                                    st.success(f"✅ Saved '{feed_nickname}' successfully! (ID: {feed_id})")
                            except Exception as e:
                                st.error(f"❌ Failed to save: {str(e)}")
        
    
    else:
        # VIEW FEEDS PAGE
        st.header("View Saved Feeds")
        
        # Get all feeds grouped by website
        grouped_feeds = db_manager.get_feeds_grouped_by_website()
        
        if not grouped_feeds:
            st.info("No saved feeds yet. Go to 'Scan Feed' page to add some feeds!")
        else:
            for website_nickname, feeds in grouped_feeds.items():
                with st.expander(f"🌐 {website_nickname} ({len(feeds)} feeds)", expanded=False):
                    for i, feed in enumerate(feeds, 1):
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.write(f"**{i}. {feed['user_given_name']}**")
                            st.code(feed['feed_url'])
                            st.caption(f"Type: {'🤖 Synthetic' if feed['is_synthetic'] else '🔍 Discovered'} | Saved: {feed['timestamp']}")
                        
                        with col2:
                            # Use regular button instead of form to avoid nesting
                            if st.button("🗑️ Delete", key=f"delete_{feed['id']}"):
                                if db_manager.delete_feed(feed['id']):
                                    st.success("Feed deleted!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete feed")

if __name__ == "__main__":
    main()