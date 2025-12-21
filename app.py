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
    
    # Split by dots and take the main domain name
    domain_parts = domain.split('.')
    if len(domain_parts) >= 2:
        # Take the main domain name (e.g., 'dealnews' from 'dealnews.com')
        main_domain = domain_parts[0]
        # Capitalize first letter and keep the rest as is
        return main_domain.capitalize()
    else:
        # Fallback to the original method if domain structure is unusual
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
    
    /* Enhanced styling for clickable feed links */
    .feed-link {
        display: inline-block;
        padding: 8px 12px;
        background: linear-gradient(145deg, #E3F2FD, #BBDEFB);
        border: 1px solid #2196F3;
        border-radius: 6px;
        margin: 4px 0;
        transition: all 0.3s ease;
    }
    
    .feed-link:hover {
        background: linear-gradient(145deg, #BBDEFB, #90CAF9);
        box-shadow: 0 2px 8px rgba(33, 150, 243, 0.3);
        transform: translateY(-1px);
    }
    
    .feed-link a {
        color: #1976D2 !important;
        text-decoration: none !important;
        font-weight: bold !important;
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
    rss_discovery = RSSDiscovery(verbose_logging=False)  # Reduce console noise
    rss_generator = SyntheticRSSGenerator()
    
    # Display content based on current page
    if st.session_state.current_page == "scan":
        # SCAN FEED PAGE
        st.header("Scan for RSS Feeds")
        
        # Initialize session state for tracking
        if "last_url" not in st.session_state:
            st.session_state.last_url = ""
        if "generated_nickname" not in st.session_state:
            st.session_state.generated_nickname = ""
        if "nickname_auto_generated" not in st.session_state:
            st.session_state.nickname_auto_generated = False
        if "trigger_autopopulate" not in st.session_state:
            st.session_state.trigger_autopopulate = False
        
        # Input section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            url_input = st.text_input(
                "Website URL", 
                placeholder="https://example.com",
                key="scan_url",
                help="Enter complete URL - nickname will auto-populate"
            )
        
        # Check if we should trigger auto-population
        # This happens when URL changes and becomes a valid complete URL
        if url_input != st.session_state.last_url:
            st.session_state.last_url = url_input
            if url_input:
                try:
                    normalized = normalize_url(url_input)
                    if validators.url(normalized):
                        # URL is valid and complete
                        generated_nickname = get_website_nickname_from_url(normalized)
                        st.session_state.generated_nickname = generated_nickname
                        st.session_state.nickname_auto_generated = True
                        # Directly update the widget's session state
                        st.session_state.scan_nickname = generated_nickname
                except:
                    # Invalid URL - clear auto-generated nickname if it was auto-generated
                    if st.session_state.nickname_auto_generated:
                        st.session_state.generated_nickname = ""
                        st.session_state.nickname_auto_generated = False
                        st.session_state.scan_nickname = ""
            else:
                # Empty URL - clear everything
                st.session_state.generated_nickname = ""
                st.session_state.nickname_auto_generated = False
                st.session_state.scan_nickname = ""
        
        with col2:
            # Don't use value parameter, let the widget use its own session state
            website_nickname = st.text_input(
                "Website Nickname", 
                placeholder="Auto-generated from URL",
                key="scan_nickname",
                help="Auto-populated when you enter a complete URL"
            )
            
            # Detect if user manually changed the nickname
            if website_nickname != st.session_state.generated_nickname:
                st.session_state.nickname_auto_generated = False
            if website_nickname != st.session_state.generated_nickname:
                st.session_state.nickname_auto_generated = False
        
        # Provide visual feedback about auto-population
        if st.session_state.generated_nickname and st.session_state.nickname_auto_generated:
            st.success(f"✨ Auto-generated nickname: '{st.session_state.generated_nickname}'")
        elif url_input and not validators.url(normalize_url(url_input) if url_input else ""):
            st.info("💡 Enter a complete URL (like https://example.com) to auto-generate nickname")
        
        # Scan button
        st.markdown('<div class="scan-button">', unsafe_allow_html=True)
        scan_clicked = st.button("🔍 Scan for Feeds", type="primary", use_container_width=True)
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
                    # Get nickname (use the current value from the input field)
                    current_nickname = website_nickname
                    # If somehow still empty, generate it
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
                    # Make feed URL clickable and open in new tab with enhanced styling
                    st.markdown(f"""
                    <div class="feed-link">
                        🔗 <a href="{feed['url']}" target="_blank">
                        <strong>Test Feed:</strong> {feed['url'][:50]}{'...' if len(feed['url']) > 50 else ''} 
                        <span style="font-size: 0.9em;">🔗 (Opens in new tab)</span>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Keep code block for easy copying
                    with st.expander("📋 Copy URL", expanded=False):
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
                            # Make feed URL clickable and open in new tab with enhanced styling
                            st.markdown(f"""
                            <div class="feed-link">
                                🔗 <a href="{feed['feed_url']}" target="_blank">
                                <strong>Test Feed:</strong> {feed['feed_url'][:50]}{'...' if len(feed['feed_url']) > 50 else ''} 
                                <span style="font-size: 0.9em;">🔗 (Opens in new tab)</span>
                                </a>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Keep code block for easy copying in a collapsible section
                            with st.expander("📋 Copy URL", expanded=False):
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